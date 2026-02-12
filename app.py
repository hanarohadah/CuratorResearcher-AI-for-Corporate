import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from fpdf import FPDF
import json
import re
from datetime import datetime

# --- KONFIGURASI MODEL ---
# Mengambil API Key dari Streamlit Secrets (Aman untuk GitHub)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
except Exception as e:
    st.error("Konfigurasi API Key belum ditemukan di Streamlit Secrets.")
    st.stop()

# --- FUNGSI LOGIKA ---
def parse_ai_output(response_text):
    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def generate_pdf(data, results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BERITA ACARA VERIFIKASI PROPOSAL PENELITIAN", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="L&D Department - CMM Group", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="A. DETAIL PENELITIAN", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=f"Judul: {data['judul']}\nStakeholder: {data['stakeholder']}\nWaktu: {data['waktu']}")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="B. HASIL EVALUASI AI", ln=True)
    pdf.set_font("Arial", size=11)
    
    for key, val in results.items():
        if "skor" in key:
            pdf.cell(0, 8, txt=f"- {key.replace('_', ' ').title()}: {val}%", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 8, txt=f"Kesimpulan: {results.get('saran_perbaikan', 'Lolos verifikasi.')}")

    return pdf.output(dest='S').encode('latin-1')

# --- UI STREAMLIT ---
st.set_page_config(page_title="L&D Research Curator", layout="wide", page_icon="🛡️")

st.title("🛡️ Research Curator AI - CMM Group")
st.info("Sistem kurasi otomatis proposal penelitian. Skor minimal untuk lolos: 95%.")

with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        judul = st.text_input("Judul Penelitian")
        luaran = st.text_area("Luaran Penelitian")
        data_req = st.text_area("Data yang Dibutuhkan")
    with col2:
        stakeholder = st.text_input("Stakeholder/Sampel")
        waktu_mulai = st.date_input("Rencana Mulai", min_value=datetime.now().date())
        instrumen = st.text_area("Daftar Pertanyaan Penelitian")
    
    btn_analisis = st.form_submit_button("Analisis Sensitivitas Proposal")

if btn_analisis:
    diff = waktu_mulai - datetime.now().date()
    
    if any(boss in stakeholder.lower() for boss in ["ceo", "direktur", "komisaris", "founder"]):
        st.error("❌ PENOLAKAN OTOMATIS: Stakeholder Top Management dilarang.")
    elif diff.days < 21:
        st.error(f"❌ PENOLAKAN OTOMATIS: Minimal H-21 pengajuan (Kurang {21 - diff.days} hari).")
    else:
        with st.spinner("AI Gemini sedang menganalisis keamanan data..."):
            prompt = f"""
            Berperanlah sebagai Kurator L&D Perusahaan yang ketat. Analisis data proposal ini:
            Judul: {judul} | Luaran: {luaran} | Data: {data_req} | Stakeholder: {stakeholder} | Instrumen: {instrumen}

            Aturan: Data gaji/strategi rahasia = skor 0. Pertanyaan menjelekkan kantor = skor 0.
            
            OUTPUT HARUS DALAM JSON:
            {{
                "skor_judul": 0-100, "skor_luaran": 0-100, "skor_data": 0-100, 
                "skor_stakeholder": 0-100, "skor_instrumen": 0-100,
                "avg_score": 0-100, "saran_perbaikan": "..."
            }}
            """
            response = llm.invoke(prompt)
            hasil = parse_ai_output(response.content)
            
            if hasil:
                avg = hasil.get('avg_score', 0)
                if avg >= 95:
                    st.success(f"✅ SKOR: {avg}% - PROPOSAL AMAN!")
                    pdf_bytes = generate_pdf({"judul":judul, "stakeholder":stakeholder, "waktu":waktu_mulai}, hasil)
                    st.download_button("Download Berita Acara (PDF)", data=pdf_bytes, file_name="Lolos_Kurasi_LD.pdf")
                else:
                    st.error(f"⚠️ SKOR: {avg}% - REVISI DIBUTUHKAN")
                    st.write(f"**Saran AI:** {hasil.get('saran_perbaikan')}")
                    st.json(hasil)
            else:
                st.warning("Terjadi kesalahan format AI, silakan coba lagi.")
