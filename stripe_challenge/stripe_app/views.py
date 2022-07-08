import json
import os

import stripe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Event

stripe.api_key = os.environ.get('STRIPE_API_KEY')


def index(request):
    if request.method == 'POST':
        product = stripe.Product.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.add_message(
            request, level=250,
            message=f'Product created successfully! product id: {product.id}',
            extra_tags='success'
        )
        return redirect('index')

    return render(request, 'index.html')


@csrf_exempt
def events(request):
    if request.method == 'POST':
        json_payload = json.loads(request.body)
        event = stripe.Event.construct_from(json_payload, stripe.api_key)
        Event.objects.create(event_type=event.type, event_id=event.data.object.id)
        return HttpResponse(status=200)
    
    # pagination
    page_num = request.GET.get('page')
    paginator = Paginator(Event.objects.all(), per_page=10)
    page_obj = paginator.get_page(page_num)

    context = {
        'page_obj': page_obj,
        'page_range': paginator.get_elided_page_range(page_obj.number)
    }
    return render(request, 'events.html', context)

