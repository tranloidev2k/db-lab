from django.test import TestCase
from django.utils import timezone

from shop.models import Customer


class LazyQuerySetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        Customer.objects.bulk_create([
            Customer(email="a@vn.com", country="VN", created_at=now, is_verified=True),
            Customer(email="b@vn.com", country="VN", created_at=now, is_verified=False),
            Customer(email="c@us.com", country="US", created_at=now, is_verified=True),
        ])

    def test_building_queryset_runs_no_query(self):
        with self.assertNumQueries(0):
            # TODO: tạo qs: country="VN", bỏ khách chưa verify, sắp xếp created_at giảm dần
            qs = Customer.objects.filter(country="VN")
            qs = qs.exclude(is_verified=False)
            qs = qs.order_by("-created_at")

    def test_count_then_loop(self):
        qs = Customer.objects.filter(country="VN").order_by("-created_at")

        # TODO: điền số query đúng
        with self.assertNumQueries(2):
            qs.count()
            for c in qs[:5]:
                c.email

    def test_result_cache(self):
        qs = Customer.objects.filter(country="VN")

        with self.assertNumQueries(1):
            # TODO: dùng qs 2 lần (vd: lặp 2 lần) sao cho chỉ tốn 1 query
            for x in qs:
                print(x)

            print(len(qs))

            pass

        # TODO: sau khi qs đã được evaluate, len(qs) tốn bao nhiêu query?
        with self.assertNumQueries(0):
            self.assertEqual(len(qs), 2)

    def test_new_queryset_has_no_cache(self):
        # TODO: điền số query đúng
        with self.assertNumQueries(2):
            list(Customer.objects.all())
            list(Customer.objects.all())
