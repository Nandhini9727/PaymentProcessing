"""
URL configuration for PaymentProcessing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # the url path as '' will be forwarded to home function in views.py to render home.html to front end
    path('make_payment/',views.make_payment,name='make_payment'),  # the url path as 'make_payment/' will be forwarded to make_payment function in views.py so that the function can forward credit card details to processing server and get approprite response to render either sucess or failure html templates to user.
    path('getTotalSpend/',views.getTotalSpend,name = 'getTotalSpend'), # the url path as 'getTotaLSpend/'  will be forwarded to getTotalSpend function in views so that the function can forward the the credit card number to processing server and get the total spend from the DynamoDB for that specific credit card number
]
