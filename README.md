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

# 📝 Jawaban Pertanyaan Reflektif (Tugas 2)

### 1. Alur Perjalanan Request: Dari URL sampai Tampil di Browser

Pas pengguna ngetik atau ngebuka alamat portofolio di _browser_, _browser_ bakal ngirim HTTP _request_ yang langsung ditangkap sama Django. Pintu masuk pertamanya ada di `urls.py` level proyek. Di sini, `urls.py` proyek bertindak kayak pengarah lalu lintas utama yang ngerutein permintaan lewat `include("main.urls")`. Begitu dioper ke `urls.py` milik aplikasi `main`, Django bakal nyocokin rute spesifik yang dicari—apakah pengguna mau buka halaman utama, `showcase/`, atau `experience/`. Setelah nemu rute yang pas, dia bakal manggil fungsi _view_ yang sesuai (misalnya `show_main`).

Di sinilah fungsi _view_ bekerja sebagai otak aplikasinya. _View_ bakal ngecek apa aja data yang dibutuhin, lalu minta tolong ke `models.py` buat ngambil data aktual yang ada di _database_. Pas datanya udah dapet, _view_ bakal ngebungkus data itu jadi parameter/konteks tambahan dan ngereturn fungsi `render()` barengan sama file _template_ HTML-nya. Akhirnya, _template engine_ bakal ngerender data dinamis tersebut jadi struktur HTML utuh, terus dikirim balik ke _browser_ sampai halaman portofolionya muncul di layar pengguna.

### 2. Kenapa Harus Pakai Model daripada Hardcode di Template?

Ngedata bagian portofolio kayak _experience_, _projects_, atau _expertise_ di dalam **Model** itu krusial banget karena data-data ini sifatnya bakal terus bertambah seiring berjalannya waktu. Kalau kita nekat _hardcode_ tulis manual di dalam _template_ HTML, setiap ada proyek atau pengalaman baru kita harus bongkar-pasang kode markup-nya lagi. Selain bikin capek, cara ini juga rentan bikin tampilan nggak konsisten dan susah di-_maintain_.

Dengan naruh data di Model, kita bisa nerapin prinsip **DRY (Don't Repeat Yourself)** secara maksimal. Struktur komponen (kayak elemen _card_) cukup kita bikin sekali aja di _template_, terus sisanya tinggal kita _looping_ pakai data dari Model. Selain itu, urusan **CRUD (Create, Read, Update, Delete)** jadi jauh lebih practical karena kita bisa nambah atau ngubah data kapan aja lewat Django Admin tanpa perlu ngotak-ngatik kode tampilan _template_-nya sama sekali.

### 3. Perbedaan `makemigrations` dan `migrate`

Gampangnya, beda kedua perintah ini ada di tahap perancangan versus eksekusi ke _database_. Perintah `makemigrations` itu fungsinya mirip pas kita belajar konsep awal OOP—yaitu bikin _blueprint_ (rancangan). Pas kita ngubah atau nambah struktur data di `models.py`, `makemigrations` bakal menyiapkan catatan atau _blueprint_ perubahan itu di folder `migrations/`, tapi pada tahap ini struktur tabel di _database_ aslinya belum berubah sama sekali. Nah, barulah perintah `migrate` yang bertugas buat mindahin dan nerapin _blueprint_ tadi secara fisik ke dalam _database_, jadi _database_ kita siap diisi data sesuai _blueprint_ barunya.

**Contoh perubahan model yang butuh dua perintah ini:**  
Misalnya kita mau nambahin atribut/field baru `description` pada model `Project` di `models.py`:

```python
class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # <-- atribut/kolom baru
```

Urutan eksekusinya wajib dua tahap:

1. Jalankan `python manage.py makemigrations` buat nyiapin _blueprint_ penambahan kolom `description`.
2. Jalankan `python manage.py migrate` buat mengeksekusi _blueprint_ tersebut ke _database_ biar kolomnya beneran terbuat di tabel.

---

## 🤖 AI Disclosure & Reflection

Dalam proses pengerjaan Tugas 1ndan 2, saya memanfaatkan AI (**Claude**) dan (**Gemini**) sebagai alat bantu. Berikut adalah rincian penggunannya:

### 1. Prompting Strategy

Saya menggunakan teknik _iterative prompting_ dan _context-based debugging_. Daripada meminta AI membuat seluruh kode dari awal, saya membangun kode sendiri dan memberikan potongan kode yang bermasalah atau hasil akhir yang belum sesuai, lalu meminta penjelasan konseptual beserta solusi perbaikannya.

### 2. Pembagian Kontribusi: AI vs Penulisan Mandiri

- **Dibantu AI:**
  - Diskusi _conventional commit message_ (seperti penggunaan _prefix_ `feat`, `style`, `fix`, dll.).
  - _Troubleshooting_ staging dan konflik Git.
  - Membantu mencari solusi ketika tampilan CSS tidak sesuai dengan ekspektasi di _breakpoint_ tertentu.
  - Penyediaan referensi logika dan penjelasan jika ada alur JavaScript yang belum dipami.
  - Membantu merapihkan README agar lebih terbaca dan rapih.
  - Membantu pengeditan dan penyutingan struktur kalimat pada penjelasan dokumentasi agar lebih rapih dan profesional.
- **Dikerjakan Mandiri:**
  - Penulisan seluruh struktur HTML dan _layout_ CSS utama.
  - Penyesuaian akhir tampilan visual, skema warna, dan pemilihan aset proyek.

### 3. Analisis Kritis & Perbaikan Manual

AI tidak selalu memberikan hasil yang sesuai dengan kebutuhan proyek dan ekspektasi saya. Beberapa perbaikan manual tetap dilakukan, sebagai contoh: saat Claude menyarankan _rule_ CSS yang tidak sesuai dengan _wireframe_, saya menolaknya dan melakukan perbaikan manual agar tampilan tetap konsisten dengan desain awal.  Begitu pula saat responsivitas di breakpoint tertentu tidak sesuai harapan atau ketika menghadapi logika JavaScript yang belum familier, saya akan menjadikan kode dari AI sebagai referensi pemahaman logika dan mengembangkannya ulang secara mandiri.

_(Catatan Evaluator: Rincian baris kode yang dibantu AI telah saya tandai dengan comment langsung di dalam file terkait)._

---
