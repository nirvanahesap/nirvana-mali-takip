import os
import django
import pandas as pd

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from core.models import (
    Malik,
    AidatDonemi,
    MalikOdemesi
)

donem = AidatDonemi.objects.get(
    donem_adi="3.Taksit"
)

df = pd.read_excel(
    "odemeler.xlsx",
    sheet_name="MALİK ÖDEMELERİ",
    header=None
)

adet = 0

for _, row in df.iterrows():

    daire = row[0]

    if pd.isna(daire):
        continue

    daire = str(daire)

    if "-" not in daire:
        continue

    daire_no = daire.split("-")[0].strip()

    try:
        malik = Malik.objects.get(
            daire_no=daire_no
        )
    except Malik.DoesNotExist:
        continue

    # 1. ödeme
    tutar1 = row[20]
    tip1 = row[22]

    if (
        pd.notna(tutar1)
        and tutar1 != 0
        and tip1 in ["N", "D"]
    ):

        MalikOdemesi.objects.create(
            malik=malik,
            aidat=donem,
            tutar=float(tutar1),
            odeme_tipi=tip1
        )

        adet += 1

    # 2. ödeme
    tutar2 = row[23]
    tip2 = row[24]

    if (
        pd.notna(tutar2)
        and tutar2 != 0
        and tip2 in ["N", "D"]
    ):

        MalikOdemesi.objects.create(
            malik=malik,
            aidat=donem,
            tutar=float(tutar2),
            odeme_tipi=tip2
        )

        adet += 1

print(f"{adet} adet 3.Taksit ödemesi aktarıldı.")