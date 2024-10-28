import os
import time
from pandasai.llm.local_llm import LocalLLM
import streamlit as st 
from pandasai.connectors import MySQLConnector
from pandasai import SmartDataframe
import threading
from queue import Queue

# Initialize session state for generation control
def init_session_state():
    if 'generation_stopped' not in st.session_state:
        st.session_state['generation_stopped'] = False
    if 'is_generating' not in st.session_state:
        st.session_state['is_generating'] = False
    if 'button_state' not in st.session_state:
        st.session_state['button_state'] = "Generate"
    if 'response_queue' not in st.session_state:
        st.session_state['response_queue'] = Queue()

# Initialize session state at startup
init_session_state()

# Konfigurasi MySQL Connector
my_connector = MySQLConnector(
    config={
        "host": "localhost",
        "port": 3306,
        "database": "pandasai",
        "username": "root",
        "password": "",
        "table": "cleaned_mb_data",
    }
)

model_llama="llama3.1:8b"

# Konfigurasi model untuk Llama-3.1-8B
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model=model_llama
)

# Inisialisasi SmartDataframe dengan caching
df_connector = SmartDataframe(
    my_connector, 
    config={
        "llm": model,
        "cache_path": "./cache",
        "enable_cache": True,
        "verbose": True
    }
)

def generate_response(prompt, stopped_flag, queue):
    """Thread-safe generate response function"""
    try:
        if not stopped_flag[0]:  # Check thread-safe flag
            response = df_connector.chat(prompt)
            if not stopped_flag[0]:  # Check again before putting result
                queue.put(("success", response))
    except Exception as e:
        if not stopped_flag[0]:
            queue.put(("error", str(e)))

def handle_button_click():
    """Handle button state changes"""
    if st.session_state.button_state == "Generate":
        st.session_state.button_state = "Stop"
        st.session_state.is_generating = True
        st.session_state.generation_stopped = False
    else:
        st.session_state.button_state = "Generate"
        st.session_state.is_generating = False
        st.session_state.generation_stopped = True

st.title(f"MySQL with Model {model_llama}")

# Menambahkan sidebar untuk informasi model
with st.sidebar:
    st.info("Using Llama 3.1 (8B) Model")
    if st.checkbox("Show Model Info"):
        st.write("Model: Llama 3.1 8B")
        st.write("Max Tokens: 4096")
        st.write("Temperature: 0.7")

# Menggunakan text_area untuk input
prompt = st.text_area("Enter your prompt:", height=100, key="prompt_input")

# Create columns for the toggle button
col1, col2 = st.columns([1, 5])
with col1:
    # Dynamic toggle button
    if st.button(
        st.session_state.button_state,
        key="toggle_button",
        type="primary",
        on_click=handle_button_click
    ):
        pass

# Response placeholder
response_placeholder = st.empty()

# Handle generation process
if st.session_state.is_generating and not st.session_state.generation_stopped and prompt:
    # Thread-safe flag using a list (mutable object)
    stopped_flag = [False]
    
    # Start generation in a separate thread
    generation_thread = threading.Thread(
        target=generate_response,
        args=(prompt, stopped_flag, st.session_state.response_queue)
    )
    generation_thread.start()
    
    # Show spinner while generating
    with st.spinner("Generating response..."):
        while generation_thread.is_alive():
            if st.session_state.generation_stopped:
                stopped_flag[0] = True  # Set thread-safe stop flag
                st.warning("Generation stopped by user.")
                st.session_state.button_state = "Generate"
                time.sleep(0.1)  # Give thread time to clean up
                st.rerun()
                break
            time.sleep(0.1)
    
    # Check for results if not stopped
    if not stopped_flag[0] and not st.session_state.response_queue.empty():
        result_type, result_content = st.session_state.response_queue.get()
        if result_type == "success":
            response_placeholder.write(result_content)
        else:
            st.error(f"Error occurred: {result_content}")
            st.info("Make sure Ollama is running and the model is properly installed.")
    
    # Reset states after completion
    st.session_state.button_state = "Generate"
    st.session_state.is_generating = False
    st.session_state.response_queue.queue.clear()  # Clear queue for next run
    st.rerun()

# Menambahkan JavaScript untuk mendeteksi Ctrl+Enter
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        const textArea = document.querySelector('textarea');
        if (textArea && textArea.value.trim()) {
            const buttons = document.getElementsByTagName('button');
            for (let button of buttons) {
                if (button.innerText === 'Generate') {
                    button.click();
                    break;
                }
            }
        }
    }
});
</script>
""", unsafe_allow_html=True)

# Menambahkan petunjuk penggunaan
st.markdown("""
---
### Tips Penggunaan:
- Ketik prompt Anda di area teks di atas
- Klik tombol "Generate" atau tekan **Ctrl+Enter** untuk memulai proses
- Tombol akan berubah menjadi "Stop" selama proses berlangsung
- Klik "Stop" untuk membatalkan proses generate
- Gunakan area teks yang lebih besar untuk prompt yang panjang
""")