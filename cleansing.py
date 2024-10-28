import pandas as pd
import numpy as np
from datetime import datetime

# Create sample messy data
data = pd.read_csv('.../PotensiMB.csv',
                   delim_whitespace=True,  # This handles multiple spaces
                        skipinitialspace=True,  # Skip spaces at the start of fields
                        error_bad_lines=False,  # Skip problematic lines
                        warn_bad_lines=True)

# Create DataFrame
df = pd.DataFrame(data)

print("=== ORIGINAL DATA ANALYSIS ===")
print("\n1. First 5 rows of original data:")
print(df.head())

print("\n2. Data Info (types and non-null counts):")
print(df.info())

print("\n3. Basic statistics of original data:")
print(df.describe(include='all'))

print("\n4. Missing values in each column:")
print(df.isnull().sum())

def clean_date_format(date_val):
    """
    Membersihkan format tanggal dari berbagai format input menjadi YYYY-MM-DD
    
    Parameters:
    date_val: Input tanggal (bisa string atau numeric)
    
    Returns:
    str: Tanggal dalam format YYYY-MM-DD
    """
    try:
        # Konversi ke string dan pastikan panjangnya 8 digit
        date_str = str(int(date_val))
        if len(date_str) != 8:
            return None
            
        # Ekstrak tahun, bulan, dan hari
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:]
        
        # Validasi nilai tanggal
        if not (1900 <= int(year) <= 2100 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            return None
            
        # Format ulang menjadi YYYY-MM-DD
        return f"{year}-{month}-{day}"
    except:
        return None
    
# Now let's clean the data
def clean_data(df):
    df_clean = df.copy()
    
    # Clean customer_id
    # Kombinasi terbaik dari kedua pendekatan
    df_clean['no_cif'] = df_clean['no_cif'].astype(str)  # Konversi ke string
    df_clean['no_cif'] = df_clean['no_cif'].str.strip()  # Bersihkan spasi
    df_clean.loc[df_clean['no_cif'] == 'nan', 'no_cif'] = 'UNKNOWN'  # Tangani 'nan'

    df_clean['recuco'] = df_clean['recuco'].astype(str)  # Konversi ke string
    df_clean['recuco'] = df_clean['recuco'].str.strip()  # Bersihkan spasi
    df_clean.loc[df_clean['recuco'] == 'nan', 'recuco'] = 'UNKNOWN'  # Tangani 'nan'

    df_clean['nama'] = df_clean['nama'].str.strip()
    df_clean['nama'] = df_clean['nama'].fillna('UNKNOWN')
    
    # Clean purchase_date
    # Terapkan fungsi ke DataFrame
    df_clean['tanggal_lahir'] = df_clean['tanggal_lahir'].apply(clean_date_format)
    df_clean['tanggal_lahir'] = pd.to_datetime(df_clean['tanggal_lahir'])

    # Clean price
    df_clean['usia'] = pd.to_numeric(df_clean['usia'], errors='coerce')
    df_clean['usia'] = df_clean['usia'].fillna(df_clean['usia'].median())
    
     # Clean email
    df_clean['email'] = df_clean['email'].str.lower()
    df_clean['email'] = df_clean['email'].fillna('unknown@email.com')

    # Clean product_name
    df_clean['no_hp'] = df_clean['no_hp'].str.strip()
    df_clean['no_hp'] = df_clean['no_hp'].fillna('Unknown Product')
    
    # Kombinasi terbaik dari kedua pendekatan
    df_clean['pekerjaan'] = df_clean['pekerjaan'].astype(str)  # Konversi ke string
    df_clean['pekerjaan'] = df_clean['pekerjaan'].str.strip()  # Bersihkan spasi
    df_clean.loc[df_clean['pekerjaan'] == 'nan', 'pekerjaan'] = 'UNKNOWN'  # Tangani 'nan'

    df_clean['jenis_produk'] = df_clean['jenis_produk'].str.strip()
    df_clean['jenis_produk'] = df_clean['jenis_produk'].fillna('UNKNOWN')

     # Clean price
    df_clean['usia'] = pd.to_numeric(df_clean['usia'], errors='coerce')
    df_clean['usia'] = df_clean['usia'].fillna(df_clean['usia'].median())
    
    # Clean quantity
    df_clean['no_rekening'] = pd.to_numeric(df_clean['no_rekening'], errors='coerce')
    df_clean['no_rekening'] = df_clean['no_rekening'].fillna(1)
    df_clean.loc[df_clean['no_rekening'] < 0, 'no_rekening'] = 1
    
    # Clean quantity
    df_clean['kode_cabang'] = df_clean['kode_cabang'].astype(str)
    df_clean['kode_cabang'] = df_clean['kode_cabang'].str.strip()
   
    df_clean['nama_cabang'] = df_clean['nama_cabang'].str.strip()
    df_clean['nama_cabang'] = df_clean['nama_cabang'].fillna('UNKNOWN')
    
    # Clean quantity
    df_clean['kode_cabang2'] = df_clean['kode_cabang2'].astype(str)
    df_clean['kode_cabang2'] = df_clean['kode_cabang2'].str.strip()

    df_clean['nama_cabang2'] = df_clean['nama_cabang2'].str.strip()
    df_clean['nama_cabang2'] = df_clean['nama_cabang2'].fillna('UNKNOWN')

    df_clean['kode_cabkor'] = df_clean['kode_cabkor'].astype(str)
    df_clean['kode_cabkor'] = df_clean['kode_cabkor'].str.strip()

# Clean product_name
    df_clean['no_kartu'] = df_clean['no_kartu'].str.strip()
    df_clean['no_kartu'] = df_clean['no_kartu'].str.title()
    df_clean['no_kartu'] = df_clean['no_kartu'].fillna('Unknown Product')

    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
   
    
    return df_clean

# Clean the data
df_cleaned = clean_data(df)

print("\n\n=== CLEANED DATA ANALYSIS ===")
print("\n1. First 5 rows of cleaned data:")
print(df_cleaned.head())

print("\n2. Cleaned Data Info (types and non-null counts):")
print(df_cleaned.info())

print("\n3. Basic statistics of cleaned data:")
print(df_cleaned.describe(include='all'))

print("\n4. Missing values in cleaned data:")
print(df_cleaned.isnull().sum())

print("\n5. Unique values in categorical columns:")
for col in ['nama',  'email']:
    print(f"\nUnique {col}s:")
    print(df_cleaned[col].unique())

#print("\n6. Summary statistics for numerical columns:")
#print(df_cleaned[['price', 'quantity', 'total_amount']].agg(['min', 'max', 'mean', 'median']))

# Display changes made
print("\n7. Changes made during cleaning:")
print(f"Original shape: {df.shape}")
print(f"Cleaned shape: {df_cleaned.shape}")
print(f"Duplicates removed: {len(df) - len(df_cleaned)}")

def save_cleaned_data(df_cleaned, base_filename='cleaned_mb_data'):
    """
    Save cleaned data to multiple formats
    """
    # 1. Save to CSV
    csv_file = f"{base_filename}.csv"
    df_cleaned.to_csv(csv_file, index=False)
    print(f"Saved CSV file: {csv_file}")

    # 2. Save to Excel
    excel_file = f"{base_filename}.xlsx"
    df_cleaned.to_excel(excel_file, index=False, sheet_name='Cleaned_Data')
    print(f"Saved Excel file: {excel_file}")

    # 3. Save to Pickle (for preserving data types)
    pickle_file = f"{base_filename}.pkl"
    df_cleaned.to_pickle(pickle_file)
    print(f"Saved Pickle file: {pickle_file}")

    # 4. Save to JSON
    json_file = f"{base_filename}.json"
    df_cleaned.to_json(json_file, orient='records')
    print(f"Saved JSON file: {json_file}")

    # Create a summary file
    with open(f"{base_filename}_summary.txt", 'w') as f:
        f.write("=== DATA CLEANING SUMMARY ===\n\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Total rows: {len(df_cleaned)}\n")
        f.write(f"Total columns: {len(df_cleaned.columns)}\n")
        f.write("\nColumns:\n")
        for col in df_cleaned.columns:
            f.write(f"- {col}\n")
        f.write("\nData types:\n")
        for col, dtype in df_cleaned.dtypes.items():
            f.write(f"- {col}: {dtype}\n")

# Save the cleaned data
save_cleaned_data(df_cleaned)

print("\nAll files have been saved successfully!")
