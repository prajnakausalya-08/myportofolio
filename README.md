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

AI membantu saya memahami command yang perlu dijalankan seperti `makemigrations`, `migrate`, `runserver`, dan `test`, dan membantu membaca output dari terminal ketika saya kurang yakin dengan hasilnya. AI juga ngebantu saya saat menggunakan Django shell untuk masukin data Education ke database. Selain itu, saya menggunakan AI untuk memahami requirement test case dan memeriksa apakah skenario test yang dibuat sudah mencakup halaman yang dapat diakses, data yang muncul ketika tersedia, dan empty state ketika tidak ada data. Saya tetap melakukan implementasi dan pengecekan sendiri, termasuk menjalankan project melalui browser, memasukkan data melalui Django shell, serta menjalankan seluruh unit test. Hasil akhirnya adalah 9 test berhasil dijalankan dengan status `OK`.