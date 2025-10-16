import pandas as pd
import os
from sqlalchemy import create_engine

# === 1. KONFIGURASI DATABASE ===
user = "postgres"
password = "123456"     # ganti dengan password PostgreSQL kamu
host = "localhost"
port = "5432"
database = "latsar"

# Buat koneksi dengan SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# === 2. LOKASI FILE CSV ===
folder_path = r"C:\Users\luluk\Documents\GitHub\Aktualisasi-Forecast\Data Observasi"

# Ambil semua file CSV di folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# === 3. GABUNG SEMUA CSV (JIKA ADA BEBERAPA) ===
df_list = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df_temp = pd.read_csv(file_path)
    df_temp['source_file'] = file  # optional: simpan nama file asal
    df_list.append(df_temp)

# Gabungkan semua CSV jadi satu dataframe
df_all = pd.concat(df_list, ignore_index=True)

print(f"✅ {len(csv_files)} file CSV berhasil digabung, total {len(df_all)} baris data.")
print("Preview data:")
print(df_all.head())

# === 4. SIMPAN KE DATABASE ===
table_name = "data_prediksi"   # nama tabel tujuan di PostgreSQL

df_all.to_sql(table_name, engine, index=False, if_exists="replace")
print(f"🎯 Data berhasil disimpan ke tabel '{table_name}' di database '{database}'.")