from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:tag_id>/', views.detail, name='detail'),
]
