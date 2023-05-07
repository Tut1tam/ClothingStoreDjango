from django.urls import path

from . import views
from .views import OrderSummaryView

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("catalog", views.catalog, name="catalog"),
    path("product/<int:product_id>", views.product, name="product"),
    path("cart", OrderSummaryView.as_view(), name="cart"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.register, name="register"),
    path("add_to_cart/<int:pk>", views.add_to_cart, name="add_to_cart"),
    path(
        "remove_single_item_from_cart/<int:pk>",
        views.remove_single_item_from_cart,
        name="remove_single_item_from_cart",
    ),
    path("profile", views.profile, name="profile"),
    path("edit_profile_page", views.edit_profile_page, name="edit_profile_page"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("catalog/<str:category>", views.catalog_category, name="catalog_category"),
]
# add custom 404 page
handler404 = "Store.views.error_404_view"
