from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def home(request):
    return render(request,'home.html')

def make_payment(request):
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder')
        card_number = request.POST.get('cardnumber')
        expiry_date = request.POST.get('expiry')
        cvv = request.POST.get('cvv')
        
        # Now you can process the data as needed
        
        # For example, you can save it to a database
        
        # Redirect to a success page
        return render(request,'sucess.html')
    else:
        # Handle GET requests or render a different template
        return render(request, 'error.html', {'message': 'Method not allowed'})