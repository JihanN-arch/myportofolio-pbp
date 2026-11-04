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

## 📝 Jawaban Pertanyaan Reflektif (Tugas 2)

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

## 📝 Jawaban Pertanyaan Reflektif (Tugas 3)

### 1. Kenapa Pakai `ModelForm` dan Kenapa Wajib `{% csrf_token %}`?

- **Alasan Menggunakan `ModelForm`:**  
  Kalau bikin form HTML secara manual, kita harus nulis elemen `<input>` satu per satu, ngambil datanya dari _request_ secara manual, lalu bikin validasi kustom di _view_ yang panjang dan berulang—jelas melanggar prinsip **DRY**. Dengan `ModelForm`, semua itu jauh lebih efisien karena Django otomatis ngebikinin _field_ form dari _model_ dan menyediakan validasi bawaan, seperti pengecekan tipe data, batas karakter (`max_length`), dan _field_ wajib diisi atau tidak. Selain itu, data yang sudah valid bisa langsung disimpan lewat `form.save()` tanpa perlu memetakan ulang tiap _field_ ke objek _model_.
- **Alasan Wajib Menambahkan `{% csrf_token %}`:**  
  Token ini berfungsi untuk melindungi aplikasi dari serangan **CSRF (_Cross-Site Request Forgery_)**, yaitu ketika penyerang memanfaatkan _cookie_ pengguna yang sedang login untuk mengirim permintaan palsu tanpa sepengetahuan pengguna. Dengan `{% csrf_token %}`, Django menyisipkan nilai rahasia ke dalam form. Saat form di-_submit_, Django akan mencocokkan token di form dengan token milik sesi pengguna. Kalau tidak cocok, permintaan ditolak dan muncul _error_ **403 Forbidden**.

### 2. Kenapa JSON Lebih Disukai daripada XML?

Jujur, saya belum pernah benar-benar memakai XML dan jauh lebih sering ketemu JSON. Sekilas lihat dari slide, XML terlihat lebih ribet karena setiap data harus dibungkus _tag_ pembuka dan penutup, sehingga hasilnya panjang dan lebih susah dibaca. Sebaliknya, JSON berbasis pasangan _key-value_ yang lebih ringkas dan mudah dibaca manusia, sehingga JSON lebih disukai dalam pengembangan aplikasi web modern. WHO IS JSONN???!

### 3. Alur View yang Mengembalikan JSON & Alasan Perlunya Serialization

- **Alur Request sampai Response JSON:**  
  Secara garis besar, _view_ mula-mula menerima _request_ dari _client_ dan membaca parameter _query_ pada URL (kalau ada). Kemudian, fungsi _view_ mengambil atau memfilter data dari _database_ lewat _model_, yang hasilnya berupa _QuerySet_ (kumpulan objek Python). Setelah itu, proses **serialization** mengubah _QuerySet_ tersebut menjadi teks berformat JSON, lalu dikirim kembali ke _client_ melalui `HttpResponse` (atau `JsonResponse`) beserta _header_ `Content-Type` yang sesuai.
- **Kenapa Perlu Serialization:**  
  _QuerySet_ adalah objek Python yang hidup di memori _server_, sedangkan HTTP hanya bisa mentransfer data berupa teks murni, bukan objek bahasa pemrograman. Karena itu, _serializer_ berperan sebagai "penerjemah" yang mengekstrak nilai tiap _field_ dari objek Python ke format standar JSON, sehingga datanya bisa dipahami dan diolah oleh aplikasi lain.

---

## 📝 Jawaban Pertanyaan Reflektif (Tugas 5)

### 1. Debouncing pada Fitur Pencarian AJAX

- **Pengertian Debouncing:**  
  Debouncing adalah teknik optimasi untuk menunda eksekusi suatu fungsi sampai tidak ada lagi panggilan baru yang dipicu dalam jeda waktu tertentu (_delay_). Dalam fitur pencarian, debouncing bekerja seperti penahan _timer_. Setiap kali pengguna menekan tombol _keyboard_, _timer_ akan di-reset. Fungsi panggilan AJAX baru benar-benar dieksekusi hanya ketika pengguna berhenti mengetik selama durasi waktu yang telah ditentukan.
