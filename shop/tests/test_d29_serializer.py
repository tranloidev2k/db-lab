from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from shop.models import Customer, Order, OrderItem, Product
from shop.serializers import ProductSerializer


class ProductSerializerTests(TestCase):
    def test_serialize(self):
        p = Product.objects.create(name="P1", price=Decimal("10.50"))
        # DecimalField được trả về dạng string để không mất độ chính xác
        self.assertEqual(ProductSerializer(p).data, {"id": p.id, "name": "P1", "price": "10.50"})

    def test_validate_negative_price(self):
        s = ProductSerializer(data={"name": "P1", "price": "-1"})
        self.assertFalse(s.is_valid())
        self.assertIn("price", s.errors)

    def test_validate_name_too_long(self):
        s = ProductSerializer(data={"name": "x" * 201, "price": "1"})
        self.assertFalse(s.is_valid())
        self.assertIn("name", s.errors)

    def test_create(self):
        s = ProductSerializer(data={"name": "P1", "price": "9.99"})
        self.assertTrue(s.is_valid(), s.errors)
        p = s.save()
        self.assertEqual((p.name, p.price), ("P1", Decimal("9.99")))
        self.assertEqual(Product.objects.count(), 1)


class OrderListAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        c = Customer.objects.create(email="a@vn.com", country="VN", created_at=now)
        p = Product.objects.create(name="P1", price=Decimal("10"))
        for _ in range(5):
            o = Order.objects.create(customer=c, status="paid", created_at=now)
            OrderItem.objects.create(order=o, product=p, quantity=2)

    def test_response_shape(self):
        res = APIClient().get("/api/orders/")
        self.assertEqual(res.status_code, 200)
        first = res.json()[0]
        self.assertEqual(first["customer_email"], "a@vn.com")
        self.assertEqual(first["items"], [{"product_name": "P1", "quantity": 2}])

    def test_no_n_plus_one(self):
        with self.assertNumQueries(2):
            APIClient().get("/api/orders/")
