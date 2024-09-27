# %%
from models import Penulis, Buku, Session
from tabulate import tabulate
from sqlalchemy import and_, or_, func, delete

data = [11, 12]

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
