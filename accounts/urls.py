from .import views
from django.urls import path
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('resetpassword_validation/<uidb64>/<token>', views.resetpassword_validation, name='resetpassword_validation'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),

    
]