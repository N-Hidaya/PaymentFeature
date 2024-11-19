from django.shortcuts import render, redirect
from django.http import HttpResponse
import stripe.error
from .models import Transaction
from django.conf import settings
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    
    except ValueError as e:
        return JsonResponse({'error':'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error':'Invalid Signature'}, status=400)
    
    #Handle event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        #Update transaction in database
        #Eg. Transaction.objects.filter(...).update(status='completed')
    
    return JsonResponse({'status':'success'}, status=200)