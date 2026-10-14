# DB schema — learn_db

`Customer 1──< Order 1──< OrderItem >──1 Product`

| Model (bảng) | Rows | Field | Kiểu | Giá trị / ghi chú |
|---|---|---|---|---|
| **Customer** (`shop_customer`) | 40k | `email` | CharField(255) | `a0@example.com`… |
| | | `country` | CharField(2) | VN, US, JP, AU, AE |
| | | `created_at` | DateTimeField | 2023-10 → 2026-10 |
| | | `is_verified` | BooleanField | tất cả = True |
| | | ← `orders` | reverse FK | |
| **Product** (`shop_product`) | 1k | `name` | CharField(200) | `Product 1`… |
| | | `price` | DecimalField(10,2) | 5.48 → 504.85 |
| | | ← `orderitem_set` | reverse FK | lookup: `orderitem__` |
| **Order** (`shop_order`) | 500k | `customer` | FK → Customer | `related_name="orders"` |
| | | `created_at` | DateTimeField | 2024-10 → 2026-10 |
| | | `status` | CharField(20) | paid, cancelled, pending |
| | | ← `items` | reverse FK | đúng 3 item/order |
| **OrderItem** (`shop_orderitem`) | 1.5M | `order` | FK → Order | `related_name="items"` |
| | | `product` | FK → Product | |
| | | `quantity` | PositiveIntegerField | 1 → 3 |

Tiền 1 dòng: `F("quantity") * F("product__price")`
