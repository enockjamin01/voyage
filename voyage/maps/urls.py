from django.urls import path
from .views import Home,SignUp,Logout,LogIn

urlpatterns=[
    path('',Home.as_view(),name="home"),
    path('signup',SignUp.as_view(),name="signup"),
    path('logout',Logout.as_view(),name="logout"),
    path('login',LogIn.as_view(),name="login")
]