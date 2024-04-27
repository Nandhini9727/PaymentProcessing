from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests


def home(request):
    return render(request,'home.html')

def make_payment(request):
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder')
        card_number = request.POST.get('cardnumber')
        expiry_date = request.POST.get('expiry')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        
        payload = {
            'cardholder_name': cardholder_name,
            'card_number': card_number,
            'expiry_date': expiry_date,
            'cvv': cvv,
            'amount': amount
        }
        response = requests.post(f'http://172.31.27.150/process', data=payload)

        # Handle server response
        response_data = response.json()
        if response.status_code == 200:
            # Payment successful
            message = response_data.get('message')
            authentication_code = response_data.get('authenticationCode')
            context = {'message':message,'authentication_code':authentication_code}
            return render(request,'success.html',context)
        else:
            # Payment failed
            message = response_data.get('error')
            context = {'message':message}
            return render(request,'fail.html',context)

        
        
