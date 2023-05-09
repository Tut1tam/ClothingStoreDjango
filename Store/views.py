import django.utils.timezone as timezone
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def anonymous_required(function=None, redirect_url="start"):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous, login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def index(request):
    return render(request, "Store/index.html")


def about(request):
    return render(request, "Store/about.html")


def contact(request):
    return render(request, "Store/contact.html")


def catalog(request):
    categories = [
        {"name": "All", "link": "/catalog", "id": ""},
        {"name": "Shirt", "link": "/catalog/S", "id": "S"},
        {"name": "Pants", "link": "/catalog/P", "id": "P"},
        {"name": "Sweater", "link": "/catalog/J", "id": "J"},
        {"name": "Sweatshirt", "link": "/catalog/SW", "id": "SW"},
        {"name": "Shoes", "link": "/catalog/SH", "id": "SH"},
        {"name": "Accessories", "link": "/catalog/A", "id": "A"},
        {"name": "Other", "link": "/catalog/O", "id": "O"},
    ]
    category = ""
    products = Product.objects.all()
    context = {"products": products, "categories": categories, "category": category}
    return render(request, "Store/catalog.html", context=context)


def product(request, product_id):
    if Product.objects.filter(id=product_id).exists() is False:
        return render(request, "Store/404.html")
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "Store/product.html", context=context)


@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=product,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("cart")
        else:
            order.items.add(order_item)
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        return redirect("cart")


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            return redirect("cart")
        else:
            return redirect("product", pk=pk)
    else:
        return redirect("product", pk=pk)


@login_required
def cart(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {"object": order}
        return render(request, "Store/cart.html", context)
    except ObjectDoesNotExist:
        return render(request, "Store/cart.html", context={"object": None})


@anonymous_required(redirect_url="index")
def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("catalog")
        else:
            return redirect("login")
    return render(request, "Store/login.html")


@anonymous_required(redirect_url="index")
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if password1 == password2:
            if auth.models.User.objects.filter(username=username).exists():
                return redirect("register")
            elif auth.models.User.objects.filter(email=email).exists():
                return redirect("register")
            else:
                user = auth.models.User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect("index")
        else:
            return redirect("register")
    return render(request, "Store/register.html")


@login_required
def logout_request(request):
    logout(request)
    return redirect("index")


@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered=True)
    order_items = OrderItem.objects.filter(user=user, ordered=True)
    context = {"orders": orders, "order_items": order_items, "user": user}
    return render(
        request,
        "Store/profile.html",
        context=context,
    )


def error_404_view(request, exception):
    return render(request, "Store/404.html")


@login_required
def edit_profile_page(request):
    user = request.user
    context = {"user": user}
    return render(request, "Store/edit_profile.html", context=context)


@login_required
def edit_profile(request):
    user = auth.models.User.objects.get(username=request.user)
    username = request.user
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)
            return redirect("profile")
    return render(request, "Store/edit_profile.html")


def catalog_category(request, category):
    categories = [
        {"name": "All", "link": "/catalog", "id": ""},
        {"name": "Shirt", "link": "/catalog/S", "id": "S"},
        {"name": "Pants", "link": "/catalog/P", "id": "P"},
        {"name": "Sweater", "link": "/catalog/J", "id": "J"},
        {"name": "Sweatshirt", "link": "/catalog/SW", "id": "SW"},
        {"name": "Shoes", "link": "/catalog/SH", "id": "SH"},
        {"name": "Accessories", "link": "/catalog/A", "id": "A"},
        {"name": "Other", "link": "/catalog/O", "id": "O"},
    ]
    if category not in ["S", "P", "J", "SW", "SH", "A", "O", ""]:
        return render(request, "Store/404.html")
    products = Product.objects.filter(category=category)
    context = {"products": products, "category": category, "categories": categories}
    return render(request, "Store/catalog.html", context=context)


@login_required
def checkout(request):
    if request.method == "POST":
        user = request.user
        order = Order.objects.get(user=user, ordered=False)
        order.ordered = True
        order.save()
        return redirect("profile")
    order = Order.objects.get(user=request.user, ordered=False)
    context = {"order": order}
    return render(request, "Store/checkout.html", context=context)
