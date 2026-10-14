from decimal import Decimal

from django.db.models import Count, F, Q, Sum
from django.test import TestCase
from django.utils import timezone

from shop.models import Customer, Order, OrderItem, Product


class AnnotateAggregateTests(TestCase):
    """
    Dữ liệu:
      P1 giá 10, P2 giá 20
      A: order1 paid      = P1 x2 + P2 x1 = 40
         order2 paid      = P2 x3         = 60
         order3 cancelled = P1 x1         = 10
      B: order4 paid      = P1 x1         = 10
         order5 pending   = P2 x2         = 40
      C: không có order
    """

    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        a, b, c = Customer.objects.bulk_create([
            Customer(email=f"{name}@vn.com", country="VN", created_at=now) for name in "abc"
        ])
        p1 = Product.objects.create(name="P1", price=Decimal("10"))
        p2 = Product.objects.create(name="P2", price=Decimal("20"))

        def order(customer, status, *items):
            o = Order.objects.create(customer=customer, status=status, created_at=now)
            OrderItem.objects.bulk_create([OrderItem(order=o, product=p, quantity=q) for p, q in items])

        order(a, "paid", (p1, 2), (p2, 1))
        order(a, "paid", (p2, 3))
        order(a, "cancelled", (p1, 1))
        order(b, "paid", (p1, 1))
        order(b, "pending", (p2, 2))

    def test_aggregate_total_revenue(self):
        # TODO: tổng tiền của TẤT CẢ order item (quantity * product.price)
        result = OrderItem.objects.aggregate(revenue = Sum(F('quantity') * F('product__price')))
        self.assertEqual(result, {"revenue": Decimal("160")})

    def test_annotate_order_count(self):
        # TODO: mỗi customer kèm số order (order_count)
        qs = Customer.objects.annotate(order_count = Count('orders__id'))
        self.assertEqual(
            {c.email: c.order_count for c in qs},
            {"a@vn.com": 3, "b@vn.com": 2, "c@vn.com": 0},
        )

    def test_group_by_status(self):
        # TODO: số order theo từng status
        qs = Order.objects.values('status').annotate(n=Count('id'))
        self.assertEqual(
            {row["status"]: row["n"] for row in qs},
            {"paid": 3, "cancelled": 1, "pending": 1},
        )

    def test_having(self):
        # TODO: customer có từ 2 order "paid" trở lên
        qs = Customer.objects.annotate(p = Count('orders__id', filter=Q(orders__status='paid'))).filter(p__gte = 2)
        self.assertEqual([c.email for c in qs], ["a@vn.com"])

    def test_top_spender_paid_only(self):
        # TODO: customer chi tiêu nhiều nhất, chỉ tính order "paid" (field: spent)
        top = (
            Customer.objects.annotate(
                spent=Sum(
                        F('orders__items__quantity') * F('orders__items__product__price'),
                        filter=Q(orders__status='paid')
                    )
                )
            .order_by(F('spent').desc(nulls_last=True))
            .first()
            )

        self.assertEqual((top.email, top.spent), ("a@vn.com", Decimal("100")))
