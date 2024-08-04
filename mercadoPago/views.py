from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
import mercadopago
# {
#   "transaction_amount": 1,
#   "description": "Teste novo",
#   "paymentMethodId": "pix",
#   "email": "anthonylocheifc@gmail.com",
#   "identificationType": "CPF",
#   "number": 11345562926    
#}

sdk = mercadopago.SDK('APP_USR-942949289577962-050812-4019ece557a9f806f53560a6aa186e7a-1138000306')

class CreatePixPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        payment_data = {
            "transaction_amount": request.data.get('transaction_amount'),
            "description": request.data.get('description'),
            "payment_method_id": "pix",
            "payer": {
                "email": request.data.get('email'),
                "identification": {
                    "type": request.data.get('identificationType'),
                    "number": request.data.get('number') 
                }
            }
        }
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        print("payment_response", payment_response)
        print("payment", payment)

        if payment_response['status'] == 201:
            # Salvar pagamento no banco de dados
            payment_instance = Payment.objects.create(
                payment_id=payment['id'],
                transaction_amount=request.data.get('transaction_amount'),
                description=request.data.get('description'),
                status=payment['status'],
                payment_method="pix",
                payer_email=request.data.get('email')
            )

            serializer = PaymentSerializer(payment_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(payment, status=status.HTTP_400_BAD_REQUEST)

class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payment_id = request.data.get('data', {}).get('id')
        if payment_id:
            payment_response = sdk.payment().get(payment_id)
            payment = payment_response["response"]

            # Atualizar o pagamento no banco de dados
            payment_instance, created = Payment.objects.update_or_create(
                payment_id=payment['id'],
                defaults={
                    'transaction_amount': payment['transaction_amount'],
                    'description': payment['description'],
                    'status': payment['status'],
                    'payment_method': payment['payment_method_id'],
                    'payer_email': payment['payer']['email']
                }
            )

            return Response({'message': 'Payment updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid payment ID'}, status=status.HTTP_400_BAD_REQUEST)