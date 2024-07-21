import mysql.connector
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

class Buku:
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, iktisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.iktisar = iktisar

    def read(self, halaman):
        if halaman <= 0 or halaman > len(self.konten):
            return "Nomor halaman tidak valid"
        return self.konten[:halaman]

    def __str__(self):
        return f"{self.judul} by {self.penulis}"

def create_table():
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="", 
        database="perpustakaan"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INT AUTO_INCREMENT PRIMARY KEY,
            judul VARCHAR(255),
            penulis VARCHAR(255),
            penerbit VARCHAR(255),
            tahun_terbit INT,
            konten TEXT,
            iktisar TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_buku(judul):
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",  
        database="perpustakaan"
    )
    cursor = conn.cursor()
    query = "SELECT * FROM buku WHERE judul = %s"
    cursor.execute(query, (judul,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return Buku(result[1], result[2], result[3], result[4], result[5], result[6])
    return None

def post_buku(buku):
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",  
        database="perpustakaan"
    )
    cursor = conn.cursor()
    query = """
        INSERT INTO buku (judul, penulis, penerbit, tahun_terbit, konten, iktisar)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, buku.konten, buku.iktisar
    ))
    conn.commit()
    cursor.close()
    conn.close()

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_exception(exc):
    logger.error(f"An error occurred: {exc}")
    raise HTTPException(
        status_code=500, detail=str(exc)
    )

app = FastAPI()

class BukuRequest(BaseModel):
    judul: str
    penulis: str
    penerbit: str
    tahun_terbit: int
    konten: str
    iktisar: str

@app.post("/buku")
def add_buku(buku_request: BukuRequest):
    try:
        buku = Buku(
            buku_request.judul,
            buku_request.penulis,
            buku_request.penerbit,
            buku_request.tahun_terbit,
            buku_request.konten,
            buku_request.iktisar
        )
        post_buku(buku)
        return {"message": "Buku berhasil ditambahkan"}
    except Exception as e:
        handle_exception(e)

@app.get("/buku/{judul}")
def read_buku(judul: str):
    try:
        buku = get_buku(judul)
        if buku is None:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        return buku
    except Exception as e:
        handle_exception(e)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
