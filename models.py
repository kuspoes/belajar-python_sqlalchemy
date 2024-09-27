from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Buat engine
engine = create_engine('sqlite:///pustaka.db')

# Base
Base = declarative_base()

# Models
class Penulis(Base):
    __tablename__ = 'penulis'

    id = Column(Integer, primary_key=True)
    nama = Column(String(100), nullable=False, unique=True)
    negara = Column(String(50))

    # Buat Relasi
    # Buku adalah nama class, penulis adalah column yg menjadi ref
    buku = relationship("Buku", back_populates="penulis")

    # Untuk pengganti cursor biar mudah dibaca
    def __repr__(self) -> str:
        return f"<Penulis(nama={self.nama})>"

class Buku(Base):
    __tablename__ = 'buku'

    id = Column(Integer, primary_key=True)
    judul = Column(String(200), nullable=False)
    tahun = Column(Integer)
    penulis_id = Column(Integer, ForeignKey('penulis.id'))

    # relationship
    penulis = relationship("Penulis", back_populates='buku')

    def __repr__(self) -> str:
        return f"<Buku(judul={self.judul}) >"

# Buat tabel di database
Base.metadata.create_all(engine)

# Session
Session = sessionmaker(bind=engine)
session = Session()
