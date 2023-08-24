# dj-multidomain

## Multiple Domain Middleware for Django
This middleware allows Django projects to route requests to different URL configurations based on the request's domain. It is especially useful for projects hosted on multiple domains. Developed by Ferhat Mousavi.

## Supported (tested) Versions

- Python: 3.10 and above
- Django: 4 and above

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
5. **(Optional) If you are in DEBUG mode and want a fallback for unrecognized domains, specify the DEFAULT_DOMAIN setting:**
```
DEFAULT_DOMAIN = 'path.to.default_urls'
```
## Usage
With the middleware set up, incoming requests will be routed based on their domain to the specified URL configurations. URLs defined in COMMON_URLS will be accessible from any domain.

## Support & Contribution
For issues, feedback, or feature requests, please open an issue on the GitHub repository. Contributions are welcome; feel free to submit a pull request.
