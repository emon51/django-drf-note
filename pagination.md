# Django REST Framework (DRF) Pagination - Quick Guide

---

# What is Pagination?

Pagination splits large datasets into **smaller chunks (pages)**.

Instead of returning all data at once:

```
/items/ -> 1000 records ----> Wrong 
```

Return limited data:

```
/items/?page=1 -> 10 records ----> Correct
```


---

# Default Pagination Types in DRF

| Type                  | Description              |
| --------------------- | ------------------------ |
| PageNumberPagination  | Page-based (?page=1)     |
| LimitOffsetPagination | limit + offset           |
| CursorPagination      | efficient for large data |

---

# 1. PageNumberPagination (Most Common)

## Create Pagination Class

```python
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 10
```

## Use in View

```python
class ItemListView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    pagination_class = MyPagination
```

## Request

```
/items/?page=1
```

---

# 2. LimitOffsetPagination

```python
from rest_framework.pagination import LimitOffsetPagination

class MyPagination(LimitOffsetPagination):
    default_limit = 10
```

## Request

```
/items/?limit=10&offset=20
```

---

# 3. CursorPagination (Advanced)

```python
from rest_framework.pagination import CursorPagination

class MyPagination(CursorPagination):
    page_size = 10
    ordering = '-id'
```

- Best for large datasets
- No duplicate data issue

---

# Default Response Format

```json
{
  "count": 100,
  "next": "http://api/items/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

# Common Customization

## Change page size dynamically

```python
class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
```

## Request

```
/items/?page=1&page_size=5
```

---

# Set Global Pagination (settings.py) - works for all views

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

# When to Use Which?

| Situation            | Use                   |
| -------------------- | --------------------- |
| Normal API           | PageNumberPagination  |
| Custom skip/limit    | LimitOffsetPagination |
| Large real-time data | CursorPagination      |

---

# Best Practice

- Use PageNumberPagination in most cases
- Set global pagination
- Avoid returning huge datasets

---

Pagination = "return data in small pages instead of all at once"
