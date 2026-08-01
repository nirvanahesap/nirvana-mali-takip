from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


from .models import (
    Malik,
    AidatDonemi,
    MalikOdemesi,
    Gider,
    MalikAidat,
    FonHareketi,
    DevletHakedisi,
    Borc,
)


def dashboard(request):

    toplam_malik = Malik.objects.count()

    toplam_donem = AidatDonemi.objects.count()

    aktif_malik = Malik.objects.filter(
        muaf_mi=False
    ).count()

    muaf_malik = Malik.objects.filter(
        muaf_mi=True
    ).count()

    toplam_tahsilat = sum(
        odeme.tutar
        for odeme in MalikOdemesi.objects.all()
    )

    nakit_gelir = sum(
        odeme.tutar
        for odeme in MalikOdemesi.objects.filter(
            odeme_tipi="N"
        )
    )

    cek_kart_gelir = sum(
        odeme.tutar
        for odeme in MalikOdemesi.filter(
            odeme_tipi="D"
        )
    ) if False else sum(
        odeme.tutar
        for odeme in MalikOdemesi.objects.filter(
            odeme_tipi="D"
        )
    )

    toplam_gider = sum(
        gider.tutar
        for gider in Gider.objects.all()
    )

    fon_geliri = sum(
        hareket.tutar
        for hareket in FonHareketi.objects.filter(
            hareket_tipi="GELIR"
        )
    )

    fon_gideri = sum(
        hareket.tutar
        for hareket in FonHareketi.objects.filter(
            hareket_tipi="GIDER"
        )
    )

    toplam_hakedis = sum(
    h.tutar
    for h in DevletHakedisi.objects.all()
)

    toplam_hakedis_fmt = (
    f"{toplam_hakedis:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)
    toplam_gelir = (
    toplam_tahsilat
    + toplam_hakedis
)
    toplam_gelir_fmt = (
    f"{toplam_gelir:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

    aidat_kasasi = (
    toplam_tahsilat
    + toplam_hakedis
    - toplam_gider
)
    toplam_dis_borc = sum(
    x.tutar
    for x in Borc.objects.all()
)
    toplam_dis_borc_fmt = (
    f"{toplam_dis_borc:,.0f}"
    .replace(",", ".")
)
    fon_kasasi = fon_geliri - fon_gideri

    genel_kasa = aidat_kasasi + fon_kasasi

    borclu_sayisi = 0

    malikler = Malik.objects.filter(
        muaf_mi=False
    )

    for malik in malikler:

        toplam_borc = 0

        for donem in AidatDonemi.objects.all():

            try:

                ozel = MalikAidat.objects.get(
                    malik=malik,
                    donem=donem
                )

                hedef = ozel.tutar

            except MalikAidat.DoesNotExist:

                hedef = donem.tutar

            odenen = sum(
                odeme.tutar
                for odeme in malik.odemeler.filter(
                    aidat=donem
                )
            )

            eksik = hedef - odenen

            if eksik > 0:
                toplam_borc += eksik

        if toplam_borc > 0:
            borclu_sayisi += 1

    son_odemeler = MalikOdemesi.objects.order_by(
        "-created_at"
    )[:10]

    son_giderler = Gider.objects.order_by(
        "-created_at"
    )[:10]

    son_fon_hareketleri = FonHareketi.objects.order_by(
        "-created_at"
    )[:10]

    toplam_tahsilat_fmt = f"{toplam_tahsilat:,.0f}".replace(",", ".")
    toplam_gider_fmt = f"{toplam_gider:,.0f}".replace(",", ".")
    aidat_kasasi_fmt = f"{aidat_kasasi:,.0f}".replace(",", ".")
    fon_kasasi_fmt = f"{fon_kasasi:,.0f}".replace(",", ".")
    genel_kasa_fmt = f"{genel_kasa:,.0f}".replace(",", ".")

    context = {
        "toplam_malik": toplam_malik,
        "toplam_donem": toplam_donem,
        "aktif_malik": aktif_malik,
        "muaf_malik": muaf_malik,
        "toplam_tahsilat": toplam_tahsilat,
        "nakit_gelir": nakit_gelir,
        "cek_kart_gelir": cek_kart_gelir,
        "toplam_gider": toplam_gider,
        "aidat_kasasi": aidat_kasasi,
        "fon_geliri": fon_geliri,
        "fon_gideri": fon_gideri,
        "fon_kasasi": fon_kasasi,
        "genel_kasa": genel_kasa,
        "borclu_sayisi": borclu_sayisi,
        "son_odemeler": son_odemeler,
        "son_giderler": son_giderler,
        "son_fon_hareketleri": son_fon_hareketleri,
        "toplam_tahsilat_fmt": toplam_tahsilat_fmt,
        "toplam_gider_fmt": toplam_gider_fmt,
        "aidat_kasasi_fmt": aidat_kasasi_fmt,
        "fon_kasasi_fmt": fon_kasasi_fmt,
        "genel_kasa_fmt": genel_kasa_fmt,
        "toplam_hakedis": toplam_hakedis,
        "toplam_hakedis_fmt": toplam_hakedis_fmt,
        "toplam_gelir": toplam_gelir,
        "toplam_gelir_fmt": toplam_gelir_fmt,
        "toplam_dis_borc": toplam_dis_borc,
        "toplam_dis_borc_fmt": toplam_dis_borc_fmt,
    }

    return render(
        request,
        "core/dashboard.html",
        context,
    )

def dashboard2(request):

    nakit_gelir = sum(
        x.tutar
        for x in MalikOdemesi.objects.filter(
            odeme_tipi="N"
        )
    )

    hakedis = sum(
        x.tutar
        for x in DevletHakedisi.objects.all()
    )

    nakit_gider = sum(
        x.tutar
        for x in Gider.objects.filter(
            odeme_tipi="N"
        )
    )

    nakit_kasa = (
        nakit_gelir
        + hakedis
        - nakit_gider
    )

    kart_gelir = sum(
        x.tutar
        for x in MalikOdemesi.objects.filter(
            odeme_tipi="D"
        )
    )

    kart_gider = sum(
        x.tutar
        for x in Gider.objects.filter(
            odeme_tipi="D"
        )
    )

    kart_kasa = (
        kart_gelir
        - kart_gider
    )

    fon_gelir = sum(
        x.tutar
        for x in FonHareketi.objects.filter(
            hareket_tipi="GELIR"
        )
    )

    fon_gider = sum(
        x.tutar
        for x in FonHareketi.objects.filter(
            hareket_tipi="GIDER"
        )
    )

    fon_bakiye = (
        fon_gelir
        - fon_gider
    )

    toplam_isletme = (
        nakit_kasa
        + kart_kasa
    )

    def fmt(x):
        return (
            f"{x:,.0f}"
            .replace(",", ".")
        )
    toplam_dis_borc = sum(
    x.tutar
    for x in Borc.objects.all()
)

    toplam_dis_borc_fmt = (
    f"{toplam_dis_borc:,.0f}"
    .replace(",", ".")
)

    context = {
        "nakit_gelir": fmt(nakit_gelir),
        "hakedis": fmt(hakedis),
        "nakit_gider": fmt(nakit_gider),
        "nakit_kasa": fmt(nakit_kasa),

        "kart_gelir": fmt(kart_gelir),
        "kart_gider": fmt(kart_gider),
        "kart_kasa": fmt(kart_kasa),

        "fon_gelir": fmt(fon_gelir),
        "fon_gider": fmt(fon_gider),
        "fon_bakiye": fmt(fon_bakiye),

        "toplam_isletme": fmt(toplam_isletme),
        "toplam_dis_borc": toplam_dis_borc,
        "toplam_dis_borc_fmt": toplam_dis_borc_fmt,
    }

    return render(
        request,
        "core/dashboard2.html",
        context,
    )

def aidat_durumu(request):

    malikler = sorted(
        Malik.objects.all(),
        key=lambda x: (
            x.daire_no[0],
            int(x.daire_no[1:])
        )
    )

    donemler = AidatDonemi.objects.all()

    tablo = []

    for malik in malikler:

        satir = {
            "daire": malik.daire_no,
            "malik": malik.ad_soyad,
            "durumlar": []
        }

        for donem in donemler:

            try:

                ozel_aidat = MalikAidat.objects.get(
                    malik=malik,
                    donem=donem
                )

                hedef_tutar = ozel_aidat.tutar

            except MalikAidat.DoesNotExist:

                hedef_tutar = donem.tutar

            toplam_odeme = sum(
                odeme.tutar
                for odeme in malik.odemeler.filter(
                    aidat=donem
                )
            )

            if hedef_tutar == 0:

                durum = "⚪"

            elif toplam_odeme >= hedef_tutar:

                durum = "🟢"

            elif toplam_odeme > 0:

                durum = "🟠"

            else:

                durum = "🔴"

            satir["durumlar"].append({
                "durum": durum,
                "odenen": f"{toplam_odeme:,.0f}".replace(",", "."),
                "aidat": f"{hedef_tutar:,.0f}".replace(",", "."),
            })

        tablo.append(satir)

    context = {
        "donemler": donemler,
        "tablo": tablo,
        
    }

    return render(
        request,
        "core/aidat_durumu.html",
        context
    )


def excel_import(request):

    return HttpResponse(
        "Excel import ekranı hazır"
    )


def borclular(request):

    malikler = sorted(
        Malik.objects.filter(
            muaf_mi=False
        ),
        key=lambda x: (
            x.daire_no[0],
            int(x.daire_no[1:])
        )
    )

    donemler = AidatDonemi.objects.all()

    borclular_listesi = []

    for malik in malikler:

        toplam_borc = 0

        for donem in donemler:

            try:

                ozel_aidat = MalikAidat.objects.get(
                    malik=malik,
                    donem=donem
                )

                hedef_tutar = ozel_aidat.tutar

            except MalikAidat.DoesNotExist:

                hedef_tutar = donem.tutar

            toplam_odeme = sum(
                odeme.tutar
                for odeme in malik.odemeler.filter(
                    aidat=donem
                )
            )

            eksik = hedef_tutar - toplam_odeme

            if eksik > 0:
                toplam_borc += eksik

        if toplam_borc > 0:

            borclular_listesi.append(
                {
                    "daire": malik.daire_no,
                    "ad": malik.ad_soyad,
                    "borc": f"{toplam_borc:,.0f} ₺".replace(",", "."),
                }
            )

    context = {
        "borclular": borclular_listesi
    }

    return render(
        request,
        "core/borclular.html",
        context
    )
def giderler(request):

    giderler = Gider.objects.order_by(
        "-tarih",
        "-id"
    )

    for gider in giderler:
        gider.tutar_fmt = (
             f"{gider.tutar:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
)

    return render(
        request,
        "core/giderler.html",
        {
            "giderler": giderler
        }
    )

from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from django.http import HttpResponse


@staff_member_required
def excel_export(request):

    malikler = pd.DataFrame(
        list(Malik.objects.values())
    )

    odemeler = pd.DataFrame(
        list(MalikOdemesi.objects.values())
    )

    giderler = pd.DataFrame(
        list(Gider.objects.values())
    )

    fonlar = pd.DataFrame(
        list(FonHareketi.objects.values())
    )

    for df in [
        malikler,
        odemeler,
        giderler,
        fonlar,
    ]:
        if "created_at" in df.columns:
            df.drop(
                columns=["created_at"],
                inplace=True
            )

    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Nirvana_Mali_Takip.xlsx"'
    )

    with pd.ExcelWriter(
        response,
        engine="openpyxl"
    ) as writer:

        malikler.to_excel(
            writer,
            sheet_name="Malikler",
            index=False
        )

        odemeler.to_excel(
            writer,
            sheet_name="Odemeler",
            index=False
        )

        giderler.to_excel(
            writer,
            sheet_name="Giderler",
            index=False
        )

        fonlar.to_excel(
            writer,
            sheet_name="FonHareketleri",
            index=False
        )

    return response

def fon_giderleri(request):

    giderler = FonHareketi.objects.filter(
        hareket_tipi="GIDER"
    ).order_by("-tarih")

    toplam = sum(
        x.tutar
        for x in giderler
    )

    context = {
        "giderler": giderler,
        "toplam": toplam,
    }

    return render(
        request,
        "core/fon_giderleri.html",
        context
    )
from .models import Borc

def borclar(request):
    borclar = Borc.objects.all().order_by("borclu_adi")

    for borc in borclar:
        borc.tutar_fmt = (
            f"{borc.tutar:,.0f}"
            .replace(",", ".")
        )

    return render(
        request,
        "core/borclar.html",
        {
            "borclar": borclar
        }
    )
    
