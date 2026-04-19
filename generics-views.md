# Django REST Framework (DRF) Generic Views - Complete Guide

---

# Why Generic Views?

Generic Views help you **avoid writing repetitive CRUD logic**.

Instead of writing everything manually (like APIView), DRF provides:

* Pre-built logic for common operations
* Clean and readable code
* Faster development

---

# Base Classes Hierarchy

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

# `views.py` Complete DRF Generic Views Example

```python
# DRF Generic Views Example (Complete Real-World Template)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from .models import ModelName
from .serializers import ModelNameSerializer


# ================================
# PAGINATION CLASS
# ================================
class StandardPagination(PageNumberPagination):
    """
    Controls how many records are returned per page
    """
    page_size = 10  # default items per page


# ================================
# LIST + CREATE API
# ================================
class ModelListCreateView(ListCreateAPIView):
    """
    GET  -> List all items
    POST -> Create new item
    """

    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer

    # Authentication (only logged-in users can access)
    permission_classes = [IsAuthenticated]

    # Pagination support
    pagination_class = StandardPagination

    # FILTERING (example: search or query params)
    def get_queryset(self):
        queryset = ModelName.objects.all()

        # Example: /items/?name=abc
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    # Auto assign logged-in user during creation
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom response format (optional)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        })


# ================================
# RETRIEVE + UPDATE + DELETE API
# ================================
class ModelDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET    -> Retrieve single item
    PUT    -> Update item
    PATCH  -> Partial update
    DELETE -> Delete item
    """

    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer

    # Only authenticated users can access
    permission_classes = [IsAuthenticated]

    # Change lookup field (default = pk)
    lookup_field = "pk"

    # Example: filtering access per user
    def get_queryset(self):
        return ModelName.objects.filter(user=self.request.user)

    # Soft delete instead of permanent delete
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
```



# Quick Summary

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
