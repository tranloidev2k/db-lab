from datetime import timedelta

from django.db.models import Exists, OuterRef, Subquery
from django.test import TestCase
from django.utils import timezone

from shop.models import Customer, Order


class SubqueryExistsTests(TestCase):
    """
    Dữ liệu (t1 < t2 < t3):
      A: pending (t1), pending (t2), paid (t3)  -> order mới nhất: paid
      B: cancelled (t2)                         -> order mới nhất: cancelled
      C: không có order
    """

    @classmethod
    def setUpTestData(cls):
        t1 = timezone.now()
        t2, t3 = t1 + timedelta(days=1), t1 + timedelta(days=2)
        a, b, c = Customer.objects.bulk_create([
            Customer(email=f"{name}@vn.com", country="VN", created_at=t1) for name in "abc"
        ])
        Order.objects.bulk_create([
            Order(customer=a, status="pending", created_at=t1),
            Order(customer=a, status="pending", created_at=t2),
            Order(customer=a, status="paid", created_at=t3),
            Order(customer=b, status="cancelled", created_at=t2),
        ])

    def test_join_duplicates(self):
        # Không cần sửa: cách A bị trùng dòng vì JOIN
        qs = Customer.objects.filter(orders__status="pending").order_by("email")
        self.assertEqual([c.email for c in qs], ["a@vn.com", "a@vn.com"])

    def test_exists(self):
        # TODO: customer có ít nhất 1 order "pending", dùng Exists (không trùng, không distinct)
        qs = Customer.objects.filter(Exists(Order.objects.filter(customer=OuterRef('pk'), status='pending')))
        self.assertEqual([c.email for c in qs.order_by("email")], ["a@vn.com"])

    def test_not_exists(self):
        # TODO: customer KHÔNG có order "paid" nào
        qs = Customer.objects.filter(~Exists(Order.objects.filter(customer=OuterRef('pk'), status='paid')))
        self.assertEqual([c.email for c in qs.order_by("email")], ["b@vn.com", "c@vn.com"])

    def test_annotate_exists(self):
        # TODO: mỗi customer kèm cột boolean has_pending
        qs = Customer.objects.annotate(has_pending = (Exists(Order.objects.filter(customer=OuterRef('pk'), status='pending'))))
        self.assertEqual(
            {c.email: c.has_pending for c in qs},
            {"a@vn.com": True, "b@vn.com": False, "c@vn.com": False},
        )

    def test_last_order_status(self):
        # TODO: mỗi customer kèm status của order mới nhất (last_status), dùng Subquery
        last_order = Order.objects.filter(customer=OuterRef('pk')).order_by('-created_at').values('status')[:1]
        qs= Customer.objects.annotate(last_status = Subquery(last_order))

        self.assertEqual(
            {c.email: c.last_status for c in qs},
            {"a@vn.com": "paid", "b@vn.com": "cancelled", "c@vn.com": None},
        )
