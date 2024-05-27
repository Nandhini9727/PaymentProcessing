from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests


def home(request):
    # home function will help render home.html to the client
    return render(request,'home.html')


def make_payment(request):
    #make_payment will capture the credit card form infomration when user clicks submit button
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder')
        card_number = request.POST.get('cardnumber')
        expiry_date = request.POST.get('expiry')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        # payload is created as a dictionary object with the payment information captured by the djnago 
        payload = {
            'cardholder_name': cardholder_name,
            'card_number': card_number,
            'expiry_date': expiry_date,
            'cvv': cvv,
            'amount': amount
        }
        # a POST request is made to processing server
        response = requests.post(f'http://172.31.27.150', data=payload)

        # Handle server response
        response_data = response.json()
        if response.status_code == 200:
            # Payment successful
            message = response_data.get('message')
            authentication_code = response_data.get('authenticationCode')
            # context dictionary object is created to send it to success.html  under templates folder
            context = {'message':message,'authentication_code':authentication_code}
            # render will help get the success.html to the front end along with messages passed with the context dictionary
            return render(request,'success.html',context)
        else:
            # Payment failed
            message = response_data.get('error')
            # context dictionary object is created to send it to fail.html under templates folder
            context = {'message':message}
            # render will help get the fail.html to the front end along with messages passed with the context dictionary
            return render(request,'fail.html',context)

        
        
def getTotalSpend(request):
    #getTotalSpend will capture the credit card number when user clicks submit button and gets the total spend for that credit card 
    if request.method == 'POST':
        card_number = request.POST.get('cardnumberts')
        params = {'card_number': card_number}
        try:
            # Send GET request to processing server
            response = requests.get('http://172.31.27.150', params=params)
            #convert json into dictionary
            data = response.json()
            #getting the amount value using key of it in dictionary
            total_amount = data.get('total_amount')
    
            if total_amount is not None:
                #render will help get the home.html to the front end with message pages with the context dictionary
                return render(request, 'home.html', {'total_amount': total_amount})
            else:
                # when the total_amount is None we response with a html page that tell total spend not avialable
                return HttpResponse("<h1>Total spend not available</h1>")
        except requests.RequestException as e:
            # Handle request exception
            return HttpResponse("<h1>Error retrieving total spend</h1>")