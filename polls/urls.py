from django.urls import path
from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/vote/', views.vote, name='votes'),
]
