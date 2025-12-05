import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image
import os
from datetime import datetime

st.set_page_config(page_title="Aplikasi Absensi Online", layout="wide")

st.title("📋 Aplikasi Absensi Online")
st.write("Silakan isi absensi dengan data yang benar.")

# ---------------------------
# 1. INPUT FORM
# ---------------------------
nama = st.text_input("Nama Lengkap")
nim = st.text_input("NIM / ID")
kehadiran = st.selectbox("Kehadiran", ["Hadir", "Izin", "Sakit", "Alfa"])

# Tombol simpan
if st.button("Simpan Data"):
    if nama == "" or nim == "":
        st.error("Nama dan NIM tidak boleh kosong.")
    else:
        # Simpan ke Excel
        file_excel = "absensi.xlsx"

        # Jika file belum ada, buat baru
        if not os.path.exists(file_excel):
            df = pd.DataFrame(columns=["Tanggal", "Nama", "NIM", "Kehadiran"])
            df.to_excel(file_excel, index=False)

        # Baca file
        df = pd.read_excel(file_excel)

        # Tambahkan data baru
        data_baru = {
            "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nama": nama,
            "NIM": nim,
            "Kehadiran": kehadiran,
        }

        df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)

        # Simpan lagi
        df.to_excel(file_excel, index=False)

        st.success("Data berhasil disimpan!")

# ---------------------------
# 2. TAMPILKAN DATA ABSENSI
# ---------------------------
st.subheader("📊 Data Absensi")
if os.path.exists("absensi.xlsx"):
    df = pd.read_excel("absensi.xlsx")
    st.dataframe(df)
else:
    st.info("Belum ada data yang tersimpan.")

# ---------------------------
# 3. QR CODE GENERATOR
# ---------------------------
st.subheader("🎫 Generate QR Code Absensi")

qr_text = st.text_input("Teks QR (misal: link absensi atau ID)")

if st.button("Buat QR Code"):
    if qr_text == "":
        st.error("Teks QR tidak boleh kosong.")
    else:
        qr = qrcode.make(qr_text)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        st.image(buffer.getvalue(), caption="QR Code")

        st.download_button(
            label="Download QR Code",
            data=buffer.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )
