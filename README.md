# dj-multidomain

## Dynamic Multi-Domain Middleware for Django

`dj-multidomain` is a powerful Django middleware that enables dynamic routing of 
requests to different URL configurations based on the domain of 
incoming requests. 
It also supports automatic redirection for specific domains and provides 
options for shared common URLs. 
This middleware is ideal for projects hosted across multiple domains or 
with subdomain-specific functionalities.

Developed by **Ferhat Mousavi**.
[ferhat.mousavi@gmail.com](mailto:ferhat.mousavi@gmail.com)  

---

## Features

- **Domain-Based URL Routing**: Route requests to different URL configurations based on the domain.
- **Subdomain Handling**: Easily manage subdomains and inject subdomain data into requests.
- **Automatic Redirects**: Redirect specific domains to desired ones seamlessly.
- **Shared URLs**: Define common URLs accessible across all domains.
- **Fallback Support**: Set a default domain for unrecognized requests (DEBUG mode).

---

## Installation

### 1. Install the Package

Install `dj-multidomain` using pip:

```bash
pip install dj-multidomain
```

Ensure `publicsuffix2` is also installed:

```bash
pip install publicsuffix2
```

### 2. Add Middleware

In your `settings.py`, add the middleware to the `MIDDLEWARE` list:

```python
MIDDLEWARE = [
    ...
    'dj_multidomain.middleware.MultipleDomainMiddleware',
    ...
]
```

---

## Configuration

### 1. Map Domains to URL Configurations

Use `MULTI_DOMAIN_CONFIG` to map domains to their respective URL configuration files. Add this to `settings.py`:

```python
MULTI_DOMAIN_CONFIG = {
    'example.com': 'project.urls_example_com',
    'example.org': 'project.urls_example_org',
}
```

### 2. Redirect Domains (Optional)

If you want to redirect specific domains to others, use `MULTI_REDIRECT_CONFIG`:

```python
MULTI_REDIRECT_CONFIG = {
    'www.example.com': 'example.com',
    'oldsite.org': 'newsite.org',
}
```

### 3. Add Common URLs (Optional)

Define shared URLs that are accessible from any domain using `COMMON_URLS`:

```python
COMMON_URLS = 'project.urls_common'
```

### 4. Subdomain Configuration (Optional)

If subdomain data needs to be injected into requests, use `MULTI_SUBDOMAIN_CONFIG` to define parameter names:

```python
MULTI_SUBDOMAIN_CONFIG = ['subdomain1', 'subdomain2']
```

### 5. Default Domain (Optional)

Set a fallback URL configuration for unrecognized domains (only active in DEBUG mode):

```python
DEFAULT_DOMAIN = 'example.com'
```

---

## Example Project Structure

Below is a typical project structure for `dj-multidomain`:

```
project/
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls_common.py
│   ├── urls_example_com.py
│   ├── urls_example_org.py
│   ├── views.py
├── manage.py
```

---

## Example Usage

### 1. Domain-Specific URL Configuration

Create domain-specific URL files, e.g., `urls_example_com.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
```

### 2. Common URL Configuration

Define shared URLs in `urls_common.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
]
```

### 3. Subdomain Handling

Subdomains will be available as attributes in the `request` object. For example:

```python
def subdomain_example(request):
    subdomain1 = getattr(request, 'subdomain1', None)
    return HttpResponse(f"Subdomain 1: {subdomain1}")
```

---

## Sample Configuration

Here’s a complete example of `settings.py` for `dj-multidomain`:

```python
MIDDLEWARE = [
    ...
    'dj_multidomain.middleware.MultipleDomainMiddleware',
    ...
]

MULTI_DOMAIN_CONFIG = {
    'example.com': 'project.urls_example_com',
    'example.org': 'project.urls_example_org',
}

MULTI_REDIRECT_CONFIG = {
    'www.example.com': 'example.com',
}

MULTI_SUBDOMAIN_CONFIG = ['subdomain1', 'subdomain2']

COMMON_URLS = 'project.urls_common'

DEFAULT_DOMAIN = 'example.com'
```

---

## Supported Versions

- **Python**: 3.10 and above
- **Django**: 4.0 and above

---

## Sample Project

Explore a sample implementation:  
[GitHub: dj-multidomain Example](https://github.com/ferhat-mousavi/dj-multidomain-example)

---

## Contribution & Support

- For issues or feedback, open an issue in the [GitHub repository](https://github.com/ferhat-mousavi/dj-multidomain).
- Contributions are welcome! Feel free to submit a pull request.

---

## License

This project is licensed under the [GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html).
