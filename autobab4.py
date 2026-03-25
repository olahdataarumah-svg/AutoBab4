import streamlit as st
from openai import OpenAI

# ==========================================
# 1. TARUH API KEY LU DI SINI COACH!
# ==========================================
API_KEY = st.secrets["OPENAI_API_KEY"] 

# ==========================================
# 2. TAMPILAN WEB (USER INTERFACE)
# ==========================================
st.set_page_config(page_title="AutoBab4 - Olah Data Cepat", page_icon="🔥", layout="centered")

st.title("🔥 Mesin AutoBab4")
st.markdown("**Generator Pembahasan Bab 4 Otomatis by Olah Data Cepat**")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    var_x = st.text_input("Variabel Independen (X)", placeholder="Contoh: Kualitas Layanan")
    var_y = st.text_input("Variabel Dependen (Y)", placeholder="Contoh: Kepuasan Pelanggan")
    teori = st.text_area("Grand Theory / Ahli", placeholder="Contoh: 1. Kotler (2019)\n2. Tjiptono (2020)")
    
with col2:
    p_value = st.text_input("Nilai P-Value / Sig.", placeholder="Contoh: 0.001")
    arah_pengaruh = st.selectbox("Arah Hubungan", ["Positif", "Negatif"])
    kesimpulan = st.selectbox("Status Hipotesis", ["DITERIMA (Signifikan)", "DITOLAK (Tidak Signifikan)"])

st.markdown("---")
st.markdown("**📚 PEMETAAN PENELITIAN TERDAHULU**")
col3, col4 = st.columns(2)

with col3:
    penelitian_sejalan = st.text_area("Jurnal yang SEJALAN (Hasilnya Sama)", placeholder="Contoh: Budi (2021)")
with col4:
    penelitian_tidak_sejalan = st.text_area("Jurnal yang BERBEDA (Hasilnya Beda)", placeholder="Contoh: Andi (2022)")

st.markdown("---")

# ==========================================
# 3. TOMBOL EKSEKUSI & LOGIKA AI
# ==========================================
if st.button("🚀 GENERATE PEMBAHASAN SEKARANG!", use_container_width=True):
    if not var_x or not var_y or not p_value:
        st.warning("⚠️ Woy! Isi dulu variabel dan p-value nya Coach!")
    else:
        with st.spinner("🧠 AI lagi mikir keras ngerangkai kata-kata..."):
            try:
                # PROMPT SAKTI: ADAPTASI 2 KOLOM JURNAL
                prompt_sakti = f"""
                Bertindaklah sebagai Dosen Pembimbing Akademik yang ahli menyusun kalimat Bab 4 Skripsi Kuantitatif. 
                Tuliskan 3 paragraf pembahasan Bab 4 yang sangat akademis, mengalir, dan anti-plagiasi berdasarkan data berikut:
                - Variabel Independen (X): {var_x}
                - Variabel Dependen (Y): {var_y}
                - Nilai P-Value: {p_value}
                - Hasil Uji: Hipotesis {kesimpulan} dengan arah hubungan {arah_pengaruh}.
                - Grand Theory: {teori}
                - Penelitian Terdahulu (SEJALAN dengan hasil): {penelitian_sejalan}
                - Penelitian Terdahulu (TIDAK SEJALAN dengan hasil): {penelitian_tidak_sejalan}
                
                ATURAN PENULISAN (HARUS DIIKUTI):
                - Paragraf 1: Interpretasi hasil uji statistik. Sebutkan nilai p-value dan dampaknya secara tegas terhadap penerimaan/penolakan hipotesis.
                - Paragraf 2: Berikan argumentasi praktis yang KONKRET dan LOGIS di dunia nyata. Jelaskan argumen logis mengapa [{var_x}] bisa (atau gagal) mempengaruhi [{var_y}] sesuai dengan hasil uji. Berikan contoh dinamika di lapangan yang relevan.
                - Paragraf 3: Justifikasi Ilmiah. Susun narasi yang membandingkan hasil temuan ini dengan Grand Theory ({teori}) dan Penelitian Terdahulu. 
                  * Jika ada data di "Penelitian Terdahulu (SEJALAN)", tegaskan bahwa temuan ini MENDUKUNG/MEMPERKUAT penelitian tersebut.
                  * Jika ada data di "Penelitian Terdahulu (TIDAK SEJALAN)", sebutkan secara akademis bahwa temuan ini BERBEDA/MEMBANTAH penelitian tersebut, dan berikan sedikit opini akademis wajar mengapa perbedaan ini bisa terjadi (misal beda karakteristik sampel atau waktu).
                  * Jika salah satu dari bagian penelitian terdahulu kosong, abaikan saja dan fokus pada yang ada isinya secara natural.
                
                PENTING: Tulis langsung narasinya menjadi 3 paragraf utuh. Jangan gunakan bullet points. Jangan mengulang instruksi prompt!
                """

                client = OpenAI(api_key=API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt_sakti}
                    ]
                )
                
                hasil_bab4 = response.choices[0].message.content
                
                st.success("🎉 BERHASIL! Copy teks di bawah ini ke Word:")
                st.info(hasil_bab4)
                
            except Exception as e:
                st.error(f"❌ Error bro: {e}")