- **Pentingnya Debouncing pada Pencarian AJAX:**  
  Teknik ini sangat penting untuk mengurangi jumlah _request_ ke _server_. Tanpa debouncing, menginput kata `"laptop"` (6 karakter) akan memicu 6 _HTTP request_ terpisah secara langsung. Dengan debouncing, hanya 1 _request_ yang dikirim setelah pengguna selesai mengetik seluruh kata. Hal ini mencegah _network overhead_, mengurangi beban _database_, dan menghindari _race condition_ akibat balasan _request_ yang saling bersusulan.

### 2. Fungsi `await` pada `fetch()` dan Dampak Jika Tidak Menggunakannya

- **Fungsi `await` pada `fetch()`:**  
  Fungsi `fetch()` dalam JavaScript pada dasarnya mengembalikan sebuah **Promise** (objek yang mewakili operasi asinkron yang belum selesai). Penggunaan `await` berfungsi untuk menghentikan sementara (_pause_) eksekusi fungsi `async` sampai _Promise_ dari `fetch()` selesai di-resolve, lalu mengekstrak nilai hasilnya (_Response object_) secara langsung.
- **Dampak Jika Tidak Menggunakan `await`:**  
  Jika tidak menggunakan `await`, variabel penyimpanan hasil `fetch()` hanya akan berisi objek _Promise_ (`Promise <pending>`), bukan data _response_ dari _server_. Akibatnya, operasi lanjutan seperti `response.json()` akan _fail_ atau _error_. Selain itu, eksekusi kode di bawah baris `fetch()` akan langsung berjalan secara _synchronous_ sebelum _server_ sempat memberikan balasan, sehingga variabel hasil rendering atau pembaruan DOM akan bernilai `undefined` atau kosong.

### 3. Serangan XSS dan Kerentanan pada AJAX/JavaScript vs. Template Django

- **Pengertian Serangan XSS (Cross-Site Scripting):**  
  XSS adalah serangan di mana penyerang berhasil menyisipkan dan mengeksekusi skrip berbahaya (biasanya JavaScript) ke dalam halaman web yang dilihat oleh pengguna lain. Skrip ini dapat mencuri _cookies_, _session token_, mengambil data sensitif, hingga melakukan tindakan ilegal atas nama pengguna yang terinfeksi.
- **Kenapa AJAX/JavaScript Lebih Rentan daripada Template Django:**  
  Template Django menyediakan perlindungan otomatis berupa **HTML Auto-Escaping** saat merender variabel (misal `{{ product.name }}`), sehingga karakter berbahaya seperti `<` atau `>` diubah menjadi teks biasa yang aman. Sebaliknya, saat data balasan _fetch_ dimasukkan via JavaScript—terutama menggunakan `innerHTML = data`—fitur _auto-escaping_ Django sama sekali tidak berlaku karena proses rendering terjadi di sisi _client_ (_browser_), bukan di _template engine_ Django. Jika data dari API mengandung tag `<script>`, _browser_ akan langsung mengesekusinya sebagai HTML/JS executable.
- **Pencegahan pada JavaScript:**  
  Untuk mencegahnya, kebersihan dan keamanan kode menjadi tanggung jawab _developer_. Hindari penggunaan `innerHTML` untuk memasukkan data dari pengguna atau API, dan gunakan properti aman seperti `textContent` atau `innerText` yang secara otomatis memperlakukan data sebagai teks murni.

---

## 📝 Jawaban Pertanyaan Reflektif (Tugas 6)

### 1. REST, RESTful, serta Perbedaan PUT vs PATCH

- **Pengertian REST:**  
  REST (_Representational State Transfer_) itu **gaya arsitektur** atau aturan main buat ngerancang API, jadi bukan _library_ atau format data. API sendiri yang jadi jembatan antara _client_ dan _server_ buat transaksi data (CRUD), sedangkan REST ngatur _gimana_ jembatan itu dirancang. Dua ide utamanya:
  - **Data diperlakukan sebagai _resource_ yang ditunjuk URL.** Contoh di proyekku: `/api/v1/experiences/` buat kumpulan experience, dan `/api/v1/experiences/<id>/` buat satu experience.
  - **HTTP method yang nyatain tindakannya**, jadi tindakan ga perlu ditulis di URL. Dulu di Tugas 5 aku pakai `/projects/add-ajax/`, sekarang cukup `POST /api/v1/projects/`.
