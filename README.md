Nama: Prajna Kausalya Damdami 
NPM: 2506657213 
Kelas: F 
Status: Mahasiswa

### Tugas 1

1. Ya, saya menggunakan elemen semantik seperti `<header>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen tersebut membantu saya untuk membagi halaman berdasarkan fungsinya sehingga struktur HTML lebih terorganisir dan mudah dipahami.

2. menyesuaikan layout menurut saya cukup menantang karena harus menjaga agar rapih di ukuran layar yang berbeda. seperti pada desktop, bagian hobbies menggunakan tiga kolom , sedangkan pada mobile diubah menjadi satu kolom, pakai media query. jadi content punya ruang yang cukup dan lebih mudah dibaca pada layar yang kecil. Membuat tampilan responsive, saya. memprioristakan keterbacaan dan kerapihan layout agar tetap nyaman dibaca dari manapun. 

3. Batasan yang saya rasakan adalah informasi pada website masih harus ditulis langsung di HTML, sehingga kurang praktis jika ingin memperbarui atau menambahkan data. Pada iterasi berikutnya, saya ingin menambahkan database dan Django MVT agar informasi portofolio dapat dikelola dan ditampilkan secara dinamis.

### AI Disclosure Tugas 1

Saya menggunakan ChatGPT sebagai alat bantu selama pengerjaan Tugas 1. Pada style.css, AI membantu memberikan alternatif kode untuk visual seperti shape, border, shadow, dan warna berdasarkan desain yang saya inginkan. Pada index.html, AI membantu saya memahami fungsi dan penggunaan elemen semantik seperti `<header>`, `<main>`, `<section>`, `<article>`, dan `<footer>`.

Saya tetap menyesuaikan kode sesuai kebutuhan portofolio dan melakukan pengujian secara langsung pada browser. Ketika terdapat masalah pada styling Education yang tidak muncul pada browser, saya juga melakukan pengecekan terhadap file CSS dan HTML serta memverifikasi hasilnya pada browser.


### Tugas 2

1. Ketika pengguna membuka halaman `/education/`, browser mengirimkan request ke project Django. Request tersebut pertama kali diproses oleh `portofolio/urls.py`, kemudian diteruskan ke `main/urls.py` menggunakan `include("main.urls")`. Pada `main/urls.py`, URL `/education/` diarahkan ke view `show_education`.

View `show_education` lalu mengambil data Education dari database melalui `Education.objects.all()`. Data tersebut dimasukkan ke dalam context dengan nama `education_list` dan dikirim ke template `education.html`. Template kemudian menggunakan Django Template Language untuk melakukan perulangan pada setiap data Education dan menampilkannya dalam bentuk kartu. Setelah template dirender menjadi HTML, response dikembalikan kepada browser sehingga data Education dapat dilihat oleh pengguna.

2. Data Education sebaiknya disimpan di dalam model daripada ditulis langsung di template karena data menjadi lebih mudah dikelola dan diperbarui. Jika data ditulis langsung di HTML, setiap perubahan informasi seperti nama sekolah, tahun pendidikan, atau penambahan riwayat pendidikan harus dilakukan secara manual pada template. Jadi dengan menyimpan data di model, template hanya bertugas menampilkan data yang dikirim oleh view. Jika nantinya saya ingin menambahkan beberapa riwayat pendidikan, saya cukup menambahkan data baru tanpa harus membuat struktur HTML baru untuk setiap data. Hal ini membuat aplikasi lebih mudah dipelihara dan dikembangkan di masa depan.

3. `makemigrations` digunakan untuk membuat file migration yang mencatat perubahan pada model, sedangkan `migrate` digunakan untuk menerapkan perubahan tersebut ke database. Contohnya pada Assignment 2, saya menambahkan model `Education` ke `main/models.py`. Setelah itu saya menjalankan `python manage.py makemigrations` untuk membuat file migration `0002_education.py`, kemudian menjalankan `python manage.py migrate` untuk menerapkan perubahan tersebut ke database.

### AI Disclosure Tugas 2

Saya menggunakan ChatGPT sebagai alat bantu selama pengerjaan Tugas 2. Karena Tugas 2 merupakan kelanjutan dari Tutorial 02, konsep Model-View-Template dan alur implementasinya sudah cukup familiar bagi saya. Oleh karena itu, bantuan AI lebih banyak saya gunakan untuk memastikan urutan pengerjaan dan ketika berhubungan dengan terminal serta Django shell.



### Tugas 3

1. Menurut saya, lebih enak menggunakan ModelForm karena kita tidak perlu membuat semua bagian form dari awal secara manual. ModelForm bisa langsung mengambil field yang ada di model Django dan menjadikannya sebagai field pada form. Jadi form yang dibuat juga lebih sesuai dengan data yang ada di database. Di Tugas 3 ini saya membuat `EducationForm` dari model `Education`, jadi field seperti `school`, `start_year`, `end_year`, `curriculum`, dan `description` bisa langsung digunakan di form. Selain itu, saya menambahkan `{% csrf_token %}` karena form saya digunakan untuk mengirim data dengan method POST. CSRF token ini digunakan Django untuk memastikan request yang masuk memang berasal dari form pada website kita dan bukan request palsu dari website lain. Jadi, token ini membantu mencegah orang lain mengirim request yang tidak seharusnya untuk mengubah data di website.

2. Menurut saya JSON lebih enak digunakan untuk aplikasi web karena bentuknya lebih sederhana dan lebih ringkas dibandingkan XML. JSON juga cukup mudah dibaca, baik oleh manusia maupun program. Bentuk datanya juga menggunakan key dan value serta array yang sudah sering digunakan dalam bahasa pemrograman. JSON juga cocok digunakan untuk komunikasi antara backend dan frontend, terutama ketika data akan digunakan oleh JavaScript. Dibandingkan XML, JSON tidak membutuhkan banyak tag pembuka dan penutup sehingga data yang dikirim biasanya lebih singkat dan lebih mudah dibaca.

3. Saat data portofolio ingin dikirim dalam bentuk JSON, pertama view mengambil data dari database. Pada bagian Education, saya mengambil semua data menggunakan `Education.objects.all()`. Setelah itu data tersebut diubah menjadi JSON menggunakan `serializers.serialize("json", educations)` dan dikembalikan menggunakan `HttpResponse` dengan `content_type="application/json"`.

Setelah mendapatkan data JSON tersebut, pada `show_education` saya melakukan deserialize menggunakan `serializers.deserialize()`. Hasilnya kemudian diubah kembali menjadi object Django dan dimasukkan ke dalam `education_list` supaya bisa ditampilkan di `education.html`. Serialization diperlukan karena data yang berasal dari model Django tidak bisa langsung dikirim sebagai JSON. Data tersebut perlu diubah dulu ke format yang bisa dikirim melalui HTTP dan dibaca oleh aplikasi lain. Setelah itu, data JSON tersebut bisa di-deserialize lagi menjadi object Django ketika ingin digunakan kembali di halaman web.

### AI Disclosure Tugas 3

Saya menggunakan ChatGPT selama mengerjakan Tugas 3, terutama ketika ada bagian yang belum saya mengerti atau ketika saya bingung harus mulai dari mana. Saya menggunakan AI untuk memahami requirement tugas, memahami cara kerja ModelForm, membuat form create dan update, delete data, JSON, serialization, dan deserialization. Saya juga beberapa kali memberikan kode saya ke AI ketika ada error atau ketika saya ingin memastikan apakah cara yang saya buat sudah sesuai dengan requirement tugas.

Biasanya saya memberikan kode yang sedang saya kerjakan dan menjelaskan bagian mana yang membuat saya bingung. Setelah itu saya meminta AI menjelaskan langkahnya satu per satu. Saya lebih sering menggunakan AI untuk memahami kenapa sesuatu harus dibuat seperti itu, bukan hanya meminta kode jadi. Pada Tugas 3 ini saya memilih bagian Education untuk dibuat menggunakan ModelForm dan data delivery. Saya membuat `EducationForm`, lalu membuat fitur untuk menambah, mengedit, dan menghapus data Education. Saya juga membuat endpoint JSON dan menggunakan deserialize supaya data JSON tersebut bisa digunakan lagi untuk menampilkan data di halaman Education.

Selain Education, saya juga mengembangkan bagian Experience supaya memiliki fitur tambah, edit, hapus, dan JSON. Saat mengerjakan bagian ini, saya beberapa kali menyesuaikan kode yang diberikan karena struktur model dan tampilan Experience saya berbeda dengan contoh pada tutorial. Ada beberapa bagian yang ternyata tidak bisa langsung saya gunakan dari saran AI. Contohnya pada tampilan tombol Edit dan Hapus di Experience, hasil awalnya terlalu lebar dan kurang rapi. Saya kemudian mengecek CSS dan menyesuaikan sendiri bagian `flex` dan ukuran tombol sampai tampilannya lebih sesuai dengan halaman Education. Saya juga sempat membuka endpoint JSON Experience dan menemukan bahwa URL JSON-nya belum terdaftar di `urls.py`, lalu saya menambahkan route tersebut. Setelah semua fitur selesai, saya mengecek website melalui browser dan menjalankan python manage.py test. Saya juga menambahkan beberapa unit test untuk memastikan fitur create, edit, dan delete pada Education dan Experience berjalan dengan benar. Pada pengujian terakhir terdapat 16 test dan semuanya berhasil dengan status OK. Jadi selama pengerjaan, saya menggunakan AI sebagai alat bantu untuk memahami materi, mencari tahu penyebab error, dan mengecek pekerjaan saya, tetapi saya tetap mencoba, menyesuaikan kode, dan melakukan testing sendiri.