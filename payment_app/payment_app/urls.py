"""
URL configuration for payment_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from products.views import (checkoutSessionView,
                            ProductLandingPage, SuccessView, CancelView, webhook_view, StripeIntent)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-payment-intent/<pk>/', StripeIntent.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', webhook_view, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('', ProductLandingPage.as_view(), name='landing-page'),
    path('checkout-session/<pk>/', checkoutSessionView.as_view(), name='checkout-session')
]
