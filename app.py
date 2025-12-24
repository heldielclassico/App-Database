import streamlit as st
import mysql.connector

# Fungsi koneksi ke TiDB Cloud
from sqlalchemy import create_all, create_engine

def init_connection():
    # Format URL: mysql+pymysql://user:pass@host:port/db
    url = f"mysql+pymysql://{st.secrets['tidb']['user']}:{st.secrets['tidb']['password']}@{st.secrets['tidb']['host']}:{st.secrets['tidb']['port']}/{st.secrets['tidb']['database']}?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
    return create_engine(url)

engine = init_connection()
# Cara pakai: df = pd.read_sql("SELECT * FROM users", engine)
conn = init_connection()

# Query contoh
st.title("TiDB + Streamlit Connection")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    st.write(f"Nama: {row[1]}, Email: {row[2]}")
