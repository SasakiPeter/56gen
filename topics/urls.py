from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:topic_id>/', views.detail, name='detail'),
    path('detail/<int:topic_id>/vote/', views.vote, name='vote'),
    path('build/', views.build, name='build'),
]
