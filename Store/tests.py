from django.contrib.auth.models import User
from django.test import TestCase

from .models import Order, OrderItem, Product


class ViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser",
            email="",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            image="test.jpg",
            category="S",
        )

    def test_home_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_about_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/about/")
        self.assertEquals(response.status_code, 200)

    def test_contact_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/contact/")
        self.assertEquals(response.status_code, 200)

    def test_register_page_status_code(self):
        response = self.client.get("/register/")
        self.assertEquals(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get("/login/")
        self.assertEquals(response.status_code, 200)

    def test_logout_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/logout/")
        self.assertEquals(response.status_code, 200)

    def test_profile_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/profile/")
        self.assertEquals(response.status_code, 200)

    def test_edit_profile_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/edit_profile_page/")
        self.assertEquals(response.status_code, 200)

    def test_catalog_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/catalog/")
        self.assertEquals(response.status_code, 200)

    def test_product_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/product/1/")
        self.assertEquals(response.status_code, 200)

    def test_cart_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/cart/")
        self.assertEquals(response.status_code, 200)

    def test_add_to_cart_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/add_to_cart/1/")
        self.assertEquals(response.status_code, 200)

    def test_remove_from_cart_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/remove_from_cart/1/")
        self.assertEquals(response.status_code, 200)

    def test_remove_single_item_from_cart_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/remove_single_item_from_cart/1/")
        self.assertEquals(response.status_code, 200)

    def test_checkout_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/checkout/")
        self.assertEquals(response.status_code, 200)

    def test_catalog_category_page_status_code(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/catalog/S/")
        self.assertEquals(response.status_code, 200)


class ModelTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser",
            email="",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            image="test.jpg",
            category="S",
        )
        Order.objects.create(
            user=User.objects.get(username="testuser"),
            ordered=False,
            start_date="2021-01-01",
            ordered_date="2021-01-01",
        )
        OrderItem.objects.create(
            user=User.objects.get(username="testuser"),
            ordered=False,
            item=Product.objects.get(name="Test Product"),
            quantity=1,
        )

    def test_product_name(self):
        product = Product.objects.get(name="Test Product")
        self.assertEquals(product.name, "Test Product")

    def test_product_description(self):
        product = Product.objects.get(name="Test Product")
        self.assertEquals(product.description, "Test Description")

    def test_product_price(self):
        product = Product.objects.get(name="Test Product")
        self.assertEquals(product.price, 9.99)

    def test_product_image(self):
        product = Product.objects.get(name="Test Product")
        self.assertEquals(product.image, "test.jpg")

    def test_product_category(self):
        product = Product.objects.get(name="Test Product")
        self.assertEquals(product.category, "S")

    def test_order_user(self):
        order = Order.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order.user, User.objects.get(username="testuser"))

    def test_order_ordered(self):
        order = Order.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order.ordered, False)

    def test_order_item_user(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.user, User.objects.get(username="testuser"))

    def test_create_order_item_ordered(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.ordered, False)

    def test_create_order_item_item(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.item, Product.objects.get(name="Test Product"))

    def test_create_order_item_quantity(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.quantity, 1)

    def test_order_item_quantity(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.get_quantity(), 1)

    def test_order_item_total_item_price(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.get_total_item_price(), 9.99)

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(str(order_item), "1 of Test Product")

    def test_order_total(self):
        order = Order.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order.get_total(), 0)

    def test_order_str(self):
        order = Order.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(str(order), "testuser")

    def test_order_item_get_total_item_price(self):
        order_item = OrderItem.objects.get(user=User.objects.get(username="testuser"))
        self.assertEquals(order_item.get_total_item_price(), 9.99)
