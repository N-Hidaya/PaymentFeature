import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
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
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN +'/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })