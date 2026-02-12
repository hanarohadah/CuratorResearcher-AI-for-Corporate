🛡️ L&D Research Curator AI
Security & Integrity Screening System

Sistem ini dikembangkan untuk melakukan kurasi otomatis terhadap proposal penelitian yang masuk ke departemen L&D. Menggunakan kecerdasan buatan (Local LLM) untuk memastikan setiap instrumen dan data yang diminta tidak melanggar sensitivitas atau rahasia perusahaan.

🚀 Fitur Utama
AI Validation: Melakukan skoring otomatis (0-100%) terhadap 5 poin krusial (Judul, Luaran, Data, Stakeholder, Instrumen).

Safety Threshold: Hanya proposal dengan skor rata-rata di atas 95% yang dapat lanjut ke tahap verifikasi manusia.

Auto-PDF: Menghasilkan Berita Acara Verifikasi secara otomatis jika proposal dinyatakan "Aman".

Hard-Coded Policy: Penolakan otomatis untuk keterlibatan Top Management (CEO/Direktur) dan pengajuan di bawah H-21 hari.

🛠️ Cara Menjalankan (Untuk Admin)
1. Pastikan Mesin AI Aktif
Buka aplikasi Ollama di komputer, atau buka Terminal/CMD dan pastikan model sudah terunduh:

Bash
ollama run phi3
2. Jalankan Aplikasi
Buka Terminal di folder project, lalu ketik perintah berikut:

Bash
python -m streamlit run app.py
3. Akses Web
Buka browser dan masuk ke alamat: http://localhost:8501

📦 Prasyarat (Requirements)
Jika menjalankan di komputer baru, pastikan sudah menginstal:

Python 3.10+

Ollama AI Engine

Library Python (Instal via pip install -r requirements.txt)

📝 Catatan Penting
"Sistem ini dirancang untuk menjaga integritas data perusahaan. Jika AI memberikan skor di bawah 95%, peneliti WAJIB melakukan revisi mandiri pada poin-poin yang disebutkan oleh AI sebelum meminta verifikasi manual ke tim L&D."
