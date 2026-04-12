# 1. DRF Error Fix: `unexpected keyword argument 'pk'`

## Error

```
TypeError: <view_name>() got an unexpected keyword argument 'pk'
```

---

## Cause

Django passes URL parameters (like `pk`) to the view as keyword arguments.
If the view function does **not** accept the same parameter name → error occurs.

---

## Typical Mismatch

### URL

```python
path("students/<int:pk>/", views.studentDetailView)
```

### View (Wrong)

```python
@api_view(["GET"])
def studentDetailView(request, id):
    ...
```

---

## Fix (Match names)

### Option A (Recommended)

```python
@api_view(["GET"])
def studentDetailView(request, pk):
    student = StudentModel.objects.get(pk=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)
```

### Option B (Change URL)

```python
path("students/<int:id>/", views.studentDetailView)
```

---

## Best Practice

Use `get_object_or_404` to avoid manual try/except:

```python
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def studentDetailView(request, pk):
    student = get_object_or_404(StudentModel, pk=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)
```

---

## Golden Rule

```
URL parameter name == view function parameter name
```

---


---

## Quick Checklist

* [ ] URL uses `<int:pk>` or `<int:id>`
* [ ] View function has same parameter name
* [ ] Use `pk` consistently across project

---

## URL Pattern ↔ View Parameter Mapping

| URL Pattern | View Must Have |
| ----------- | -------------- |
| `<int:pk>`  | `pk` parameter |
| `<str:id>`  | `id` parameter |

---
