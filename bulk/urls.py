from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.my_view,name='bulk_upload'),
    path('update/<str:id>',views.update_image,name='update_image'),
    path('delete/<int:id>/',views.delete_image, name='delete_image'),
]