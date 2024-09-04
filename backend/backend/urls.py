from django.contrib import admin
from django.urls import path

import levels.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_csv/', levels.views.export_player_levels_to_csv)
]