- **Kenapa Balikin JSON Doang Belum Cukup Disebut RESTful:**  
  Karena JSON itu cuma format data (bungkusnya doang). Supaya beneran RESTful, API harus memenuhi prinsip arsitektur REST: URL-nya nunjuk _resource_, pakai standar **HTTP methods** (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) dengan benar sesuai fungsinya, dan **stateless** (tiap _request_ bawa semua info yang dibutuhin, server ga perlu inget _request_ sebelumnya). Jadi kalau cuma ngelempar data JSON tapi URL-nya berisi aksi (kayak `/add-ajax/`) atau semua tindakan lewat `POST`, ya belum bisa disebut RESTful.  
  Catatan: API-ku sebenarnya ga 100% stateless, karena `SessionAuthentication` nyimpen sesi _login_ di server. Tapi ini pilihan yang wajar buat AJAX yang jalan di website yang sama, dan DRF sendiri ga maksa satu gaya desain.
- **`PATCH`:**  
  Digunakan buat **mengubah sebagian data aja** (_partial update_). Cukup kirim _field_ yang mau diubah, _field_ lain tetap. Contoh di proyekku: modal edit Experience pakai `PATCH`, jadi kalau cuma ganti judul, data lain ga ikut berubah. Di view-nya ada `partial=request.method == "PATCH"` yang ngebedain ini.
- **`PUT`:**  
  Digunakan buat **mengganti seluruh data** secara penuh (_full update_), jadi semua _field_ wajib harus dikirim. Di DRF, kalau ada _field_ wajib yang ketinggalan, _request_-nya **ditolak dengan 400**, bukan datanya jadi kosong. Ini juga aku buktiin di _test_: `PUT` yang cuma bawa `{"year": 2024}` tanpa `title` hasilnya 400.

### 2. Peran Serializer di Django REST Framework (DRF)

- **Peran Serializer:**  
  Serializer tuh kayak penerjemah (misalnya dari bahasa Indonesia ke Inggris di otak). Kayak kalo kita nerima surat berbahasa Inggris, di otak kita menerjemahkan surat itu ke bahasa Indonesia. Kerjanya **dua arah**: pas `GET`, objek model diubah jadi data yang bisa dikirim sebagai JSON; pas `POST`/`PATCH`, data JSON dari _client_ dicek dulu lalu diubah jadi data yang siap disimpan.
- **Lebih Praktis daripada Rakit _Dictionary_ Manual:**  
  Bayangin kalau kita rakit manual pake `dict` dan `JsonResponse` kaya di Tutorial 05 bakal ribet dan capek. Di Tugas 5, `get_experiences_json` aku rakit pakai _loop_ dan `data.append({...})` satu per satu, dan input dibaca lewat `request.POST` + `ExperienceForm`. Misal kalau modelnya punya 10 _field_ atau relasi ke tabel lain, kita harus nulis kodenya satu-satu secara manual dan rawan _typo_. Sekarang cukup `ExperienceSerializer(...)`, dan input dibaca lewat `request.data` yang bisa nerima JSON.
- **Otomasi Validasi & Konversi:**  
  Serializer bisa otomatis ngecek apakah data dari _client_ valid (misalnya tipe data sesuai, tanggal akhir ga boleh sebelum tanggal mulai, _field_ wajib keisi). Validasinya terpusat di `validate_<field>` dan `validate()`, terus `is_valid(raise_exception=True)` otomatis balikin 400 lengkap sama error per _field_. Selain itu, daftar `fields` yang ditulis eksplisit bikin data sensitif (kayak email) ga ikut keluar, dan _field_ `read_only` (kayak `star_count`) ga bisa diisi dari luar.

### 3. Autentikasi vs Otorisasi & Kenapa Cuma Sembunyiin Tombol Ga Cukup

- **Autentikasi vs Otorisasi:**  
  Autentikasi itu buat ngecek **siapa kamu** (kenal apa enggak, misal udah _login_ atau belum), kalau otorisasi itu ngecek **apa yang boleh kamu lakuin** (hak aksesnya sampe mana, misal cuma pemilik/_superuser_ yang boleh ngehapus data). Di DRF keduanya dipisah: _authentication class_ (`SessionAuthentication`) baca _cookie_ sesi lalu ngisi `request.user`, terus _permission class_ (`IsPortfolioOwnerOrEditorOrReadOnly`) yang mutusin _request_ itu boleh lanjut atau ditolak 403.
- **Kenapa Harus Pakai _Permission Class_ di Server:**  
  Bisa aja kalau _user_ ngotak-ngatik URL atau mainin API-nya langsung (misal pake Postman atau _inspect element_), mereka tetep bisa nge-_hit_ _endpoint_ server. Kalau di _front-end_ tombolnya doang yang diumpetin tapi di _back-end_ ga dipasang _permission_, ya data atau _endpoint_-nya bakal jebol karena server nerima _request_ begitu aja tanpa ngecek ulang siapa yang nembak. Ini aku buktiin di `test_guest_and_visitor_cannot_write`: _request_ dikirim langsung ke API tanpa lewat tombol, dan tetep ditolak 403 dengan data di _database_ ga berubah.

