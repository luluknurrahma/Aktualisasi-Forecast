import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dashboard Pasang Surut Ketapang",
    page_icon="🌊",
    layout="wide"
)

# --- Fungsi untuk Memuat Data ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        return pd.read_excel(file_path)
    except Exception:
        return None

# --- Load Data ---
df_hist = load_data("Ketapang_Prediksi.xlsx")
df_forecast = load_data("Ketapang_Forecast.xlsx")

if df_hist is not None and df_forecast is not None:
    df_forecast = df_forecast.rename(columns={'time_forecast': 'time'})
    df_hist['time'] = pd.to_datetime(df_hist['time'])
    df_forecast['time'] = pd.to_datetime(df_forecast['time'])
    data = pd.merge(df_hist, df_forecast, on='time', how='outer')
elif df_hist is not None:
    df_hist['time'] = pd.to_datetime(df_hist['time'])
    data = df_hist
elif df_forecast is not None:
    df_forecast = df_forecast.rename(columns={'time_forecast': 'time'})
    df_forecast['time'] = pd.to_datetime(df_forecast['time'])
    data = df_forecast
else:
    data = None

# --- UI ---
if data is not None:
    data = data.set_index('time').sort_index()

    st.title("🌊 Tinggi Muka Air Laut - Ketapang")
    st.markdown("Dashboard interaktif untuk memvisualisasikan data pasang surut.")

    # --- Input Rentang Tanggal ---
    min_date = data.index.min().date()
    max_date = data.index.max().date()

    # default: 7 hari terakhir
    default_start = max_date - timedelta(days=7)
    default_end = max_date

    selected_range = st.date_input(
        "Pilih Rentang Tanggal:",
        value=(default_start, default_end),   # <-- tuple wajib date
        min_value=min_date,
        max_value=max_date
    )

    # Ambil start & end
    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        start_date, end_date = selected_range
    else:
        start_date, end_date = default_start, default_end

    # Filter data
    filtered_data = data.loc[
        (data.index.date >= start_date) & (data.index.date <= end_date)
    ]

    st.subheader(f"Data dari {start_date.strftime('%d %B %Y')} sampai {end_date.strftime('%d %B %Y')}")

    if filtered_data.empty:
        st.warning("Tidak ada data untuk rentang tanggal ini.")
    else:
        st.write("Pilih data yang ingin ditampilkan di grafik:")
        cols = st.columns(3)
        with cols[0]:
            show_observasi = st.checkbox("data_asli (Observasi)", value=True, key="obs")
        with cols[1]:
            show_prediksi = st.checkbox("prediksi_asli (Prediksi)", value=True, key="pred")
        with cols[2]:
            show_forecast = st.checkbox("prediksi_forecast (Forecast)", value=True, key="fore")

        columns_to_plot = []
        if show_observasi: columns_to_plot.append("data_asli")
        if show_prediksi: columns_to_plot.append("prediksi_asli")
        if show_forecast: columns_to_plot.append("prediksi_forecast")

        valid_columns = [
            col for col in columns_to_plot if col in filtered_data.columns and not filtered_data[col].dropna().empty
        ]

        if valid_columns:
            st.line_chart(filtered_data[valid_columns])
            if st.checkbox("Tampilkan Tabel Data Mentah untuk Rentang Terpilih"):
                st.dataframe(filtered_data[valid_columns].dropna(how='all'))
        else:
            st.info("Pilih setidaknya satu data yang tersedia.")
else:
    st.error("Gagal memuat file data. Pastikan file Excel tersedia di folder yang sama.")