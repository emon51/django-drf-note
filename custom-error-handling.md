# Custom Exceptions in Python

## What is a Custom Exception?

In Python, custom exceptions are usually created using a class.

Why?

Because:
- Exceptions are objects
- Objects are created from classes

---

# Basic Syntax

```python
class MyCustomError(Exception):
    pass
```

MyCustomError → Custom exception name
Exception → Built-in parent exception class
pass → Empty class (no extra logic yet)

```
raise MyCustomError("Something went wrong")
```
