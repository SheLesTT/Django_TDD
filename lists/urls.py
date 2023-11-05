from django.contrib import admin
from django.urls import path
from .views import home_page, view_list, new_list, add_item

print(home_page)
urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r"", home_page, name="home"),
    path(r"new", new_list, name="new_list"),
    path(r"<int:list_id>/", view_list, name="view_list"),
    path(r"<int:list_id>/add_item", add_item, name = "add_item")
]
