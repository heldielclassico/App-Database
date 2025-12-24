import streamlit as st
from sqlalchemy import create_engine, text

def init_connection():
    # Mengambil kredensial dari secrets
    user = st.secrets["tidb"]["user"]
    password = st.secrets["tidb"]["password"]
    host = st.secrets["tidb"]["host"]
    port = st.secrets["tidb"]["port"]
    database = st.secrets["tidb"]["database"]
    
    # URL Koneksi (Menggunakan PyMySQL sebagai driver)
    # Tanpa 'https://' dan menambahkan SSL argumen untuk TiDB
    conn_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?ssl_verify_cert=true"
    
    return create_engine(conn_url, pool_pre_ping=True)

engine = init_connection()

st.title("Aplikasi TiDB Cloud")

# Contoh Query untuk Testing
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW();"))
        for row in result:
            st.success(f"Koneksi Berhasil! Waktu Server: {row[0]}")
except Exception as e:
    st.error(f"Error: {e}")
