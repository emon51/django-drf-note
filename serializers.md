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

❌ Missing many=True\
❌ Save without validation\
❌ Using data incorrectly

------------------------------------------------------------------------

# Response Usage

``` python
return Response(serializer.data)
```

✔ Best practice\
❌ Avoid Response(data=serializer.data)

------------------------------------------------------------------------

# Summary

Serializer = JSON ↔ Model\
Use instance for output\
Use data for input\
Always validate before save
