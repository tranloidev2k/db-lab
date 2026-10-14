"""B1 — QuerySet là gì? Lazy evaluation là gì? (+ B16: cache của QuerySet)"""
from lab import show_sql, title

from shop.models import Customer

title("1. Tạo QuerySet + filter + order_by: CHƯA chạy query nào")
with show_sql("build queryset"):
    qs = Customer.objects.filter(country="VN").exclude(is_verified=False).order_by("-created_at")
print("SQL Django sẽ chạy khi cần:\n  ", qs.query)

title("2. Query chỉ chạy khi QuerySet được 'evaluate'")
with show_sql("list(qs[:3])"):
    first3 = list(qs[:3])        # slicing -> LIMIT 3, iterate -> chạy
with show_sql("qs.count()"):
    qs.count()                   # SELECT COUNT(*) — không load object
with show_sql("qs.exists()"):
    qs.exists()                  # SELECT 1 ... LIMIT 1

title("3. Cache: cùng 1 QuerySet object, iterate 2 lần")
qs = Customer.objects.filter(country="VN")[:100]
with show_sql("lần 1: list(qs)", print_sql=False):
    list(qs)
with show_sql("lần 2: list(qs) -> dùng _result_cache", print_sql=False):
    list(qs)

title("4. Cái bẫy: tạo QuerySet mới mỗi lần -> KHÔNG có cache")
with show_sql("Customer.objects.all()[:100] x2", print_sql=False):
    list(Customer.objects.all()[:100])
    list(Customer.objects.all()[:100])

title("5. Indexing qs[0] trên QuerySet chưa evaluate -> mỗi lần 1 query")
qs = Customer.objects.order_by("id")
with show_sql("qs[0], qs[1], qs[2]", print_sql=False):
    qs[0]; qs[1]; qs[2]
list(qs[:3])  # chú ý: slicing tạo QuerySet MỚI, không làm đầy cache của qs
