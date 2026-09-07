# Portfolio Web - Tugas PBP

**Nama:** Jihan Nabiilah P.S  
**NPM:** 2506549026  
**Kelas:** PBP C

---

## 📊 Progress Mingguan

Progress mingguan dapat diakses melalui tautan spreadsheet berikut:  
🔗 [Spreadsheet Progress Mingguan](https://docs.google.com/spreadsheets/d/1A4h345SCZcQlnkBNt1RS6Qftode1md8AMZLhAVsMl30/edit?usp=sharing)

---

## 📝 Jawaban Pertanyaan Reflektif (Tugas 1)

### 1. Penggunaan Elemen Semantik HTML5

Umm sebenernya dari ketiga elemen semantik HTML5, saya cuma menggunakan `<section>`. Tag `<section>` membantu saya untuk memisahkan area logis utama pada halaman seperti _About Me_, _Expertise_, dan _Project_. Bagi saya, ini juga membantu dalam menjaga keterbacaan kode (_code readability_).

Saya tidak menggunakan `<article>` atau `<aside>` karena kebutuhan portofolio ini berbasis _reusable card_. Struktur portofolio ini bersifat _self-contained_ dalam bentuk modul grid/flexbox, sehingga penggunaan `<section>` yang dikombinasikan dengan pembungkus `<div>` sudah cukup efisien dan memenuhi kebutuhan desain.

### 2. Tantangan Responsive Design & Evaluasi Layout

- **Tantangan Responsivitas Visual:**  
  Tantangan utama bagi saya adalah menjaga proporsi elemen visual seperti gambar dan SVG agar tidak mengalami distorsi, terpotong, atau gepeng saat diakses dari berbagai ukuran layar. Di portofolio ini, saya menerapkan properti `object-fit: cover` atau `contain` pada gambar.
- **Evaluasi & Reposisi Elemen (Desktop ke Mobile):**  
  Dalam mengevaluasi elemen dari desktop ke _mobile_, saya mengubah susunan _multi-column grid_ menjadi _single-column_ agar konten tidak berdempetan. Saya juga mengatur _font size_ tipografi di level `:root` menggunakan unit `rem` sehingga transformasinya sesuai secara proporsional. Untuk _header_, saya menyesuaikan `padding-top` pada container utama agar _page title_ tidak tertutup oleh _sticky header_.

### 3. Batasan Static Web Murni & Rencana Iterasi

- **Batasan yang Dirasakan:**  
  _For context_, jujur saya sudah lama tidak megang HTML CSS vanilla dan awalnya saya lupa bahwa ada keterbatasan pada aspek _client-side routing_ dan _state management_—berbeda dengan ekosistem SPA seperti React. Untuk menghindari redundansi kode pada _reusable component_ (seperti kartu proyek atau _expertise_), saya mengatasinya dengan memanfaatkan _server-side rendering_ sederhana menggunakan **Jinja2** melalui pengulangan _for-loop_.
- **Rencana Iterasi Selanjutnya:**  
  Untuk iterasi selanjutnya, saya berencana untuk melakukan _refactoring_ struktur komponen dan modularisasi JavaScript untuk menangani navigasi atau manipulasi DOM secara dinamis.

---

## 🤖 AI Disclosure & Reflection

Dalam proses pengerjaan Tugas 1, saya memanfaatkan AI (**Claude**) dan (**Gemini**) sebagai alat bantu. Berikut adalah rincian penggunannya:

### 1. Prompting Strategy

Saya menggunakan teknik _iterative prompting_ dan _context-based debugging_. Daripada meminta AI membuat seluruh kode dari awal, saya membangun kode sendiri dan memberikan potongan kode yang bermasalah atau hasil akhir yang belum sesuai, lalu meminta penjelasan konseptual beserta solusi perbaikannya.

### 2. Pembagian Kontribusi: AI vs Penulisan Mandiri

- **Dibantu AI:**
  - Diskusi _conventional commit message_ (seperti penggunaan _prefix_ `feat`, `style`, `fix`, dll.).
  - _Troubleshooting_ staging dan konflik Git.
  - Ide penerapan Jinja2 untuk _reusable component_.
  - Membantu mencari solusi ketika tampilan CSS tidak sesuai dengan ekspektasi di _breakpoint_ tertentu.
  - Membantu mencari library icon.
  - Membantu merapihkan README agar lebih terbaca dan rapih.
  - Membantu pengeditan dan penyutingan struktur kalimat pada penjelasan dokumentasi agar lebih rapih dan profesional.
- **Dikerjakan Mandiri:**
  - Penulisan seluruh struktur HTML dan _layout_ CSS utama.
  - Penyesuaian akhir tampilan visual, skema warna, dan pemilihan aset proyek.

### 3. Analisis Kritis & Perbaikan Manual

AI tidak selalu memberikan hasil yang sesuai dengan kebutuhan proyek dan ekspektasi saya. Beberapa perbaikan manual tetap dilakukan, sebagai contoh: saat Claude menyarankan _rule_ CSS yang tidak sesuai dengan _wireframe_, saya menolaknya dan melakukan perbaikan manual agar tampilan tetap konsisten dengan desain awal.

_(Catatan Evaluator: Rincian baris kode yang dibantu AI telah saya tandai dengan comment langsung di dalam file terkait)._

---
