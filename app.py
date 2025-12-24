import streamlit as st
import mysql.connector

# Fungsi koneksi ke TiDB Cloud
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["tidb"]["host"],
        port=st.secrets["tidb"]["port"],
        user=st.secrets["tidb"]["user"],
        password=st.secrets["tidb"]["password"],
        database=st.secrets["tidb"]["database"],
        autocommit=True,
        # Menggunakan ssl_disabled=False memastikan SSL aktif 
        # tanpa harus mencari file .pem secara manual
        ssl_disabled=False 
    )
conn = init_connection()

# Query contoh
st.title("TiDB + Streamlit Connection")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    st.write(f"Nama: {row[1]}, Email: {row[2]}")
