from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View

@login_required(login_url='/login/')
def product_ui(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {
        'products': products
    })


class PartnerLoginView(View):
    def get(self, request):
        return render(request, "auth/partner_login.html")