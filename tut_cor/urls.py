from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('addData/', views.addData, name='addData'),
    path('disData/<int:id>', views.disData, name='disData'),
    path('editData/<int:id>', views.editData, name='editData'),
    path('deleteData/<int:id>', views.deleteData, name='deleteData'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addDatatoBase', views.addDatatoBase, name='addDatatoBase'),
    path('EditDatatoBase/<int:id>/', views.EditDatatoBase, name='EditDatatoBase'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('rate/<int:id>', views.rate, name='rate')
]