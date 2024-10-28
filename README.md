# PandasAI MySQL Chat Assistant

A Streamlit-based chat interface that allows users to query MySQL databases using natural language powered by PandasAI and Llama 3.1 LLM.

## 🌟 Features

- Natural language queries to MySQL database
- Interactive Streamlit interface
- Powered by Llama 3.1 (8B parameters) model
- Data cleaning and preprocessing capabilities
- Real-time response generation
- Stop/Generate functionality
- Keyboard shortcuts support

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- MySQL Server
- Ollama (for running Llama model)

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Llama model using Ollama:
```bash
ollama pull llama3.1:8b
```

### Database Setup

1. Create a MySQL database named `pandasai`
2. Configure your MySQL connection in `app.py`:
```python
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
```

### Data Cleaning

The project includes a data cleaning script (`cleansing.py`) that:
- Handles missing values
- Standardizes date formats
- Cleans text fields
- Removes duplicates
- Exports data in multiple formats (CSV, Excel, JSON, Pickle)

To clean your data:
```bash
python cleansing.py
```

## 🎮 Usage

1. Start the Ollama server:
```bash
ollama serve
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Access the application in your browser (typically `http://localhost:8501`)

### Using the Interface

1. Enter your query in the text area
2. Generate response either by:
   - Clicking the "Generate" button
   - Using the keyboard shortcut `Ctrl+Enter`
3. Stop generation at any time by clicking the "Stop" button
4. View model information in the sidebar

### Example Queries

- "Show me the total number of customers by branch"
- "What is the age distribution of our customers?"
- "List all products and their frequencies"

## 📁 Project Structure

```
├── app.py              # Main Streamlit application
├── cleansing.py        # Data cleaning script
├── requirements.txt    # Project dependencies
└── cache/             # Cache directory for PandasAI
```

## ⚙️ Configuration

### Model Configuration
```python
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="llama3.1:8b"
)
```

### PandasAI Configuration
```python
df_connector = SmartDataframe(
    my_connector, 
    config={
        "llm": model,
        "cache_path": "./cache",
        "enable_cache": True,
        "verbose": True
    }
)
```

## 🔑 Key Dependencies

- `pandasai[connectors]`: For natural language processing of data queries
- `streamlit`: For the web interface
- `numpy`: For numerical computations
- `PyYAML`: For configuration management
- `torch`, `torchvision`, `torchaudio`: For machine learning operations

## 💡 Tips

1. **Query Optimization**:
   - Be specific in your questions
   - Include relevant column names when possible
   - Start with simple queries and gradually increase complexity

2. **Performance**
