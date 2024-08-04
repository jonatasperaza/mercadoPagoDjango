from django.urls import path, include
from mercadoPago.views import CreatePixPaymentView, WebhookView
from django.contrib import admin

urlpatterns = [
    path('api/create_pix_payment/', CreatePixPaymentView.as_view(), name='create_pix_payment'),
    path('api/webhook/', WebhookView.as_view(), name='webhook'),
    path('admin/', admin.site.urls),
]
