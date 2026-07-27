import os
import django
import pandas as pd

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from core.models import Gider

DOSYA = "odemeler.xlsx"

SAYFALAR = [
    "GİDERLER TEMMUZ 2026",
    "GİDERLER HAZİRAN 2026",
    "GİDERLER MAYIS 2026",
    "GİDERLER NİSAN 2026",
    "GİDERLER MART 2026",
    "GİDERLER ŞUBAT 2026",
    "GİDERLER OCAK 2026",
    "GİDER ARALIK 2025 VE ÖNCESİ(2)",
]

# Eski giderleri sil
Gider.objects.all().delete()

adet = 0

for sayfa in SAYFALAR:

    print(f"Okunuyor: {sayfa}")

    df = pd.read_excel(
        DOSYA,
        sheet_name=sayfa,
        header=None
    )

    # İlk 3 satır başlık
    df = df.iloc[3:]

    for _, row in df.iterrows():

        tarih = row[0]
        aciklama = row[1]
        tutar = row[2]
        odeme_tipi = row[3]

        # Açıklama boşsa geç
        if pd.isna(aciklama):
            continue

        # Tutar boşsa geç
        if pd.isna(tutar):
            continue

        aciklama = str(aciklama).strip()

        # Toplam satırlarını alma
        ust = aciklama.upper()

        if (
            "TOPLAM" in ust
            or "ÇELİK İNŞAATA VERİLEN TOPLAM TUTAR" in ust
        ):
            continue

        # Tarih
        tarih_kaydi = pd.to_datetime(
            tarih,
            errors="coerce"
        )

        if pd.isna(tarih_kaydi):
            tarih_kaydi = None
        else:
            tarih_kaydi = tarih_kaydi.date()

        # Ödeme tipi
        if pd.isna(odeme_tipi):
            odeme_tipi = "N"

        odeme_tipi = str(
            odeme_tipi
        ).strip().upper()

        if odeme_tipi not in ["N", "D"]:
            odeme_tipi = "N"

        # Tutarı güvenli dönüştür
        try:
            tutar = float(tutar)
        except:
            continue

        Gider.objects.create(
            tarih=tarih_kaydi,
            aciklama=aciklama,
            tutar=tutar,
            odeme_tipi=odeme_tipi
        )

        adet += 1

print(f"{adet} gider aktarıldı.")