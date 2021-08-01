from django.urls import path
from . import views



app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='details'),
    path('<int:pk>/result/', views.result, name='results'),
    path('<int:pk>/vote/', views.vote, name='votes')
]
