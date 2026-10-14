"""Helper dùng chung cho các bài thực hành.

Cách chạy một bài:  .venv/bin/python practice/b01_lazy_queryset.py
"""
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext


def title(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}")


@contextmanager
def show_sql(label, print_sql=True, max_sql=5):
    """Đếm số query + thời gian của đoạn code bên trong, in SQL ra."""
    start = time.perf_counter()
    with CaptureQueriesContext(connection) as ctx:
        yield ctx
    ms = (time.perf_counter() - start) * 1000
    print(f"\n--- {label}: {len(ctx.captured_queries)} query, {ms:.1f} ms")
    if print_sql:
        for q in ctx.captured_queries[:max_sql]:
            print("   SQL:", q["sql"][:300])
        if len(ctx.captured_queries) > max_sql:
            print(f"   ... (+{len(ctx.captured_queries) - max_sql} query nữa)")


def explain(qs, analyze=False):
    """In EXPLAIN của PostgreSQL cho một QuerySet."""
    print(qs.explain(analyze=analyze))
