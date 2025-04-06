from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from authentication.models import CustomUser, UserSubscription
import json
from datetime import date
from jobs.models import PostJobModel
from django.db.models import Q

def home(request):
    featured_jobs = PostJobModel.objects.all()

    search_query = request.GET.get('search', '')
    location = request.GET.get('location')

    if location:
        featured_jobs = featured_jobs.filter(location__icontains=location)

    if search_query:
        featured_jobs = featured_jobs.filter(
            Q(title__icontains=search_query) | Q(user__company_name__icontains=search_query)
        )

    work_mode = request.GET.getlist('workmode', '')
    if work_mode:
        featured_jobs = featured_jobs.filter(type__in=work_mode)

    featured_jobs = featured_jobs.order_by('-created_at')[:9]
    return render(request, 'index.html', {"jobs": featured_jobs})

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.user.is_authenticated == False:
        return JsonResponse({"message": "Please login first!"})
    if request.method == 'POST':
        data = json.loads(request.body)
        price_id = data.get('price_id')
        name = data.get('name')

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
                     'customer_email': request.user.email,
                     'name': name
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
        plan_name = session.get('metadata', {}).get('name')

        print("session.get('metadata', {}).get('name')", session.get('metadata', {}))

        try:
            user_id = session.get('metadata', {}).get('user_id')
            user = CustomUser.objects.get(id=int(user_id))
        except CustomUser.DoesNotExist:
            return HttpResponse(status=400)

        try:
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')

            subscription = stripe.Subscription.retrieve(
                subscription_id,
                expand=["items"]
            )

            invoice_id = session.get('invoice')
            if invoice_id:
                invoice = stripe.Invoice.retrieve(invoice_id)
                invoice_url = invoice.get('hosted_invoice_url')
                receipt_url = invoice.get('invoice_pdf')
                amount_paid = invoice.get('amount_paid', 0) / 100
                currency = invoice.get('currency')
            else:
                invoice_url = ''
                receipt_url = ''
                amount_paid = 0
                currency = 'usd' 

            payment_method = 'N/A'
            transaction_id = session.get('payment_intent') or 'N/A'

            print(subscription['items']['data'][0]['current_period_end'])

            UserSubscription.objects.create(
                user=user,
                stripe_subscription_id=subscription.id,
                stripe_customer_id=customer_id,
                plan_name=plan_name,
                amount_paid=amount_paid,
                currency=currency,
                payment_method=payment_method,
                transaction_id=transaction_id,
                invoice_url=invoice_url,
                receipt_url=receipt_url,
                start_date=date.fromtimestamp(subscription['start_date']),
                next_billing_date=date.fromtimestamp(subscription['items']['data'][0]['current_period_end']),
            )

        except Exception as e:
            print("❌ Error saving subscription:", e)
            return HttpResponse(status=500)


    return HttpResponse(status=200)