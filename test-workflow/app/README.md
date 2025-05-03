## Run with Docker

**Prerequisites:** Docker terinstal & berjalan.

1.  **Build Image:**
    (Di direktori root proyek, tempat `Dockerfile` berada)
    ```bash
    docker build -t my-app-image .
    ```
    *_(Catatan: `prepare.py` akan berjalan saat proses build)_*

2.  **Run Container:**
    ```bash
    docker run -d -p 7860:7860 --name my-app-container my-app-image
    ```

3.  **Access App:**
    Buka browser ke `http://localhost:7860`

---

**Untuk Stop & Hapus Container:**

* `docker stop my-app-container`
* `docker rm my-app-container`

---