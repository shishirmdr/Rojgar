from django.shortcuts import render, redirect
from .forms import SellerForm
from .models import Seller
from django.contrib.auth.models import User
from django.db import IntegrityError

def seller_create_view(request):
    form = SellerForm()
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()



    context = {
        'form': form
    }
    return render(request, "sellers/seller_create.html", context)

def seller_detail_view(request):
    obj = Seller.objects.get(id=1)

    context= {
        'object': obj
    }
    return render(request, "sellers/seller_detail.html", context)


def seller(request):
    context = {
        'user': User
    }
    return render(request, "sellers/seller.html", context)


