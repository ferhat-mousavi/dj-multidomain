# Developed by Ferhat Mousavi
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.urls import path, include


class MultipleDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.url_config = getattr(settings, 'MULTI_DOMAIN_CONFIG', None)
        self.redirect_config = getattr(settings, 'MULTI_REDIRECT_CONFIG', None)

    def __call__(self, request):
        host_domain_name = self.get_host_domain_name(request)

        if self.redirect_config:
            redirect_domain = self.redirect_config.get(host_domain_name)

            if redirect_domain:
                return HttpResponsePermanentRedirect(f'https://{redirect_domain}')

        if not self.process_request(request, host_domain_name):
            return HttpResponseNotFound()

        response = self.get_response(request)
        return response

    def get_host_domain_name(self, request):
        host_domain_name = request.get_host()
        host_domain_name = host_domain_name.split(':')[0]  # Remove port, if present

        host_domain_part_list = host_domain_name.split('.')
        if len(host_domain_part_list) > 2:  # Remove subdomain, if present
            host_domain_part_list = host_domain_part_list[-2:]
        host_domain_name = f"{host_domain_part_list[0]}.{host_domain_part_list[1]}"  # Trim subdomains

        return host_domain_name

    def process_request(self, request, host_domain_name):
        """
        This method determines which URL configuration should be used for the incoming request.
        Depending on the domain of the request, it dynamically merges domain-specific URLs with
        the common URLs defined in settings.COMMON_URLS (if available).
        """
        if not self.url_config:
            return False

        # Check if COMMON_URLS is defined in settings.
        common_urls = getattr(settings, 'COMMON_URLS', None)

        # If the domain isn't in self.url_config and DEBUG is True, use DEFAULT_DOMAIN
        # Retrieve the URL configuration module for the specific domain.
        combined_urlpatterns = []
        specific_urls_module = self.url_config.get(host_domain_name, None)
        if not specific_urls_module and settings.DEBUG:
            # Fallback to default domain configuration if DEBUG is True and domain was not found
            default_urls_module = self.url_config.get(settings.DEFAULT_DOMAIN,
                                                      None)  # Get the actual URL module for the default domain
            if default_urls_module:
                combined_urlpatterns.append(path('', include(default_urls_module)))

        if specific_urls_module:
            # Dynamically merge the domain-specific URLs with the common URLs.
            combined_urlpatterns.append(path('', include(specific_urls_module)))

        # Add COMMON_URLS if it's available
        if common_urls:
            combined_urlpatterns.append(path('', include(common_urls)))

        # Create a temporary URL configuration module to hold the combined URLs.
        # This approach allows the creation of a dynamic URL configuration without
        # having to modify the actual URL modules.
        if combined_urlpatterns:
            module_name_base = specific_urls_module if specific_urls_module else host_domain_name
            temp_urlconf_module = type(f"{module_name_base}_with_common", (object,),
                                       {
                                           "urlpatterns": combined_urlpatterns
                                       }
                                       )

            # Assign the new dynamic URL configuration to the request.
            request.urlconf = temp_urlconf_module
            return True

        return False
