import streamlit as st
from sqlalchemy import create_engine, text

# 1. Inisialisasi Koneksi
def init_connection():
    user = st.secrets["tidb"]["user"]
    password = st.secrets["tidb"]["password"]
    host = st.secrets["tidb"]["host"]
    port = st.secrets["tidb"]["port"]
    database = st.secrets["tidb"]["database"]
    
    conn_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?ssl_verify_cert=true"
    return create_engine(conn_url, pool_pre_ping=True)

engine = init_connection()

# 2. UI Halaman Input
st.title("📝 Input Data Mahasiswa")
st.subheader("Tambah data baru ke database TiDB")

# Membuat form input
with st.form("form_mahasiswa", clear_on_submit=True):
    nama = st.text_input("Nama Lengkap")
    jurusan = st.selectbox("Jurusan", ["Teknik Informatika", "Sistem Informasi", "Data Science", "Manajemen"])
    usia = st.number_input("Usia", min_value=15, max_value=60, value=20)
    
    submit_button = st.form_submit_button("Simpan ke Database")

# 3. Logika Simpan Data (INSERT)
if submit_button:
    if nama: # Validasi sederhana agar nama tidak kosong
        try:
            with engine.connect() as conn:
                # Menyiapkan query SQL
                query = text("INSERT INTO mahasiswa (nama, jurusan, usia) VALUES (:n, :j, :u)")
                
                # Eksekusi dengan parameter (aman dari SQL Injection)
                conn.execute(query, {"n": nama, "j": jurusan, "u": usia})
                conn.commit() # Penting untuk menyimpan perubahan
                
                st.success(f"Data {nama} berhasil disimpan!")
        except Exception as e:
            st.error(f"Gagal menyimpan data: {e}")
    else:
        st.warning("Mohon isi nama terlebih dahulu.")

# 4. Preview Data (Opsional)
st.divider()
st.subheader("📊 Data Terdaftar")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM mahasiswa ORDER BY id DESC LIMIT 5"))
        for row in result:
            st.write(f"ID: {row.id} | Nama: {row.nama} | Jurusan: {row.jurusan} ({row.usia} thn)")
except Exception as e:
    st.info("Tabel mungkin belum dibuat. Pastikan Anda sudah menjalankan perintah CREATE TABLE di dashboard TiDB.")