### 4. Token CSRF di SessionAuthentication & `force_authenticate`

- **Kenapa _Request_ yang Mengubah Data Tetap Butuh Token CSRF:**  
  Karena `SessionAuthentication` itu nyimpen sesi _login_ lewat _cookie_ browser. Kalau ada situs jahat yang nge-_trigger_ _request_ dari browser kamu tanpa sepengetahuanmu (serangan CSRF), browser bakal otomatis nyertain _cookie_ sesi kamu ke server. Makanya butuh **token CSRF** sebagai pengaman tambahan biar server tahu kalau _request_ itu bener-bener dikirim secara sadar dari _client_ asli, bukan dari situs lain yang nyolong jalur. Token ini ampuh karena situs jahat bisa bikin browser **ngirim** _cookie_, tapi ga bisa **baca** isi _cookie_ `csrftoken` punya situsku, jadi ga bisa naruh nilainya di _header_ `X-CSRFToken`.
- **Kenapa _Test_ dengan `force_authenticate` Ga Cukup:**  
  Karena `force_authenticate` itu cara instan buat nembak _endpoint_ di _unit test_ DRF dengan cara **_by-pass_ (ngelewatin)** proses autentikasi normal dan mekanisme pengecekan _cookie_ session/CSRF. Jadi, meskipun _test_ kamu lolos pakai `force_authenticate`, itu _gak ngetes sama sekali_ apakah sistem perlindungan CSRF bener-bener aktif menangkal _request_ ilegal dari luar. Bahkan `APIClient` biasa juga ngelewatin pengecekan CSRF secara bawaan, walaupun udah pakai `.login()`. Buat ngetes CSRF beneran, harus pakai **`APIClient(enforce_csrf_checks=True)`** plus **`.login()`** biar ada _session_ asli. Di proyekku ini ada di `test_session_write_without_csrf_is_rejected` (tanpa token → 403) dan `test_session_write_with_csrf_succeeds` (dengan token → berhasil).

---

## 🤖 AI Disclosure & Reflection

Dalam proses pengerjaan Tugas 1, 2, 3, 4, 5, dan 6 saya memanfaatkan AI (**Claude**) dan (**Gemini**) sebagai alat bantu. Berikut adalah rincian penggunannya:

### 1. Prompting Strategy

Saya menggunakan teknik _iterative prompting_ dan _context-based debugging_. Daripada meminta AI membuat seluruh kode dari awal, saya membangun kode sendiri dan memberikan potongan kode yang bermasalah atau hasil akhir yang belum sesuai, lalu meminta penjelasan konseptual beserta solusi perbaikannya.

Khusus pada **Tugas 3**, karena kendala manajemen waktu akibat kepadatan jadwal kuis serta keikutsertaan dalam _hackathon_ di minggu sebelumnya, saya sempat meminta Claude untuk merancang (_generate_) beberapa bagian kode dasar. Namun, karena kode dari AI sering kali tidak langsung pas dengan konteks proyek, saya melakukan penyesuaian ulang secara manual agar seluruh modul dapat terintegrasi dengan baik.

### 2. Pembagian Kontribusi: AI vs Penulisan Mandiri

- **Dibantu AI:**
  - Diskusi _conventional commit message_ (seperti penggunaan _prefix_ `feat`, `style`, `fix`, dll.).
  - _Troubleshooting_ staging dan konflik Git.
  - Membantu mencari solusi ketika tampilan CSS tidak sesuai dengan ekspektasi di _breakpoint_ tertentu.
  - Penyediaan referensi logika dan penjelasan jika ada alur JavaScript yang belum dipami.
  - Membantu merapihkan README agar lebih terbaca dan rapih.
  - Membantu pengeditan dan penyutingan struktur kalimat pada penjelasan dokumentasi agar lebih rapih dan profesional.
  - Pembuatan komponen **modal pop-up** (_add_, _edit_, dan _delete_).
  - Implemetasi dan _styling_ **toolbar search**.
  - Pembuatan komponen **toaster / notification toast**.
  - Menyediakan referensi logika, debugging, dan penjelasan alur asynchronous (AJAX, fetch(), debouncing, dan manipulasi DOM).
  - Debugging dan merapihkan logika kode JS, serializer dan views untuk API.
  - Parafrase jawaban refleksi agar kalimatnya lebih enak dibaca.

