from decimal import Decimal

from django.db.models import Prefetch
from django.test import TestCase
from django.utils import timezone

from shop.models import Customer, Order, OrderItem, Product


class SelectPrefetchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        customers = Customer.objects.bulk_create([
            Customer(email=f"c{i}@vn.com", country="VN", created_at=now) for i in range(3)
        ])
        products = Product.objects.bulk_create([
            Product(name=f"Product {i}", price=Decimal("10.00") * (i + 1)) for i in range(3)
        ])
        orders = Order.objects.bulk_create([
            Order(customer=customers[i % 3], created_at=now, status="paid") for i in range(10)
        ])
        OrderItem.objects.bulk_create([
            OrderItem(order=o, product=p, quantity=q)
            for o in orders
            for p, q in zip(products, [1, 2, 3])
        ])

    def test_select_related(self):
        with self.assertNumQueries(1):
            # TODO: lấy tất cả order kèm customer
            qs = Order.objects.select_related('customer').all()
            emails = [o.customer.email for o in qs]
        self.assertEqual(len(emails), 10)

    def test_prefetch_related(self):
        with self.assertNumQueries(2):
            # TODO: lấy tất cả order kèm items
            qs = Order.objects.prefetch_related('items').all()
            total = sum(len(o.items.all()) for o in qs)
        self.assertEqual(total, 30)

    def test_select_and_prefetch_combined(self):
        with self.assertNumQueries(2):
            # TODO: order -> customer, order -> items -> product
            # gợi ý: Prefetch("items", queryset=OrderItem.objects....)
            qs = Order.objects.select_related('customer').prefetch_related(
                Prefetch('items', queryset=OrderItem.objects.select_related('product'))
            )
            for o in qs:
                o.customer.email
                for item in o.items.all():
                    item.product.name

    def test_prefetch_with_filter(self):
        with self.assertNumQueries(2):
            # TODO: kèm theo mỗi order chỉ những item có quantity >= 2,
            # lưu vào thuộc tính o.big_items (dùng to_attr)
            qs = Order.objects.prefetch_related(
                Prefetch(
                    'items',
                    queryset=OrderItem.objects.filter(quantity__gte=2),
                    to_attr='big_items',
                )
            )
            counts = [len(o.big_items) for o in qs]
        self.assertEqual(counts, [2] * 10)
