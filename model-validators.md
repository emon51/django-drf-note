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


# Django & DRF Validation — Model vs Serializer (Complete Guide)

## Overview

In Django REST Framework (DRF), validation happens in **two layers**:

| Layer                    | Purpose                              |
| ------------------------ | ------------------------------------ |
| Model Validation         | Database-level safety (global rules) |
| Serializer Validation    | API-level/business rules             |

---

# 1. Model Validation (Database Layer)

## ✔ Purpose

* Ensures data integrity in database
* Works in Admin, Shell, API
* Always enforced

---

## Example

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentModel(models.Model):
    name = models.CharField(max_length=100)

    age = models.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(60)
        ]
    )

    dept = models.CharField(max_length=100)
```

---

## What it enforces

| Rule     | Example   |
| -------- | --------- |
| MinValue | age >= 18 |
| MaxValue | age <= 60 |

---

# 2. Serializer Validation (API Layer)

## ✔ Purpose

* API-specific rules
* Business logic validation
* Input validation before saving

---

## Basic Serializer

```python
from rest_framework import serializers
from .models import StudentModel

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = "__all__"
```

---

# 3. Field-Level Validation

## ✔ Use Case

Validate a single field

```python
def validate_age(self, value):  # syntax: def validate_<field_name>(self, value):
    if value < 21:
        raise serializers.ValidationError("Age must be at least 21 for API users")
    return value
```

---

# 4. Object-Level Validation

## ✔ Use Case

Validate multiple fields together

```python
def validate(self, data):
    if data["dept"] == "CSE" and data["age"] < 22:
        raise serializers.ValidationError("CSE students must be 22+")
    return data
```

---

# 5. Combined Validation Flow

When you call:

```python
serializer.is_valid()
```

DRF performs:

```
1. Serializer field validation
2. Serializer object validation
3. Model validation
4. If all pass → data is valid
```

---

# 6. Real Example (Full Stack Validation)

## Model Layer

```python
age = models.IntegerField(
    validators=[
        MinValueValidator(18),
        MaxValueValidator(60)
    ]
)
```

---

## Serializer Layer

```python
def validate_age(self, value):
    if value < 21:
        raise serializers.ValidationError("API rule: age must be 21+")
    return value
```

---

# 7. Behavior Table

| Input Age | Result                            |
| --------- | --------------------------------- |
| 17        | Blocked (Model Validation)        |
| 20        | Blocked (Serializer Validation)   |
| 25        | Accepted                          | 

---

# 8. Key Concept

Model = Database safety layer
Serializer = API/business logic layer

---

# 9. Request Flow in DRF

```
Request → Serializer → Model → Database
           (API rules)   (DB rules)
```

---


> Model validation ensures database integrity across all interfaces, while serializer validation enforces API-specific business rules before data reaches the database.

---

# Summary

* ✔ Use model validators for global constraints
* ✔ Use serializer validation for API logic
* ✔ Combine both for strong data protection
* ✔ Always call `serializer.is_valid()` before saving

