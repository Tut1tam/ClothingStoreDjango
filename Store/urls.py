from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("about", views.about, name="about"),
    # path("contact", views.contact, name="contact"),
    # path("products", views.products, name="products"),
    # path("product/<int:product_id>", views.product, name="product"),
    # path("cart", views.cart, name="cart"),
    # path("checkout", views.checkout, name="checkout"),
    # path("login", views.login_request, name="login"),
    # path("logout", views.logout_request, name="logout"),
    # path("register", views.register, name="register"),
]
