from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def initiate_payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) * 100 #Amount in cents
        #Logic to create a transaction entry
        #transaction = Transaction.objects.create(user=request.user, amount=amount, status='pending')

        #Integrate with Stripe here
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='sgd',
            payment_method_types=['card']
        )
        #Pass client secret to frontend
        return render(request, 'payments/initiate_payment.html', {'client_secret': intent.client_secret})

        #return HttpResponse("Initiating payment...")
    
    return render(request, 'payments/initiate_payment.html')