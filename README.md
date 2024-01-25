# dj-multidomain

## Multiple Domain Middleware for Django

This middleware enables Django projects to route requests to different URL configurations based on the domain of the
incoming request. It offers both domain-based URL routing and automatic redirection to another domain for specific
domains. It's particularly useful for projects hosted across multiple domains. Developed by Ferhat Mousavi.

## Supported (tested) Versions

- Python: 3.10 and above
- Django: 4 and above

## Sample Project

[dj-multidomain example](https://github.com/ferhat-mousavi/dj-multidomain-example)

## Installation

1. **Install the package using pip:**

```
   pip install dj-multidomain
```

2. **Add the Middleware to your Django settings:**

```
MIDDLEWARE = [
    ...
    'dj-multidomain.middleware.MultipleDomainMiddleware',
    ...
]
```

3. **Configure the domains and their associated URL configurations in settings.py using the MULTI_DOMAIN_CONFIG setting:**

```
MULTI_DOMAIN_CONFIG = {
    'domain1.com': 'path.to.urls_for_domain1',
    'domain2.com': 'path.to.urls_for_domain2',
    ...
}
```

4. **(Optional for redirect domains)Configure the domains and their associated domain configurations in settings.py
   using the MULTI_REDIRECT_CONFIG setting:**

```
MULTI_REDIRECT_CONFIG = {
    "not_my_desire_domain1.com": "my_desire_domain1.com",
    "not_my_desire_domain2.com": "my_desire_domain2.com",
    ...
}
```

sample `path.to.urls_for_domain1` file

```
from django.urls import path, include

urlpatterns = [
    path('', include('domain1_app.urls')),
]
```

4. **(Optional) For common URLs accessible from any domain, specify the COMMON_URLS setting:**

```
COMMON_URLS = 'path.to.common_urls'
```

sample `path.to.common_urls` file

```
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

5. **(Optional) If you are in DEBUG mode and want a fallback for unrecognized domains, specify the DEFAULT_DOMAIN
   setting:**

```
DEFAULT_DOMAIN = 'path.to.default_urls'
```

## Usage

With the middleware set up, incoming requests will be routed based on their domain to the specified URL configurations.
URLs defined in COMMON_URLS will be accessible from any domain.

## Support & Contribution

For issues, feedback, or feature requests, please open an issue on the GitHub repository. Contributions are welcome;
feel free to submit a pull request.
