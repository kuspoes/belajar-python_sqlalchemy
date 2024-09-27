try:
    seishi = s.query(Penulis).filter(Penulis.nama.ilike('%ishi%')).first()

    buku_daftar = [
        Buku(judul="And Then There Were None", tahun=1939, penulis_id=seishi.id),
        Buku(judul="Murder on the Orient Express", tahun=1934, penulis_id=seishi.id),
        Buku(judul="The Murder of Roger Ackroyd", tahun=1926, penulis_id=seishi.id),
        Buku(judul="Death on the Nile", tahun=1937, penulis_id=seishi.id),
        Buku(judul="The A.B.C. Murders", tahun=1936, penulis_id=seishi.id)
    ]

    for b in buku_daftar:
        s.add(b)
    s.commit()
    print(f"{len(buku_daftar)} berhasil ditambahkan")
except Exception as e:
    s.rollback()
    print(f"Error: {str(e)}")
finally:
    s.close()


# tambah data berdasarkan penulis yang sudah ada
with Session() as s:
    seishi = s.query(Buku).filter(Buku.id == 10).first()
    seishi.judul = 'The Ghost of the Imperial Hotel '
    seishi.tahun = 1965

    s.add(seishi)


    s.commit()


# insert dari dict
data = [
    {
        "nama": "Sir Arthur Conan Doyle",
        "negara": "Inggris"
    },
    {
        "nama": "Shoji Shimada",
        "negara": "Jepang"
    },
    {
        "nama": "Haji Abdul Malik Karim Amarullah (HAMKA)",
        "negara": "Indonesia"
    }
]

with Session() as s:
    penulis = [Penulis(**data) for data in data]

    s.add_all(penulis)
    s.commit()

# %%
from models import Penulis, Buku, Session

data = [
    { "judul": "Tenggelamnya Kapal Van Der Wijck", "tahun": 1938 },
    { "judul": "Merantau ke Deli", "tahun": 1941 }
]

# insert dengan penulis
with Session() as s:
    hamka = s.query(Penulis).filter(Penulis.nama.ilike('%malik%')).first()

    insert_buku = [Buku(**data, penulis_id = hamka.id) for data in data]
    s.add_all(insert_buku)
    s.commit()

# query between range tahun
with Session() as s:
    query = s.query(Buku).filter(Buku.tahun.between(1920, 1950))
    for q in query:
        print(f"{q.tahun} {q.judul}")


# query dengan range tahun dan di format table
with Session() as s:
    query = s.query(Penulis, Buku).outerjoin(Buku, Penulis.id == Buku.penulis_id).filter(Buku.tahun.between(1900, 1930))
    results = query.all()

    headers = ['Penulis', 'Judul', 'Tahun']
    table_data = [[penulis.nama, buku.judul, buku.tahun] for penulis, buku in results]

    print(tabulate(table_data, headers=headers, tablefmt='grid'))

# filter dengan multiple kriteria
with Session() as s:
    query = s.query(Penulis, Buku).outerjoin(Buku, Penulis.id == Buku.penulis_id).filter(Buku.tahun.between(1900, 1980)).filter(Penulis.negara == 'Inggris')
    results = query.all()

    headers = ['Penulis', 'Judul', 'Bahasa', 'Tahun']
    table_data = [[penulis.nama, buku.judul, penulis.negara, buku.tahun] for penulis, buku in results]

    print(tabulate(table_data, headers=headers, tablefmt='grid'))

with Session() as s:
    query = s.query(Penulis, Buku).outerjoin(Buku, Penulis.id == Buku.penulis_id).filter(and_(Buku.tahun.between(1900, 1980), Penulis.negara == 'Inggris'))
    results = query.all()

    headers = ['Penulis', 'Judul', 'Bahasa', 'Tahun']
    table_data = [[penulis.nama, buku.judul, penulis.negara, buku.tahun] for penulis, buku in results]

    print(tabulate(table_data, headers=headers, tablefmt='grid'))

# Query dengan multiple kriteria
with Session() as s:
    query = s.query(Penulis, Buku).outerjoin(Buku, Penulis.id == Buku.penulis_id).filter(
        and_(
            or_(
                Penulis.negara == 'Inggris',
                Penulis.negara == 'Jepang'
            ),
            Buku.tahun.between(1930, 1970)
        )
    )
    results = query.all()

    headers = ['Penulis', 'Judul', 'Bahasa', 'Tahun']
    table_data = [[penulis.nama, buku.judul, penulis.negara, buku.tahun] for penulis, buku in results]

    print(tabulate(table_data, headers=headers, tablefmt='grid'))

# Cari duplicates
# import func dari sqla
with Session() as s:
    cari_duplicates = s.query(
        Buku.judul,
        func.count(Buku.judul).label('count')
    ).group_by(Buku.judul).having(func.count(Buku.judul) > 1).all()
    print(cari_duplicates)

# bacth delete dengan dict
# import delete dari sqla
with Session() as s:
    cari = s.query(Buku).filter(Buku.id.in_(data)).delete(synchronize_session='fetch')
    s.commit()
