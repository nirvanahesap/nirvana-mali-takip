from django.contrib import admin

from .models import (
    Malik,
    AidatDonemi,
    MalikOdemesi,
    Gider,
    MalikAidat,
    FonHareketi,
    DevletHakedisi,
 
)


@admin.register(Malik)
class MalikAdmin(admin.ModelAdmin):

    list_display = (
        "daire_no",
        "ad_soyad",
        "muaf_mi",
        "aktif_mi",
        "temmuz_oncesi_durum",
    )

    search_fields = (
        "daire_no",
        "ad_soyad",
    )

    list_filter = (
        "muaf_mi",
        "aktif_mi",
        "temmuz_oncesi_durum",
    )


@admin.register(AidatDonemi)
class AidatDonemiAdmin(admin.ModelAdmin):

    list_display = (
        "donem_adi",
        "tutar",
        "aktif_mi",
    )

    list_filter = (
        "aktif_mi",
    )


@admin.register(MalikOdemesi)
class MalikOdemesiAdmin(admin.ModelAdmin):

    list_display = (
        "malik",
        "aidat",
        "tarih",
        "tutar",
        "odeme_tipi",
    )

    list_filter = (
        "aidat",
        "odeme_tipi",
    )

    search_fields = (
        "malik__ad_soyad",
        "malik__daire_no",
    )


@admin.register(Gider)
class GiderAdmin(admin.ModelAdmin):

    list_display = (
        "aciklama",
        "tutar",
        "odeme_tipi",
        "tarih",
    )

    list_filter = (
        "odeme_tipi",
    )

    search_fields = (
        "aciklama",
    )


admin.site.register(MalikAidat)
admin.site.register(FonHareketi)
admin.site.register(DevletHakedisi)
