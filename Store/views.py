from django.shortcuts import render


def index(request):
    return render(request, "Store/index.html")


def about(request):
    return render(request, "Store/about.html")


def contact(request):
    return render(request, "Store/contact.html")


# def faq(request):
#     return render(request, "Store/faq.html")


# def products(request):
#     return render(request, "Store/products.html")


# def product(request, product_id):
#     return render(request, "Store/product.html")


# def cart(request):
#     return render(request, "Store/cart.html")


# def checkout(request):
#     return render(request, "Store/checkout.html")


# def login_request(request):
#     return render(request, "Store/login.html")


# def logout_request(request):
#     return render(request, "Store/logout.html")


# def register(request):
#     return render(request, "Store/register.html")
