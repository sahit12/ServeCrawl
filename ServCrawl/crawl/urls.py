from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='crawl-about'),
    path('wiki_data/', views.wiki_data, name='crawl-wiki_data'),
    path('summary/', views.extract_summ, name='crawl-extract_summ')
]