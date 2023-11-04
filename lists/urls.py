from django.contrib import admin
from django.urls import path
from .views import home_page

print(home_page)
urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r"", home_page, name="home"),
]
