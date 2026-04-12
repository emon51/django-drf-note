# Django Model Field Validations - Notes

##  Overview

Model field validation ensures that data stored in the database is **correct, safe, and consistent**. Django provides built-in validators and also allows custom validation logic.

---

# Required Packages / Imports

```python
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
    FileExtensionValidator
)
from django.core.exceptions import ValidationError
```

---

# Universal Syntax (Model Field with Validators)

```python
field_name = models.FieldType(
    options...,
    validators=[
        Validator1,
        Validator2,
        ...
    ]
)
```

---

# Common Field Validations

---

## 1. Integer / Numeric Fields

### ✔ Use Case:

* Age, price, quantity

```python
age = models.IntegerField(
    validators=[
        MinValueValidator(18),
        MaxValueValidator(60)
    ]
)
```

---

## 2. CharField / TextField

### ✔ Use Case:

* Name, username, description

```python
name = models.CharField(
    max_length=100,
    validators=[
        MinLengthValidator(3),
        RegexValidator(
            regex=r'^[A-Za-z ]+$',
            message="Only letters and spaces allowed"
        )
    ]
)
```

---

## 3. Email Field

```python
email = models.EmailField(unique=True)
```

✔ Built-in validation

---

## 4. URL Field

```python
website = models.URLField()
```

---

## 5. File Field

```python
file = models.FileField(
    validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'docx'])
    ]
)
```

---

## 6. Decimal Field

```python
price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(0)]
)
```

---

## 7. Choice Field

```python
DEPT_CHOICES = [
    ("CSE", "CSE"),
    ("EEE", "EEE"),
    ("BBA", "BBA"),
]

dept = models.CharField(
    max_length=10,
    choices=DEPT_CHOICES
)
```

---

## 8. Optional Field

```python
address = models.CharField(
    max_length=255,
    null=True,
    blank=True
)
```

---

## 9. Unique Constraint

```python
email = models.EmailField(unique=True)
```

---

# Custom Validator (Important)

## Define Function

```python
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError("Value must be even")
```

## Use in Model

```python
age = models.IntegerField(
    validators=[validate_even]
)
```

---

# Full Example (Combined)

```python
class StudentModel(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            RegexValidator(regex=r'^[A-Za-z ]+$')
        ]
    )

    age = models.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(60)
        ]
    )

    email = models.EmailField(unique=True)

    dept = models.CharField(
        max_length=10,
        choices=[
            ("CSE", "CSE"),
            ("EEE", "EEE")
        ]
    )

    address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
```

---

# Best Practices

* Always use **model-level validation** (core logic)
* Use **custom validators** for business rules
* Combine with **serializer validation** in DRF
* Avoid putting all validation only in views

---

# Key Concepts Summary

| Concept          | Purpose                 |
| ---------------- | ----------------------- |
| `validators=[]`  | Attach validation rules |
| `null=True`      | Allow NULL in database  |
| `blank=True`     | Allow empty input       |
| `unique=True`    | Prevent duplicates      |
| `choices=`       | Restrict allowed values |
| Custom Validator | Business-specific logic |

---

> Model-level validation ensures data integrity across all layers (admin, API, shell), making it the most reliable place for enforcing rules.
