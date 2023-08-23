# Developed by Ferhat Mousavi
from django.conf import settings
from django.http import HttpResponseNotFound
from django.urls import get_resolver


class MultipleDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.url_config = getattr(settings, 'MULTI_DOMAIN_CONFIG', None)

    def __call__(self, request):
        if not self.process_request(request):
            return HttpResponseNotFound()

        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Processes the request to determine which URL configuration should be used.
        Initially checks the common URLs (from settings.COMMON_URLS), and if none match,
        it checks the domain-specific configuration.
        """
        if not self.url_config:
            return False

        host = request.get_host()
        host = host.split(':')[0]  # Remove port, if present

        host_list = host.split('.')
        if len(host_list) > 2:
            host_list = host_list[-2:]
        host = f"{host_list[0]}.{host_list[1]}"  # Trim subdomains

        # Firstly, check the common URLs
        match = None
        try:
            resolver = get_resolver(settings.COMMON_URLS)  # Reference to the module containing common URLs
            try:
                match = resolver.resolve(request.path_info)
            except:
                pass

            if match:
                request.urlconf = settings.COMMON_URLS
                return True  # If a match is found in the common URLs, continue processing the request
        except:
            pass

        # If the domain isn't in self.url_config and DEBUG is True, use DEFAULT_DOMAIN
        if host not in self.url_config and settings.DEBUG:
            request.urlconf = self.url_config[getattr(settings, 'DEFAULT_DOMAIN')]
            return True

        # Use the domain-specific URL configuration
        if host in self.url_config:
            request.urlconf = self.url_config[host]
        else:
            if not settings.DEBUG:  # If DEBUG is False, do not use the DEFAULT_DOMAIN
                return False
            # Fallback to default domain configuration if DEBUG is True and domain was not found
            request.urlconf = self.url_config[getattr(settings, 'DEFAULT_DOMAIN')]

        return True
