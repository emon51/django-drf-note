# Django REST Framework (DRF) Generic Views - Complete Guide

---

# 1. Why Generic Views?

Generic Views help you **avoid writing repetitive CRUD logic**.

Instead of writing everything manually (like APIView), DRF provides:

* Pre-built logic for common operations
* Clean and readable code
* Faster development

---

# 2. Base Classes Hierarchy

```
APIView
   ↑
GenericAPIView
   ↑
Mixins (Create, List, Update, Delete)
   ↑
Concrete Generic Views (ListCreateAPIView, etc.)
```

---

# 3. GenericAPIView (Core)

This is the **foundation class**.

### Basic Syntax 
```python
# List + Create API (ListCreateAPIView)
from rest_framework.generics import ListCreateAPIView

from .models import ModelName
from .serializers import ModelNameSerializer


class ModelNameListCreateView(ListCreateAPIView):
    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer


# Retrieve + Update + Delete API
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import ModelName
from .serializers import ModelNameSerializer


class ModelNameDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer



# URL Pattern
from django.urls import path

from .views import ModelNameListCreateView, ModelNameDetailView

urlpatterns = [
    path('items/', ModelNameListCreateView.as_view()),
    path('items/<int:pk>/', ModelNameDetailView.as_view()),
]
```



































```python
from rest_framework.generics import GenericAPIView

class StudentView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

### Important Attributes

```python
queryset = Model.objects.all()
serializer_class = MySerializer
lookup_field = 'pk'  # default
```

### Important Methods

```python
def get_queryset(self):
    return Student.objects.filter(active=True)


def get_serializer_class(self):
    return StudentSerializer


def get_object(self):
    return self.get_queryset().get(pk=self.kwargs['pk'])
```

---

# 4. Mixins (Add Functionality)

Mixins provide **specific behaviors**.

## ListModelMixin

```python
from rest_framework.mixins import ListModelMixin

class StudentListView(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        return self.list(request)
```

## CreateModelMixin

```python
class StudentCreateView(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request):
        return self.create(request)
```

## RetrieveModelMixin

```python
class StudentDetailView(GenericAPIView, RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
```

## UpdateModelMixin

```python
class StudentUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, pk):
        return self.update(request, pk=pk)
```

## DestroyModelMixin

```python
class StudentDeleteView(GenericAPIView, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
```

---

# 5. Concrete Generic Views (Most Important)

These are **ready-made views** combining mixins + GenericAPIView.

---

## 1. ListAPIView (GET all)

```python
from rest_framework.generics import ListAPIView

class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 2. CreateAPIView (POST)

```python
from rest_framework.generics import CreateAPIView

class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 3. RetrieveAPIView (GET one)

```python
class StudentDetailView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 4. UpdateAPIView (PUT/PATCH)

```python
class StudentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 5. DestroyAPIView (DELETE)

```python
class StudentDeleteView(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 6. ListCreateAPIView (GET + POST)

```python
class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

## 7. RetrieveUpdateDestroyAPIView (GET + PUT + DELETE)

```python
class StudentRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

---

# 6. URL Configuration

```python
from django.urls import path

urlpatterns = [
    path('students/', StudentListCreateView.as_view()),
    path('students/<int:pk>/', StudentRUDView.as_view()),
]
```

---

# 7. Common Customizations (Very Important)

## 1. Filtering Data

```python
def get_queryset(self):
    user = self.request.user
    return Student.objects.filter(user=user)
```

---

## 2. Custom Response Logic

```python
def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    return Response({
        "count": len(serializer.data),
        "data": serializer.data
    })
```

---

## 3. Perform Create Hook

```python
def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)
```

---

## 4. Perform Update Hook

```python
def perform_update(self, serializer):
    serializer.save(updated_by=self.request.user)
```

---

## 5. Perform Destroy Hook

```python
def perform_destroy(self, instance):
    instance.delete()
```

---

# 8. Permissions & Authentication

```python
from rest_framework.permissions import IsAuthenticated

class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
```

---

# 9. Pagination (Quick Use)

```python
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 10

class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = MyPagination
```

---

# 10. Real-World Use Cases

## Case 1: Simple CRUD API

Use:

* ListCreateAPIView
* RetrieveUpdateDestroyAPIView

---

## Case 2: User-specific Data

```python
def get_queryset(self):
    return Student.objects.filter(user=self.request.user)
```

---

## Case 3: Admin vs User Serializer

```python
def get_serializer_class(self):
    if self.request.user.is_staff:
        return AdminSerializer
    return StudentSerializer
```

---

## Case 4: Soft Delete

```python
def perform_destroy(self, instance):
    instance.is_deleted = True
    instance.save()
```

---

# 11. Best Practices

* Use **concrete generic views** for most cases
* Override only when needed
* Keep logic in:

  * serializers → validation
  * views → request handling
* Use `get_queryset()` instead of hardcoding queryset
* Always use permissions

---

# 12. When NOT to Use Generic Views

Avoid Generic Views when:

* Complex business logic
* Multiple models in one API
* Highly customized workflows

→ Use **APIView instead**

---

# 13. Quick Summary

| Task                       | View                         |
| -------------------------- | ---------------------------- |
| List                       | ListAPIView                  |
| Create                     | CreateAPIView                |
| Retrieve                   | RetrieveAPIView              |
| Update                     | UpdateAPIView                |
| Delete                     | DestroyAPIView               |
| List + Create              | ListCreateAPIView            |
| Retrieve + Update + Delete | RetrieveUpdateDestroyAPIView |

---
