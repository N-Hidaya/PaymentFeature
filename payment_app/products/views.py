import stripe
import json
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
import stripe.error
from .models import Products

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'

class ProductLandingPage(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        product = Products.objects.get(name='Bracelet La Vie')
        context = super(ProductLandingPage, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context
    
# Create your views here.
class checkoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = Products.objects.get(id=product_id)
        print(product)
        DOMAIN = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency':'sgd',
                        'unit_amount':product.price,
                        'product_data': {
                            'name':product.name,
                            'description': 'Pretty bracelet from France'
                        },
                    },
                    'quantity':1,
                },
            ],
            metadata={
                'product_id': product.id
            },
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN +'/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })
    

@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    #Handle session checkout completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        
        customer_email = session['customer_details']['email']
        product_id = session['metadata']['product_id']

        product = Products.objects.get(id=product_id)
        send_mail(
            subject='Here is your product!',
            message=f'Thanks for your purchase! You can view the product here: {product.url}',
            recipient_list= [customer_email],
            from_email='kitade96loli@gmail.com'
        )
    
    elif event['type'] == "payment_intent.succeeded":
        intent = event['data']['object']
        print(intent)

        stripe_customer_id = intent['customer']
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        customer_email = stripe_customer['email']
        product_id = session['metadata']['product_id']
        product = Products.objects.get(id=product_id)

        send_mail(
            subject='Here is your product!',
            message=f'Thanks for your purchase! You can view the product here: {product.url}',
            recipient_list= [customer_email],
            from_email='kitade96loli@gmail.com'
        )
        #Decide whether to send file or URL

    return HttpResponse(status=200)

class StripeIntent(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer =stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs['pk']
            product = Products.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='sgd',
                customer=customer['id'],
                metadata={
                    "product_id": product_id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        
        except Exception as e:
            return JsonResponse({ 'error': str(e)})