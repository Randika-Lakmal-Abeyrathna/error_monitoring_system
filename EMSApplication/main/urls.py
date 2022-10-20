from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name="index"),
    path('home', views.index, name="home"),
    path('register/',views.register,name="register"),
    path('reset/',views.reset,name="reset"),
    path('adminhome/',views.adminhome,name="adminhome"),
    path('logout',views.logoutUser,name="logoutUser"),
    path('login/',views.loginUser,name="loginUser"),
    path('adminhome/update',views.updateUser,name="updateUser"),
    path('adminhome/addserver',views.addserver,name="addserver"),
    path('adminhome/updateserver',views.updateserver,name="updateserver"),
    path('sendEmail',views.sendEmail,name="sendEmail"),
    path('changepassword',views.changepassword,name="changepassword"),
    
]