from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from authentication.models import CustomUser, UserSubscription
from django.contrib.auth.decorators import login_required
import json
import datetime


def home(request):
    return render(request, 'index.html')

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.user.is_authenticated == False:
        return JsonResponse({"message": "Please login first!"})
    if request.method == 'POST':
        data = json.loads(request.body)
        price_id = data.get('price_id')

        try:
            session = stripe.checkout.Session.create(
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                metadata={
                     'user_id': request.user.id,
                     'customer_email': request.user.email
                }
            )
            return JsonResponse({'checkout_url': session.url})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("Webhook verification failed:", e)
        return HttpResponse(status=400)

    print("✅ Event type:", event['type'])

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=400)

    try:
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')

        invoice = stripe.Invoice.retrieve(session['invoice'])
        payment_intent_id = invoice['payment_intent']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        subscription = stripe.Subscription.retrieve(subscription_id)

        UserSubscription.objects.create(
            user=user,
            stripe_subscription_id=subscription.id,
            stripe_customer_id=customer_id,
            plan_name=subscription['items']['data'][0]['price'].get('nickname', 'Custom Plan'),
            amount_paid=invoice['amount_paid'] / 100,
            currency=invoice['currency'],
            payment_method=payment_intent['payment_method_types'][0],
            transaction_id=payment_intent['id'],
            invoice_url=invoice['hosted_invoice_url'],
            receipt_url=invoice['invoice_pdf'],
            start_date=datetime.fromtimestamp(subscription['start_date']),
            next_billing_date=datetime.fromtimestamp(subscription['current_period_end']),
        )
    except Exception as e:
        print("❌ Error saving subscription:", e)
        return HttpResponse(status=500)


    return HttpResponse(status=200)