from django.db import models


class Malik(models.Model):

    DURUM_SECENEKLERI = [
        ("TAMAM", "Tamam"),
        ("EKSIK", "Eksik"),
        ("MUAF", "Muaf"),
    ]

    daire_no = models.CharField(
        max_length=20,
        unique=True
    )

    ad_soyad = models.CharField(
        max_length=200
    )

    muaf_mi = models.BooleanField(
        default=False
    )

    aktif_mi = models.BooleanField(
        default=True
    )

    temmuz_oncesi_durum = models.CharField(
        max_length=20,
        choices=DURUM_SECENEKLERI,
        default="TAMAM"
    )

    notlar = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.daire_no} - {self.ad_soyad}"

    class Meta:
        verbose_name = "Malik"
        verbose_name_plural = "Malikler"

class AidatDonemi(models.Model):

    donem_adi = models.CharField(
        max_length=100
    )

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    aktif_mi = models.BooleanField(
        default=True
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.donem_adi

    class Meta:
        verbose_name = "Aidat Dönemi"
        verbose_name_plural = "Aidat Dönemleri"
class MalikOdemesi(models.Model):

    ODEME_TIPLERI = [
        ("N", "Nakit"),
        ("D", "Çek/Kart"),
    ]

    malik = models.ForeignKey(
        Malik,
        on_delete=models.CASCADE,
        related_name="odemeler"
    )

    aidat = models.ForeignKey(
        AidatDonemi,
        on_delete=models.CASCADE
    )

    tarih = models.DateField(
        
        blank=True,
        null=True

    )

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    odeme_tipi = models.CharField(
        max_length=1,
        choices=ODEME_TIPLERI
    )

    aciklama = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.malik} - {self.tutar}"

    class Meta:
        verbose_name = "Malik Ödemesi"
        verbose_name_plural = "Malik Ödemeleri"
class GiderKategori(models.Model):

    ad = models.CharField(
        max_length=100,
        unique=True
    )

    aktif_mi = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.ad

    class Meta:
        verbose_name = "Gider Kategorisi"
        verbose_name_plural = "Gider Kategorileri"
    
class Gider(models.Model):

    ODEME_TIPLERI = [
        ("N", "Nakit"),
        ("D", "Çek/Kart"),
    ]

    aciklama = models.CharField(
        max_length=500
    )

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    odeme_tipi = models.CharField(
        max_length=1,
        choices=ODEME_TIPLERI
    )

    tarih = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.aciklama

    class Meta:
        verbose_name = "Gider"
        verbose_name_plural = "Giderler"

class MalikAidat(models.Model):

    malik = models.ForeignKey(
        "Malik",
        on_delete=models.CASCADE,
        related_name="ozel_aidatlar"
    )

    donem = models.ForeignKey(
        "AidatDonemi",
        on_delete=models.CASCADE,
        related_name="ozel_aidatlar"
    )

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    aciklama = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Özel Aidat Tutarı"
        verbose_name_plural = "Özel Aidat Tutarları"
        unique_together = (
            "malik",
            "donem"
        )

    def __str__(self):
        return (
            f"{self.malik.daire_no} - "
            f"{self.donem.donem_adi} - "
            f"{self.tutar:,.0f} TL"
        )


class FonHareketi(models.Model):

    HAREKET_TIPI = [
    ("GELIR", "Gelir"),
    ("GIDER", "Gider"),
    ("HAKEDIS", "Hakediş"),
]

    tarih = models.DateField()

    hareket_tipi = models.CharField(
        max_length=10,
        choices=HAREKET_TIPI
    )

    aciklama = models.CharField(
        max_length=500
    )

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Fon Hareketi"
        verbose_name_plural = "Fon Hareketleri"

    def __str__(self):
        return (
            f"{self.hareket_tipi} - "
            f"{self.aciklama} - "
            f"{self.tutar}"
        )


class DevletHakedisi(models.Model):

    tarih = models.DateField()

    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Devlet Hakedişi"
        verbose_name_plural = "Devlet Hakedişleri"

    def __str__(self):
        return (
            f"{self.tarih} - "
            f"{self.tutar}"
        )