import streamlit as st
from langchain_community.llms import Ollama
from fpdf import FPDF
import json
import re
from datetime import datetime, timedelta

# --- KONFIGURASI MODEL ---
# Pakai llama3 atau phi3 (sesuai yang kamu download di Ollama)
llm = Ollama(model="phi3:latest") 

# --- FUNGSI LOGIKA ---
def parse_ai_output(response_text):
    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def generate_pdf(data, results, is_bypass=False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BERITA ACARA VERIFIKASI PROPOSAL PENELITIAN", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="L&D Department", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="A. DETAIL PENELITIAN", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=f"Judul: {data['judul']}\nStakeholder: {data['stakeholder']}\nWaktu: {data['waktu']}")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="B. HASIL EVALUASI AI", ln=True)
    pdf.set_font("Arial", size=11)
    
    if is_bypass:
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(0, 8, txt="STATUS: APPROVED (BYPASS ADMIN)\nCatatan: Disetujui melalui jalur khusus manajemen.")
    else:
        for key, val in results.items():
            if "skor" in key:
                pdf.cell(0, 8, txt=f"- {key.replace('_', ' ').title()}: {val}%", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 8, txt=f"Kesimpulan: {results.get('saran_perbaikan', 'Lolos verifikasi.')}")

    return pdf.output(dest='S').encode('latin-1')

# --- UI STREAMLIT ---
st.set_page_config(page_title="L&D Research Curator", layout="wide", page_icon="🛡️")

st.title("🛡️ Research Curator AI")
st.info("Sistem ini akan memvalidasi proposal Anda secara otomatis. Skor minimal untuk lolos adalah 95%.")

# Form Input
with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        judul = st.text_input("Judul Penelitian")
        luaran = st.text_area("Luaran (Contoh: Rekomendasi kebijakan, bukan kewajiban ganti sistem)")
        data_req = st.text_area("Data yang Dibutuhkan (Sebutkan secara spesifik)")
    with col2:
        stakeholder = st.text_input("Stakeholder/Sampel (Contoh: Karyawan Produksi)")
        waktu_mulai = st.date_input("Rencana Mulai", min_value=datetime.now().date())
        instrumen = st.text_area("Daftar Pertanyaan Penelitian")
    
    btn_analisis = st.form_submit_button("Analisis Sensitivitas Proposal")

# --- PROSES ANALISIS ---
if btn_analisis:
    # Cek durasi waktu (Min 3 minggu)
    diff = waktu_mulai - datetime.now().date()
    
    if any(boss in stakeholder.lower() for boss in ["ceo", "direktur", "komisaris", "founder"]):
        st.error("❌ PENOLAKAN OTOMATIS: Stakeholder Top Management tidak boleh dilibatkan.")
    elif diff.days < 21:
        st.error(f"❌ PENOLAKAN OTOMATIS: Waktu terlalu mepet. Minimal 21 hari (Kurang {21 - diff.days} hari lagi).")
    else:
        with st.spinner("AI sedang membedah instrumen Anda..."):
            prompt = f"""
            Berperanlah sebagai Kurator L&D yang galak. Analisis data proposal ini.
            Aturan: Data gaji/rahasia=Skor 0. Luaran maksa=Skor 0. Instrumen jelek-jelekin kantor=Skor 0.
            
            INPUT:
            Judul: {judul} | Luaran: {luaran} | Data: {data_req} | Stakeholder: {stakeholder} | Instrumen: {instrumen}

            OUTPUT DALAM JSON:
            {{
                "skor_judul": 0-100, "skor_luaran": 0-100, "skor_data": 0-100, 
                "skor_stakeholder": 0-100, "skor_instrumen": 0-100,
                "avg_score": 0-100, "saran_perbaikan": "..."
            }}
            """
            raw_ai = llm.invoke(prompt)
            hasil = parse_ai_output(raw_ai)
            
            if hasil:
                avg = hasil.get('avg_score', 0)
                if avg >= 95:
                    st.success(f"✅ SKOR: {avg}% - PROPOSAL AMAN!")
                    pdf_bytes = generate_pdf({"judul":judul, "stakeholder":stakeholder, "waktu":waktu_mulai}, hasil)
                    st.download_button("Download Berita Acara (PDF)", data=pdf_bytes, file_name="Verifikasi_LND_Clear.pdf")
                else:
                    st.error(f"⚠️ SKOR: {avg}% - PERLU REVISI")
                    st.write(f"**Alasan AI:** {hasil.get('saran_perbaikan')}")
                    # Tampilkan detail skor agar user tahu mana yang harus diperbaiki
                    st.json(hasil)
            else:
                st.warning("AI memberikan format yang salah, coba klik analisis lagi.")