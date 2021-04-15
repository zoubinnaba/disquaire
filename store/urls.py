from django.urls import path
from store.views import index, listing, album_detail, search

app_name = "store"

urlpatterns = [
    path('', index, name='index'),
    path('store', listing, name="listing"),
    path('search', search, name="search"),
    path('album_detail/<int:pk>/', album_detail, name='album_detail')
]
