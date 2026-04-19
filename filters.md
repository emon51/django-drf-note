## filters.py
```python
import django_filters
from .models import ModelName


class ModelNameFilter(django_filters.FilterSet):
    """
    Comprehensive FilterSet for ModelName

    Covers:
    - Search filtering
    - Exact match filtering
    - Range filtering (number/date)
    - Boolean filtering
    - Ordering support
    """

    # 1. Case-insensitive search (most common)
    search = django_filters.CharFilter(
        field_name="<field_name>",
        lookup_expr="icontains"
    )

    # 2. Exact match filtering
    exact_field = django_filters.CharFilter(
        field_name="<field_name>",
        lookup_expr="exact"
    )

    # 3. Numeric range filtering (greater than or equal)
    min_value = django_filters.NumberFilter(
        field_name="<field_name>",
        lookup_expr="gte"
    )

    # 4. Numeric range filtering (less than or equal)
    max_value = django_filters.NumberFilter(
        field_name="<field_name>",
        lookup_expr="lte"
    )

    # 5. Date filtering (after)
    date_after = django_filters.DateFilter(
        field_name="<field_name>",
        lookup_expr="gte"
    )

    # 6. Date filtering (before)
    date_before = django_filters.DateFilter(
        field_name="<field_name>",
        lookup_expr="lte"
    )

    # 7. Boolean filtering (true/false)
    is_active = django_filters.BooleanFilter(
        field_name="<field_name>"
    )

    # 8. Ordering filter (sorting support)
    ordering = django_filters.OrderingFilter(
        fields=(
            ("<field_name>", "<field_name>"),
            ("<field_name>", "<field_name>"),
        )
    )

    class Meta:
        """
        Meta:
        - model → attaches filter to model
        - fields → auto-generated exact filters only
        """

        model = ModelName

        # These are AUTO filters (exact match only)
        # Custom filters above are NOT included here
        fields = [
            "<field_name_1>",
            "<field_name_2>"
        ]
```

## views.py
```python
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import ModelName
from .serializers import ModelNameSerializer
from .filters import ModelNameFilter


class ModelNameListView(ListAPIView):
    """
    List API with full filtering support

    Features:
    - django-filter integration
    - custom FilterSet usage
    - scalable query handling
    """

    # Base queryset
    queryset = ModelName.objects.all()

    # Serializer for response formatting
    serializer_class = ModelNameSerializer

    # Enable filtering backend
    filter_backends = [DjangoFilterBackend]

    # Attach custom FilterSet
    filterset_class = ModelNameFilter

    """
    Alternative (less common):

    filterset_fields = ["field1", "field2"]

    #Used for simple exact filtering only
    """
```
