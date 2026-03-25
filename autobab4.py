import streamlit as st
from openai import OpenAI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AutoBab4 - Olah Data Cepat", page_icon="🎓", layout="centered")

# --- KUNCI BRANKAS OPENAI (SINTAKS VERSI TERBARU) ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==========================================
# --- SISTEM GEMBOK PASSWORD CEO ---
# ==========================================
PASSWORD_HARIAN = "LULUSCEPAT"  
PASSWORD_VIP = "VIPBAB4"        

st.title("🎓 Mesin AutoBab4 - Olah Data Cepat")
st.markdown("Masukkan data penelitian kamu di bawah ini, dan biarkan AI menyusun paragraf pembahasan Bab 4 kamu secara instan!")
st.markdown("---")

input_pass = st.text_input("🔑 Masukkan Password Akses:", type="password")

if input_pass != PASSWORD_HARIAN and input_pass != PASSWORD_VIP:
    st.warning("🔒 Aplikasi terkunci. Silakan masukkan password yang valid.")
    st.info("💡 Belum punya password? Beli akses Premium di link bio TikTok / Lynk.id sekarang!")
    st.stop() 
# ==========================================
# --- BATAS GEMBOK ---
# ==========================================

st.success("🔓 Akses Diberikan! Selamat menggunakan AutoBab4.")

# --- FORM INPUT DATA MAHASISWA ---
col1, col2 = st.columns(2)
with col1:
    variabel_x = st.text_input("Variabel Independen (X)", placeholder="Contoh: Kualitas Layanan")
    p_value = st.number_input("Nilai P-Value / Sig.", format="%.3f", value=0.000)
with col2:
    variabel_y = st.text_input("Variabel Dependen (Y)", placeholder="Contoh: Kepuasan Pelanggan")
    arah_hubungan = st.selectbox("Arah Hubungan", ["Positif", "Negatif"])

# DIUBAH JADI TEXT_AREA BIAR BISA BANYAK
teori = st.text_area("Grand Theory / Ahli yang Digunakan (Bisa lebih dari 1)", placeholder="1. Kotler & Keller (2016)\n2. Tjiptono (2019)")

st.markdown("**Pemetaan Penelitian Terdahulu:**")
jurnal_sejalan = st.text_area("Jurnal yang SEJALAN (Bisa lebih dari 1)", placeholder="1. Pratama (2022)\n2. Budi (2021)")
jurnal_berbeda = st.text_area("Jurnal yang BERBEDA (Opsional, Bisa lebih dari 1)", placeholder="1. Wijaya (2021)\nKosongkan jika tidak ada")

# --- TOMBOL GENERATE & LOGIKA AI ---
if st.button("🚀 GENERATE PEMBAHASAN SEKARANG!", use_container_width=True):
    if not variabel_x or not variabel_y or not teori:
        st.error("⚠️ Variabel X, Y, dan Teori wajib diisi!")
    else:
        with st.spinner("⏳ AI sedang menyusun paragraf pembahasan yang elegan..."):
            try:
                status_hipotesis = "DITERIMA (Signifikan)" if p_value < 0.05 else "DITOLAK (Tidak Signifikan)"

                prompt_system = f"""
                Kamu adalah Dosen Pembimbing Skripsi ahli statistik dan manajemen yang sangat cerdas. 
                Tugasmu adalah menulis 3 paragraf Pembahasan (Bab 4) berdasarkan data berikut:
                - Variabel X: {variabel_x}
                - Variabel Y: {variabel_y}
                - Nilai P-Value: {p_value} (Status: {status_hipotesis})
                - Arah Hubungan: {arah_hubungan}
                - Grand Theory: {teori}
                - Jurnal Sejalan: {jurnal_sejalan}
                - Jurnal Berbeda: {jurnal_berbeda}

                ATURAN PENULISAN:
                - Paragraf 1: Jelaskan makna statistik p-value. Jika < 0.05, hipotesis diterima dan X berpengaruh terhadap Y. Jika > 0.05, hipotesis ditolak dan X tidak berpengaruh. Jelaskan juga arah hubungannya ({arah_hubungan}).
                - Paragraf 2: Berikan alasan logis/praktis di lapangan MENGAPA hasil ini terjadi. 
                  * JIKA DITOLAK: Berikan alasan "ngeles" yang akademis kenapa X tidak mempengaruhi Y.
                  * JIKA NEGATIF: Berikan alasan logis kenapa semakin tinggi X justru membuat Y menurun.
                  Kaitkan alasan praktis ini dengan grand theory.
                - Paragraf 3: Bandingkan dengan penelitian terdahulu. Nyatakan sejalan dengan jurnal sejalan. Jika jurnal berbeda diisi, sebutkan bahwa hasil ini berbeda dengan penelitian tersebut dan berikan alasan perbedaan (misal beda sampel/karakteristik). Jika jurnal berbeda kosong, buat kalimat penutup yang elegan.
                
                Langsung berikan 3 paragraf tanpa kata pengantar atau penutup tambahan. Gunakan bahasa akademis formal yang rapi.
                """

                # SINTAKS OPENAI VERSI TERBARU
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Anda adalah asisten AI pembuat pembahasan skripsi."},
                        {"role": "user", "content": prompt_system}
                    ],
                    temperature=0.7
                )
                
                hasil = response.choices[0].message.content
                st.success("✅ Pembahasan Berhasil Dibuat!")
                st.write(hasil)
            
            except Exception as e:
                st.error(f"Terjadi kesalahan sistem: {e}")
