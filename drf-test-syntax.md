# Django DRF Testing – Basic Syntax Note

## 1. Model Test Template

```python
class <ModelName>ModelTest(APITestCase):

    def test_<behavior_name>(self):
        obj = <ModelName>.objects.create(<field>=<value>)

        self.assertEqual(obj.<field>, <expected_value>)
        self.assertEqual(str(obj), <expected_str>)
```

---

## 2. API Test Setup (setUp)

```python
class <ModelName>APITest(APITestCase):

    def setUp(self):
        self.<object> = <ModelName>.objects.create(<field>=<value>)

        self.list_url = reverse('<url-name>-list-create')
        self.detail_url = reverse('<url-name>-detail', kwargs={'pk': self.<object>.pk})
```

---

## 3. Common API Test Patterns

### GET (List)
```python
response = self.client.get(self.list_url)
self.assertEqual(response.status_code, 200)
```

### POST (Create)
```python
data = {"<field>": "<value>"}
response = self.client.post(self.list_url, data, format='json')
self.assertEqual(response.status_code, 201)
```

### GET (Detail)
```python
response = self.client.get(self.detail_url)
self.assertEqual(response.status_code, 200)
```

### PATCH / PUT (Update)
```python
data = {"<field>": "<new_value>"}
response = self.client.patch(self.detail_url, data, format='json')
self.assertEqual(response.status_code, 200)
```

### DELETE
```python
response = self.client.delete(self.detail_url)
self.assertEqual(response.status_code, 204)
```

---

# Django DRF Testing – Examples

## 1. Model Test Example

```python
from rest_framework.test import APITestCase
from .models import Task

class TaskModelTest(APITestCase):

    def test_create_task_with_defaults(self):
        task = Task.objects.create(title="Test Task")

        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(str(task), "Test Task")
```

---

## 2. API Test Setup (setUp Example)

```python
from django.urls import reverse

class TaskAPITest(APITestCase):

    def setUp(self):
        self.task = Task.objects.create(
            title="Sample Task",
            description="A test task",
            status="pending"
        )

        self.list_url = reverse('task-list-create')
        self.detail_url = reverse('task-detail', kwargs={'pk': self.task.pk})
```

---

## 3. GET (List Tasks)

```python
def test_list_tasks(self):
    response = self.client.get(self.list_url)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)
```

---

## 4. POST (Create Task)

```python
def test_create_task(self):
    data = {
        "title": "New Task",
        "description": "Task description",
        "status": "in_progress"
    }

    response = self.client.post(self.list_url, data, format='json')

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data["title"], "New Task")
```

---

## 5. GET (Detail Task)

```python
def test_retrieve_task(self):
    response = self.client.get(self.detail_url)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["title"], "Sample Task")
```

---

## 6. PATCH (Partial Update)

```python
def test_update_task(self):
    data = {"status": "done"}

    response = self.client.patch(self.detail_url, data, format='json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["status"], "done")
```

---

## 7. DELETE Task

```python
def test_delete_task(self):
    response = self.client.delete(self.detail_url)

    self.assertEqual(response.status_code, 204)
```

---

## 8. Core Testing Pattern

Arrange → Act → Assert

### Example:
```python
# Arrange
task = Task.objects.create(title="A")

# Act
response = self.client.get("/api/tasks/")

# Assert
self.assertEqual(response.status_code, 200)
```

---

## 9. Status Code Quick Reference

- 200 → Success (GET, PATCH)
- 201 → Created (POST)
- 204 → Deleted (DELETE)
- 400 → Bad Request
- 404 → Not Found

## 4. Core Idea

Arrange → Act → Assert

- Arrange: create data
- Act: call API
- Assert: check result
