"""B2 + B3 — N+1 query, select_related vs prefetch_related"""
from django.db.models import Prefetch

from lab import show_sql, title

from shop.models import Order, OrderItem

title("1. N+1 với ForeignKey: Order -> customer")
with show_sql("KHÔNG tối ưu", max_sql=3):
    for o in Order.objects.order_by("id")[:50]:
        o.customer.email          # mỗi order thêm 1 query -> 1 + 50

with show_sql("select_related('customer') -> JOIN", max_sql=1):
    for o in Order.objects.select_related("customer").order_by("id")[:50]:
        o.customer.email

title("2. N+1 với quan hệ ngược (1-nhiều): Order -> items")
with show_sql("KHÔNG tối ưu", max_sql=3):
    for o in Order.objects.order_by("id")[:50]:
        list(o.items.all())

with show_sql("prefetch_related('items') -> 2 query, nối bằng Python"):
    for o in Order.objects.prefetch_related("items").order_by("id")[:50]:
        list(o.items.all())

title("3. Kết hợp: order -> customer (JOIN) + items -> product (JOIN trong prefetch)")
with show_sql("select_related + Prefetch(queryset=...)"):
    qs = (
        Order.objects.select_related("customer")
        .prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product"))
        )
        .order_by("id")[:50]
    )
    for o in qs:
        o.customer.email
        for it in o.items.all():
            it.product.name

title("4. Bẫy: filter() sau prefetch làm MẤT prefetch")
with show_sql("o.items.filter(quantity__gt=1) -> query mới mỗi vòng", print_sql=False):
    for o in Order.objects.prefetch_related("items").order_by("id")[:50]:
        list(o.items.filter(quantity__gt=1))
