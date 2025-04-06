from django.shortcuts import redirect
from authentication.models import UserSubscription
from django.utils.timezone import now

def subscription_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            if not subscription.status == 'active' or subscription.next_billing_date < now():
                return redirect('pricing_page')
        except UserSubscription.DoesNotExist:
            return redirect('pricing_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

