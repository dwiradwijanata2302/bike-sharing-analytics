# 🚲 Bike Sharing Analytics Dashboard

Dashboard interaktif untuk menganalisis pola penyewaan sepeda berdasarkan
waktu, karakteristik pengguna, cuaca, musim, dan jenis hari. Proyek ini
dibangun menggunakan Python, Pandas, Plotly, dan Streamlit sebagai bagian
dari analisis data Bike Sharing.

> **Mulai cepat:** buka bagian [Menjalankan Dashboard](#menjalankan-dashboard)
> untuk menjalankan aplikasi secara lokal.

---

## ✨ Tentang Proyek

Dataset Bike Sharing berasal dari sistem Capital Bikeshare di Washington,
D.C., Amerika Serikat, dengan periode pengamatan 2011-2012. Data mencatat
penyewaan sepeda, waktu, kondisi cuaca, serta dua kelompok pengguna:

- **Casual:** pengguna kasual atau tidak terdaftar.
- **Registered:** pengguna terdaftar.

Dashboard menggunakan data per jam yang telah diperkaya dengan label tahun,
musim, cuaca, jenis hari, segmen waktu, serta satuan lingkungan yang lebih
mudah dibaca.

### Informasi analisis

| Komponen | Keterangan |
|---|---|
| Data harian pada notebook | 731 baris |
| Data per jam pada notebook/dashboard | 17.379 baris |
| Periode | 2011-2012 |
| Metrik utama | `cnt`, total penyewaan sepeda |
| Kelompok pengguna | `casual` dan `registered` |
| Sumber dashboard | `dashboard/main_data.csv` |

---

## 🧭 Cara Menggunakan Dashboard

Setelah aplikasi dibuka, ikuti alur berikut:

1. Gunakan **Filter Analisis** di sidebar.
2. Atur rentang tanggal, tahun, musim, kondisi cuaca, dan jenis hari.
3. Baca empat KPI pada bagian **Ringkasan Performa Penyewaan**.
4. Gunakan tombol navigasi di bawah ringkasan untuk berpindah halaman.
5. Ubah input simulator untuk melihat skenario yang berbeda.

### Halaman yang tersedia

#### 🏠 Overview

Halaman utama untuk melihat:

- Total penyewaan dan rata-rata penyewaan per jam.
- Jam puncak dan rata-rata penyewaan pada jam tersebut.
- Tren penyewaan harian dan bulanan.
- Pola penyewaan berdasarkan jam dan hari.
- Heatmap hari dan jam.
- Proporsi Casual dan Registered.
- Analisis musim, cuaca, serta lingkungan.
- Segmentasi intensitas penyewaan.
- Perbandingan hari kerja dan akhir pekan/libur.
- Ringkasan insight otomatis berdasarkan filter aktif.

#### 👥 Customer Analysis

Menganalisis perilaku pengguna melalui:

- Total dan proporsi Casual vs Registered.
- Pola penyewaan Casual dan Registered berdasarkan jam.
- Perbandingan perilaku menurut jenis hari.
- Simulasi hipotetis perpindahan sebagian Casual menjadi Registered.

Simulasi perpindahan pengguna hanya mengubah angka pada tampilan simulasi.
Dataset asli tidak diubah.

#### 🧪 Simulation Lab

Fitur **What-If Analysis** untuk menguji skenario perubahan permintaan:

- Slider perubahan permintaan dari `-50%` sampai `+50%`.
- Perbandingan baseline dan hasil simulasi.
- Selisih jumlah penyewaan.
- Grafik sebelum dan sesudah simulasi.
- Interpretasi otomatis berdasarkan nilai slider.

Perhitungan ini adalah skenario hipotetis berbasis data historis terfilter,
bukan prediksi aktual.

#### 📦 Capacity Planning

Membantu mengevaluasi jam yang berpotensi membutuhkan perhatian operasional:

- Slider untuk menentukan ambang kapasitas penyewaan per jam.
- Grafik rata-rata permintaan per jam.
- Garis ambang kapasitas.
- Jumlah jam yang melampaui ambang.
- Tabel detail jam yang melampaui ambang.

Dataset tidak menyediakan jumlah armada aktual. Karena itu, ambang kapasitas
di halaman ini adalah parameter simulasi manual, bukan kapasitas operasional
sebenarnya.

#### 🔎 Data Explorer

Menyediakan eksplorasi data yang sedang aktif:

- Tabel interaktif hasil filter global.
- Pemilihan kolom yang ingin ditampilkan.
- Statistik deskriptif numerik.
- Download hasil filter dalam format CSV.

Ekspor dibuat dari salinan data terfilter sehingga tidak mengubah dataset asli.

---

## 📌 Ringkasan Hasil Analisis Notebook

Hasil berikut berasal dari analisis eksploratif pada `notebook.ipynb`.
Dashboard tetap memungkinkan pengguna memperoleh hasil berbeda ketika filter
diubah.

### Pola waktu dan jenis hari

- Rata-rata penyewaan pada **hari kerja mencapai puncak pukul 17:00**, sekitar
  **525,3 sewa per jam**.
- Rata-rata penyewaan pada **akhir pekan/libur mencapai puncak pukul 13:00**,
  sekitar **372,7 sewa per jam**.
- Temuan ini menunjukkan perbedaan pola antara kebutuhan komuter pada hari
  kerja dan aktivitas rekreasi pada akhir pekan/libur.

### Cuaca

Rata-rata penyewaan harian berdasarkan kondisi cuaca pada notebook:

| Kondisi cuaca | Jumlah observasi | Rata-rata penyewaan harian |
|---|---:|---:|
| Cerah | 463 | 4.876,8 |
| Berkabut/Berawan | 247 | 4.035,9 |
| Hujan/Salju Ringan | 21 | 1.803,3 |

Dibandingkan kondisi cerah, rata-rata pada kondisi berkabut/berawan lebih
rendah sekitar 17,2%, sedangkan hujan/salju ringan lebih rendah sekitar 63,0%.

### Suhu

| Kategori suhu | Jumlah observasi | Rata-rata penyewaan harian |
|---|---:|---:|
| Dingin (<10°C) | 60 | 1.677,8 |
| Sejuk (10-20°C) | 299 | 3.692,3 |
| Hangat (20-30°C) | 300 | 5.661,7 |
| Panas (>30°C) | 72 | 5.410,0 |

Kombinasi rata-rata terendah yang ditemukan adalah **Dingin (<10°C) +
Hujan/Salju Ringan**, sekitar **1.039 sewa per hari dari 3 hari observasi**.

### Pertumbuhan 2012 dibandingkan 2011

Total penyewaan pada notebook:

| Tahun | Total penyewaan |
|---|---:|
| 2011 | 1.243.103 |
| 2012 | 2.049.576 |

Pertumbuhan total 2012 dibandingkan 2011 adalah **806.473 penyewaan** atau
**64,9%**, setara sekitar **1,65 kali** total tahun 2011.

- Pertumbuhan year-over-year terendah berdasarkan bulan terjadi pada **Juni**:
  **41,3%**.
- Pertumbuhan tertinggi terjadi pada **Maret**: **157,4%**.

### Kualitas dan keterbatasan data

Pemeriksaan pada notebook menemukan:

- Tidak ada missing value atau duplikat pada data awal yang diperiksa.
- Terdapat nilai kelembapan `hum = 0`, yaitu 1 baris pada data harian dan
  22 baris pada data per jam; nilai tersebut ditangani pada proses cleaning
  notebook menggunakan median bulan yang sama.
- Data per jam berisi 17.379 dari 17.544 kemungkinan kombinasi 731 hari ×
  24 jam. Sebanyak 165 jam tidak tercatat, kemungkinan karena tidak ada
  penyewaan.
- Outlier pada Casual dan kecepatan angin dipertahankan karena dapat
  merepresentasikan kejadian nyata, bukan otomatis kesalahan input.
- Korelasi dan pola historis tidak membuktikan hubungan sebab-akibat.

---

## 🗂️ Struktur Proyek

```text
submission-asah/
├── README.md
├── requirements.txt
├── notebook.ipynb
└── dashboard/
    ├── dashboard.py
    └── main_data.csv
```

---

## 🛠️ Instalasi Lokal

### Prasyarat

- Python 3.10 atau lebih baru
- PowerShell, Command Prompt, atau terminal lain

### 1. Masuk ke folder proyek

```powershell
cd C:\submission-asah
```

### 2. Buat virtual environment

```powershell
python -m venv .venv
```

### 3. Aktifkan virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jika PowerShell memblokir script lokal, jalankan terminal sebagai pengguna
yang sesuai atau gunakan Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependency

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Menjalankan Dashboard

Dari folder root proyek, jalankan:

```powershell
streamlit run dashboard/dashboard.py
```

Setelah berhasil, buka alamat lokal yang ditampilkan Streamlit, biasanya:

```text
http://localhost:8501
```

Aplikasi membaca dataset dari path relatif terhadap file dashboard:

```text
dashboard/main_data.csv
```

Jangan memindahkan CSV keluar dari folder `dashboard` tanpa menyesuaikan
konfigurasi path pada aplikasi.

---

## ☁️ Deployment ke Streamlit Community Cloud

1. Buat repository GitHub untuk proyek ini.
2. Push seluruh file proyek, termasuk:
   - `dashboard/dashboard.py`
   - `dashboard/main_data.csv`
   - `requirements.txt`
   - `README.md`
3. Buka [Streamlit Community Cloud](https://share.streamlit.io/).
4. Pilih **Create app**.
5. Pilih repository dan branch yang digunakan.
6. Isi **Main file path** dengan:

   ```text
   dashboard/dashboard.py
   ```

7. Klik **Deploy**.

Jika melakukan perubahan kode setelah deployment:

```powershell
git add .
git commit -m "Update dashboard"
git push
```

Streamlit Community Cloud akan membangun ulang aplikasi dari commit terbaru.

### File yang tidak perlu diunggah

Jangan commit virtual environment atau secrets:

```text
.venv/
.streamlit/secrets.toml
__pycache__/
*.pyc
```

Gunakan `.gitignore` untuk mengecualikan file tersebut.

---

## 📦 Dependency

Dependency utama tersedia di [requirements.txt](requirements.txt):

```text
streamlit
pandas
numpy
plotly
```

---

## 👤 Identitas Proyek

- **Nama:** I Made Dwira Dwijanata
- **Email:** ds014b6y0757@student.devacademy.id
- **ID Dicoding:** DS014B6Y0757

---

## ⚠️ Catatan Interpretasi

Dashboard ini ditujukan untuk eksplorasi dan analisis historis. Hasil
simulasi pada **Customer Analysis**, **Simulation Lab**, dan **Capacity
Planning** merupakan skenario hipotetis untuk membantu eksplorasi keputusan.
Hasil tersebut tidak boleh diperlakukan sebagai prediksi permintaan,
kapasitas armada aktual, atau rekomendasi operasional tanpa validasi data
tambahan.
