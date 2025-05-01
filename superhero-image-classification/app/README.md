# Deployment FP KCV

## Deployment di Railway

**Prerequisites:** punya akun GitHub dan repositories app yang fungsional

1. [https://railway.com](https://railway.com/)
2. Buka website di atas dan login dengan akun GitHub
3. Pastikan di GitHub sudah ada repositories yang siap deployment
4. Isi repositories : Dockerfile, main.py, requirements.txt, model
5. `Deploy a new project`
6. `Deploy from GitHub repo`
7. Pilih repo yang ingin di deploy 

---

## Deployment di Microsoft Azure

**Prerequisites:** : punya akun Microsoft Azure (free dari ITS), punya terminal Ubuntu WSL yang sudah di install SSH

1. [Azure](https://portal.azure.com/?Microsoft_Azure_Education_correlationId=c3c8a54e-f40c-4302-bd0a-015bc9a32c1a&Microsoft_Azure_Education_newA4E=true&Microsoft_Azure_Education_asoSubGuid=61a18394-4bb9-4f30-b719-636db39a8490#home)
2. Buka link di atas, pilih `Virtual machines`
3. Pilih `Create`, klik `Azure virtual machine`
4. Isi atribut-atribut form
    - `Resource group` : Create new
    - `Virtual machine name` : your_vm_name_here
    - `Region` : (Asia Pasific) Australia East
    - `Availability options` :  Availability zone
    - `Zone options` : Self-selected zone
    - `Security type` : Trusted launch virtual machines
    - `Image` : Ubuntu Server 22.04 LTS - x64 Gen2
    - `VM architecture` : x64
    - `Run with Azure Spot discount` : `Check` (Opsional)
    - `Authentication type` : SSH public key
    - `Username` : azureuser
    - `SSH public key source` : Generate new key pair
    - `SSH Key Type` : RSA SSH Format
    - `Key pair name` : your_key_name_here (untuk connect SSH dari local kita)
    - `Public inbound ports` : Allow selected ports
    - `Select inbound ports` : Check HTTP (80), HTTPS (443), dan SSH (22)
5. Review + create
    - `Preferred phone number` : Isi nomer telepon kalian
6. Download private key and create resource
7. Tunggu loading VM nya, lalu klik `Go to resource`
8. Di tab `Overview` pilih `Connect` cari `Native SSH` klik `Select`
9. Masuk ke VM via SSH
    - Download private key SSH dari Azure (yang ada pada langkah nomer 6)
    - Pindahkan ke direktori ~/.ssh
        ```bash
        chmod 400 ~/.ssh/<your-private-key>
        ```
        ```bash
        ssh -i ~/.ssh/<your_key_name_here>.pem azureuser@<your_VM_public_IP>
        ```
10. Download packages:
    ```bash
    sudo apt-get update
    sudo apt install docker.io
    ```
11. Download app repositories dari GitHub:
    ```bash
    git clone https://github.com/algof/fp_kcv_deployment.git
    ```
12. Build Image: (Di direktori root proyek, tempat `Dockerfile` berada)
    ```bash
    cd fp_kcv_deployment
    sudo docker build -t <your-image-name> .
    ```
13. Run Container:
    ```bash
    sudo docker run -d -p 8501:8501 --name <your-container-name> <your-image-name>
    ```
14. Azure network settings: <br>
    Add new inbound rule for port 8501 in Azure <br>
    Allow access from TCP to destination port 8501
15. Access App:
    Buka browser ke `http://<your-vm-public-ip>:8501`

**Cara lain untuk akses**
1. Run Container:
    ```bash
    sudo docker run -d -p 80:8501 --name <your-container-name> <your-image-name>
    ```
2. Access App:
    Buka browser ke `http://<your-vm-public-ip>`
3. Jika ingin bisa set DNS name untuk mengganti akses ke `http://<your-vm-dns-name>`

---

**Untuk Stop & Hapus Container:**

* `docker stop <your-container-name>`
* `docker rm <your-container-name>`

---

**Opsional: Reverse proxy di Microsoft Azure**
1. Install nginx:
    ```sh
    sudo apt install nginx
    sudo systemctl status nginx
    ```
2. Edit nginx.conf:
    ```sh
    cd /etc/nginx/
    sudo nano nginx.conf
    ```
    uncomment `server_names_hash_bucket_size` <br>
    ganti size ke 128
3. Buat konfigurasi nginx:
    ```sh
    sudo nano /etc/nginx/sites-available/streamlit.com
    ```
    ```conf
    server {
        listen 80;
        server_name <your-vm-dns-name>.australiaeast.cloudapp.azure.com;

        client_max_body_size 200M;

        location / {
            proxy_pass http://localhost:8501;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_redirect off;
        }
    }
    ```
4. Aktifkan konfigurasi nginx:
    ```sh
    sudo ln -s /etc/nginx/sites-available/streamlit.com /etc/nginx/sites-enabled
    ```
5. Mengetes konfigurasi nginx:
    ```sh
    sudo nginx -t
    ```
6. Restart nginx:
    ```sh
    sudo systemctl restart nginx
    ```
7. Sebelumnya dari `http://<your-vm-dns-name>:8501` ke `http://<your-vm-dns-name>`