- **Dikerjakan Mandiri:**
  - Penulisan seluruh struktur HTML dan _layout_ CSS utama.
  - Penyesuaian akhir tampilan visual, skema warna, dan pemilihan aset proyek.
  - Penyesuaian akhir logika, integrasi antar-komponen, dan _refactoring_ gaya tampilan.
  - Menghubungkan seluruh komponen UI dengan backend Django, mengolah response AJAX, serta memastikan alur E2E (End-to-End) berjalan lancar.
  - Mengembangkan dan mengadaptasi logika JavaScript hasil rekomendasi AI sesuai dengan kebutuhan spesifik proyek.
  - views dan serializer API

### 3. Analisis Kritis & Perbaikan Manual

AI tidak selalu memberikan hasil yang sesuai dengan kebutuhan proyek dan ekspektasi saya. Beberapa perbaikan manual tetap dilakukan, sebagai contoh: saat Claude menyarankan _rule_ CSS yang tidak sesuai dengan _wireframe_, saya menolaknya dan melakukan perbaikan manual agar tampilan tetap konsisten dengan desain awal.  Begitu pula saat responsivitas di breakpoint tertentu tidak sesuai harapan atau ketika menghadapi logika JavaScript yang belum familier, saya akan menjadikan kode dari AI sebagai referensi pemahaman logika dan mengembangkannya ulang secara mandiri.

Pada Tugas 3, ketika porsi kode yang dibantu AI cukup banyak, saya mendapati beberapa masukan kode mengalami ketidakcocokan (_miss_) dengan struktur dan _style_ yang sudah saya bangun sebelumnya. Proses ini menuntut saya untuk melakukan evaluasi kritis dan perbaikan manual secara menyeluruh. Meskipun membutuhkan usaha ekstra, proses perbaikan mandiri ini justru sangat bermanfaat karena memastikan saya benar-benar memahami logika di balik kode tersebut, bukan sekadar menerimanya secara membabi buta.

Pada Tugas 4, saat menyesuaikan layout dan style pada navbar, saya sempat mengalami kebuntuan dalam memisahkan hierarki visual antara navigasi utama, identitas brand, dan menu account. Setelah sempat mencoba merombak kode secara mandiri dengan hasil yang kurang terstruktur, saya lempar kode ke AI dan menemukan pendekatan desain baru, seperti ide penggunaan badge untuk profil pengguna serta penambahan line breaker sebagai pemisah intuitif pada tampilan mobile. Meskipun menggunakan AI tanpa konfigurasi agent memerlukan penyesuaian ekstra untuk menyelaraskan kode generate dengan struktur utama, pendekatan eksploratif ini sengaja saya pilih agar saya dapat mengevaluasi ide-ide baru secara kritis, memegang kendali penuh atas hasil akhirnya, dan benar-benar memahami logika di balik setiap keputusan desain. Sama seprti di tugas sebelumnya :D

Pada Tugas 5, Sama seperti pada tugas sebelumnya, jika terdapat logika kode atau kendala teknis yang belum saya pahami sepenuhnya, saya berkonsultasi dengan AI untuk mengeksplorasi referensi solusi. Setelah memahami kodenya, saya melakukan penyesuaian (adjustment), refactoring, dan integrasi secara mandiri agar sesuai dengan kebutuhan serta struktur proyek yang saya bangun

Pada Tugas 6 ini, jika mengalami kendala teknis, saya berkonsultasi dengan AI. Saya menggunakan AI untuk memahami logika kode, menanyakan sintaks, serta mengonfirmasi proses alur data dan logika program saya. Biasanya, saya menulis kode terlebih dahulu, lalu menanyakannya kepada AI untuk mengecek barangkali ada penulisan yang salah atau kode yang kurang tepat, mengingat saya jujur sering banget typo. Selain itu, saya juga menggunakan AI untuk merapikan jawaban dari tugas refleksi dan melakukan parafrase agar kalimatnya lebih enak dibaca.

---

🔗 **Tautan Percakapan AI:**

- [Dokumentasi Percakapan Gemini](https://share.gemini.google/OVE7LGkSrSel)

_(Catatan Evaluator: Rincian baris kode yang dibantu AI telah saya tandai dengan comment langsung di dalam file terkait)._

---
