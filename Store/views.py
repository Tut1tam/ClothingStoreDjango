import django.utils.timezone as timezone
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Order, OrderItem, Product


def index(request):
    return render(request, "Store/index.html")


def about(request):
    return render(request, "Store/about.html")


def contact(request):
    return render(request, "Store/contact.html")


def catalog(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "Store/catalog.html", context=context)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    image = product.image
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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(self.request, "Store/cart.html", context)
        except ObjectDoesNotExist:
            return redirect("/")


def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            return redirect("login")
    return render(request, "Store/login.html")


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
    return render(
        request,
        "Store/profile.html",
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
