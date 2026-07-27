import os
import django
import pandas as pd

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from core.models import FonHareketi

# Önce eski fon hareketlerini temizle
FonHareketi.objects.all().delete()

df = pd.read_excel(
    "odemeler.xlsx",
    sheet_name="FON GELİR-GİDER",
    header=None
)

adet = 0

for _, row in df.iterrows():

    # GELİR TARAFI
    gelir_tarih = row[0]
    gelir_tutar = row[1]

    if (
        pd.notna(gelir_tarih)
        and pd.notna(gelir_tutar)
        and isinstance(gelir_tutar, (int, float))
    ):

        FonHareketi.objects.create(
            tarih=pd.to_datetime(gelir_tarih).date(),
            hareket_tipi="GELIR",
            aciklama="Fon Geliri",
            tutar=float(gelir_tutar)
        )

        adet += 1

    # GİDER TARAFI
    gider_tarih = row[5]
    gider_aciklama = row[6]
    gider_tutar = row[7]

    if (
        pd.notna(gider_tarih)
        and pd.notna(gider_aciklama)
        and pd.notna(gider_tutar)
    ):

        try:

            FonHareketi.objects.create(
                tarih=pd.to_datetime(gider_tarih).date(),
                hareket_tipi="GIDER",
                aciklama=str(gider_aciklama).strip(),
                tutar=float(gider_tutar)
            )

            adet += 1

        except:
            pass

print(f"{adet} fon hareketi aktarıldı.")