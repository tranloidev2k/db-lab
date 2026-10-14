from django.db.models import FETCH_RAISE
from django.shortcuts import render
from rest_framework import generics

from shop.models import Order
from shop.serializers import OrderSerializer


# def order_list(request):
#     orders = Order.objects.order_by("-created_at")[:20]

#     # TODO 2: bật FETCH_RAISE cho `orders` để Django báo lỗi khi có lazy load FK

#     # TODO 3: sửa `orders` để hết N+1 (cả customer, items và product)

#     return render(request, "shop/order_list.html", {"orders": orders})


# class OrderListAPI(generics.ListAPIView):
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return (
#             Order.objects
#             # TODO 5 (D29): tối ưu để hết N+1 do serializer lồng nhau gây ra
#             .order_by("-created_at")[:20]
#         )


# ---------------- D25: FBV vs CBV ----------------
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.views.generic import ListView

from shop.models import Product


# TODO 1: chặn mọi method khác GET (POST/DELETE... phải trả 405) bằng 1 decorator
@require_GET
def product_list_fbv(request):
    products = Product.objects.order_by("name")

    # TODO 2: phân trang 20 sản phẩm/trang, số trang lấy từ query param ?page=
    #         (gợi ý: Paginator(...).get_page(...) — tự xử lý page sai/vượt quá)
    page_obj = Paginator(products, 20).get_page(request.GET.get("page"))

    return render(request, "shop/product_list.html", {
        "products": page_obj,   # Page object cũng iterate được như list
        "page_obj": page_obj,
    })


class ProductListView(ListView):
    # TODO 3: khai báo các thuộc tính để có kết quả GIỐNG HỆT product_list_fbv:
    #         model, ordering, paginate_by, template_name, context_object_name
    model = Product
    template_name = "shop/product_list.html"
    paginate_by = 20
    ordering = ["name"]
    context_object_name = "products"
