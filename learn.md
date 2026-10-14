Phần 1: Danh sách câu hỏi
Nhóm A: Kiến trúc và request lifecycle
Kiến trúc MTV của Django là gì, khác gì với MVC truyền thống?
Vòng đời (lifecycle) của một HTTP request trong Django diễn ra thế nào?
Middleware là gì, hoạt động ra sao? Cho ví dụ ứng dụng.
WSGI và ASGI khác nhau như thế nào?
django-admin, manage.py và các lệnh quản lý dùng để làm gì?
Nhóm B: ORM và QuerySet
QuerySet là gì? "Lazy evaluation" của QuerySet nghĩa là gì?
select_related và prefetch_related khác nhau như thế nào?
N+1 query problem trong Django là gì, cách phát hiện và khắc phục?
Sự khác nhau giữa filter(), get(), exclude(), all()?
values(), values_list() và only(), defer() khác nhau ra sao?
annotate() và aggregate() khác nhau như thế nào?
Q object và F object dùng để làm gì?
Cách thực hiện transaction trong Django ORM?
bulk_create, bulk_update dùng khi nào, có hạn chế gì?
So sánh get_or_create và update_or_create.
QuerySet có được cache không? Cơ chế cache của QuerySet hoạt động thế nào?
Nhóm C: Model và migrations
Migration là gì, hoạt động thế nào? makemigrations và migrate khác nhau ra sao?
null=True và blank=True khác nhau như thế nào?
on_delete trong ForeignKey có những lựa chọn nào, ý nghĩa từng cái?
Quan hệ OneToOne, ForeignKey, ManyToMany khác nhau và dùng khi nào?
related_name dùng để làm gì?
Custom model manager và custom QuerySet là gì, khi nào dùng?
Cách xử lý một data migration (không chỉ đổi schema mà còn đổi dữ liệu)?
abstract base class, multi-table inheritance và proxy model khác nhau thế nào?
Nhóm D: View, form, serializer
Function-based view (FBV) và class-based view (CBV) khác nhau, ưu nhược điểm?
Django Form và ModelForm khác nhau như thế nào?
CSRF là gì, Django bảo vệ chống CSRF thế nào?
Signal trong Django là gì, dùng khi nào, có nhược điểm gì?
Trong Django REST Framework, serializer là gì? Serializer và ModelSerializer khác nhau ra sao?
Nhóm E: Authentication, security, session
Cơ chế authentication của Django hoạt động thế nào?
Session trong Django lưu ở đâu, hoạt động thế nào?
Django lưu password thế nào? Có an toàn không?
Các cơ chế bảo mật Django cung cấp sẵn (XSS, SQL injection, clickjacking...)?
Phân biệt authentication và authorization; permission và group trong Django.
Nhóm F: Performance, caching, async, deployment
Các tầng caching trong Django (per-view, template fragment, low-level cache API)?
Cách tối ưu hiệu năng ứng dụng Django khi truy vấn database chậm?
Celery dùng để làm gì trong dự án Django, khi nào cần?
Async view trong Django (từ 3.1+) hoạt động thế nào, có giới hạn gì?
DEBUG=True trong production có vấn đề gì? Checklist deploy an toàn gồm những gì?
Cách viết test trong Django (TestCase, Client, fixtures) và những điểm cần lưu ý?
Nhóm G: ORM nâng cao, DRF và phiên bản mới
Subquery, OuterRef và Exists dùng khi nào?
Xử lý QuerySet hàng trăm nghìn bản ghi mà không tốn bộ nhớ thế nào?
Meta.constraints (UniqueConstraint, CheckConstraint) dùng để làm gì?
Custom user model: vì sao nên tạo từ đầu, chọn AbstractUser hay AbstractBaseUser?
Làm việc nhóm gặp conflict migration thì xử lý thế nào? --merge, --fake, squash là gì?
Trong DRF, ViewSet và Router hoạt động thế nào?
DRF: authentication (JWT), pagination, throttling và versioning cấu hình thế nào, cần lưu ý gì?
GenericForeignKey là gì, ưu nhược điểm?
Django 5.x và 6.0 có những tính năng mới đáng chú ý nào?