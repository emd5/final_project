from .views import book_add_search, book_add_scan, book_post_view, book_list_view

from django.urls import path

urlpatterns = [
    path('', book_list_view, name='book_add_landing'),
    # path('<int:pk>', book_detail_view, name='book_detail')
    path('search/', book_add_search, name='book_search'),
    path('post/', book_post_view, name='book_post'),
    path('scan/', book_add_scan, name='book_scan'),
]
