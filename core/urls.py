from django.urls import path
from core.views import giderler
from core.views import excel_export

from .views import (
    dashboard,
    dashboard2,
    aidat_durumu,
    excel_import,
    borclular,
    fon_giderleri,
)


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("aidat-durumu/", aidat_durumu, name="aidat_durumu"),
    path("excel-import/", excel_import, name="excel_import"),
    path("borclular/", borclular, name="borclular"),
    path("giderler/", giderler, name="giderler"),
    path("excel-export/", excel_export, name="excel_export"),
    path("nirvana-finans-2026/", dashboard2, name="dashboard2"),
    path("fon-giderleri/", fon_giderleri, name="fon_giderleri"),
]