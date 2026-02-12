# 🛡️ L&D RESEARCH CURATOR AI
### **CMM Group - Digital Integrity & Screening System**

Sistem ini adalah **Legacy Project** yang dirancang untuk mengotomatisasi proses **filter awal** proposal penelitian. Tujuannya adalah memastikan setiap riset yang masuk tidak mengekspos **data sensitif** perusahaan.

---

## 🌟 FITUR UTAMA

* **AI Automated Scoring:** Melakukan penilaian mendalam pada 5 poin utama: **Judul, Luaran, Data, Stakeholder, dan Instrumen.**
* **Threshold Ketat (95%):** Hanya proposal dengan tingkat keamanan **minimal 95%** yang bisa lolos. Kurang dari itu? **Wajib Revisi!**
* **Security Policy Hard-Coded:**
    * **Stakeholder:** Otomatis **MENOLAK** jika melibatkan **CEO, Direktur, Komisaris, atau Founder**.
    * **Timeline:** Otomatis **MENOLAK** jika pengajuan kurang dari **21 hari (3 minggu)** sebelum mulai.
* **Auto-PDF Generation:** Menghasilkan **Berita Acara Verifikasi** resmi dalam format PDF sebagai bukti lolos kurasi AI.

---

## 🛠️ PANDUAN INSTALASI (SETUP CEPAT)

Agar sistem ini berjalan di komputer baru, ikuti langkah-langkah **WAJIB** ini:

1.  **Install Python:** Pastikan **Python 3.10** ke atas sudah terinstal di Windows.
2.  **Install Ollama:** Download di [ollama.com](https://ollama.com) dan jalankan model dengan perintah di terminal:
    > `ollama run phi3`
3.  **Install Dependencies:** Buka terminal di folder project ini dan ketik:
    > `pip install -r requirements.txt`

---

## 🚀 CARA MENJALANKAN APLIKASI

Ikuti urutan ini agar tidak terjadi *error*:

1.  **Buka Aplikasi Ollama** (Pastikan ikon gajah muncul di taskbar pojok kanan bawah).
2.  **Buka Terminal** di folder project: `D:\LnD Hana Rohadah\Penelitian`.
3.  **Jalankan Perintah Utama:**
    > **`python -m streamlit run app.py`**
4.  Aplikasi akan terbuka otomatis di browser pada alamat **`http://localhost:8501`**.

---

## 📜 FILOSOFI SISTEM (WAJIB DIBACA PENGGANTI)

> **"Sistem ini diciptakan untuk menjaga kerahasiaan dapur CMM Group."**
> 
> Jika peneliti mengeluh karena skornya rendah, mintalah mereka membaca **Saran Perbaikan** yang diberikan AI secara detail. Jangan memberikan verifikasi manual jika AI belum memberikan lampu hijau (**Clear 95%**), karena risiko kebocoran data menjadi tanggung jawab penuh tim L&D.

---
**Developed by: Hana Rohadah (L&D Department)**
