# Serializers - Note

## What is a Serializer?

A serializer converts: - Model → JSON (response) - JSON → Model
(validation + input)

------------------------------------------------------------------------

## Basic Syntax

``` python
serializer = SerializerClass(
    instance=None,
    data=None,
    many=False,
    partial=False,
    context=None
)
```
# Parameter Details

## 1. instance

### Type:

```
Model instance OR QuerySet OR None
```

### Purpose:

Used for **serialization (reading data)**

### Examples:

```python
instance=student_obj
instance=StudentModel.objects.all()
instance=None
```

---

## 2. data

### Type:

```
dict OR list[dict] OR None
```

### Purpose:

Used for **deserialization (input data)**

### Examples:

```python
data={"name": "Emon", "age": 25}
data=[{"name": "A"}, {"name": "B"}]  # bulk (with many=True)
data=None
```

---

## 3. many

### Type:

```
bool
```

### Purpose:

Indicates multiple objects

### Values:

```python
many=True
many=False
```

---

## 4. partial

### Type:

```
bool
```

### Purpose:

Allows partial updates (PATCH)

### Values:

```python
partial=True
partial=False
```

---

## 5. context

### Type:

```
dict OR None
```

### Purpose:

Pass extra runtime data to serializer

### Example:

```python
context={
    "request": request,
    "user": request.user
}
```

---

# Common Usage Patterns

## GET (Read)

```python
serializer = StudentSerializer(instance=students, many=True)
```

## POST (Create)

```python
serializer = StudentSerializer(data=request.data)
```

## PATCH (Partial Update)

```python
serializer = StudentSerializer(
    instance=student,
    data=request.data,
    partial=True
)
```

## WITH CONTEXT

```python
serializer = StudentSerializer(
    instance=student,
    context={"request": request}
)
```

---

------------------------------------------------------------------------

# BEST PRACTICE USAGE

## GET (Single)

``` python
serializer = UserSerializer(instance=user)
return Response(serializer.data)
```

## GET (List)

``` python
serializer = UserSerializer(instance=users, many=True)
return Response(serializer.data)
```

## POST

``` python
serializer = UserSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data)
```

## PUT

``` python
serializer = UserSerializer(instance=user, data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data)
```

## PATCH

``` python
serializer = UserSerializer(instance=user, data=request.data, partial=True)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data)
```

------------------------------------------------------------------------

# MEMORY PATTERN

instance = output\
data = input\
many = list\
partial = patch\
is_valid = check\
save = store\
data = response\
errors = problems

------------------------------------------------------------------------

# Important Methods

## is_valid()

``` python
serializer.is_valid(raise_exception=True)
```

## save()

``` python
serializer.save()
```

## data

``` python
serializer.data
```

## errors

``` python
serializer.errors
```

------------------------------------------------------------------------

# Lifecycle

Input → is_valid() → validated_data → save() → data

------------------------------------------------------------------------

# Common Mistakes

Missing many=True\
Save without validation\
Using data incorrectly

------------------------------------------------------------------------

# Response Usage

``` python
return Response(serializer.data)
```

✔ Best practice\
Avoid Response(data=serializer.data)

------------------------------------------------------------------------

# Summary

Serializer = JSON ↔ Model\
Use instance for output\
Use data for input\
Always validate before save

## Full Serializer Structure with Validation

```code
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    # ----------------------------
    # Fields (optional customization)
    # ----------------------------
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email']

    # ----------------------------
    # Field-level validation
    # ----------------------------
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return value

    def validate_email(self, value):
        if "admin" in value:
            raise serializers.ValidationError("Admin emails not allowed")
        return value

    # ----------------------------
    # Object-level validation
    # ----------------------------
    def validate(self, data):
        name = data.get('name')
        email = data.get('email')

        if name and email and name.lower() in email:
            raise serializers.ValidationError(
                "Name should not be part of email"
            )

        return data
```
