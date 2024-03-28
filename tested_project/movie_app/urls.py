from django.contrib import admin
from django.urls import path
from . import views
app_name='movie_app'
urlpatterns = [
    path('',views.index,name='index'),
    path('movie/<int:movie_id>/',views.details,name='details'),
    path('add/',views.add_movie,name='add_movie'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('<slug:c_slug>/', views.index, name='products_by_category'),
    path('movie/<int:movie_id>/review/', views.review, name='review'),


]
