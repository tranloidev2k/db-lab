from django.conf import settings
from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('orders/', views.order_list),
    # path('api/orders/', views.OrderListAPI.as_view()),
    path('products/fbv/', views.product_list_fbv),
    path('products/cbv/', views.ProductListView.as_view()),
]

if settings.DEBUG and not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
