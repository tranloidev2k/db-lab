from decimal import Decimal

from django.test import TestCase

from shop.models import Product

URLS = ["/products/fbv/", "/products/cbv/"]


class ProductListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 45 sản phẩm -> 3 trang (20, 20, 5)
        Product.objects.bulk_create(
            Product(name=f"P{i:02d}", price=Decimal("1")) for i in range(45)
        )

    def test_first_page(self):
        for url in URLS:
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertEqual(res.status_code, 200)
                names = [p.name for p in res.context["products"]]
                self.assertEqual(names, [f"P{i:02d}" for i in range(20)])

    def test_last_page(self):
        for url in URLS:
            with self.subTest(url=url):
                res = self.client.get(url, {"page": 3})
                self.assertEqual(len(res.context["products"]), 5)
                self.assertEqual(res.context["page_obj"].number, 3)

    def test_post_not_allowed(self):
        for url in URLS:
            with self.subTest(url=url):
                self.assertEqual(self.client.post(url).status_code, 405)
