# Developed by Ferhat Mousavi
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.urls import path, include


class MultipleDomainMiddleware:
    """
    Middleware to handle multiple domains in a Django project.
    This middleware dynamically routes requests to different URL configurations
    based on the domain of the incoming request. It also supports automatic redirection
    from certain domains to others and allows for fallback handling in DEBUG mode.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware.
        - get_response: This is the next middleware or view that will handle the request
          after this middleware processes it.
        - url_config: Retrieves the MULTI_DOMAIN_CONFIG setting from Django settings.
          This contains the mapping of domains to their respective URL configurations.
        - redirect_config: Retrieves the MULTI_REDIRECT_CONFIG setting, which maps domains
          that should be automatically redirected to other domains.
        """
        self.get_response = get_response
        self.url_config = getattr(settings, 'MULTI_DOMAIN_CONFIG', None)
        self.redirect_config = getattr(settings, 'MULTI_REDIRECT_CONFIG', None)

    def __call__(self, request):
        """
        Handles the incoming request.
        This method is executed for every HTTP request that passes through the middleware stack.
        """

        # Extract the domain name from the request's host (excluding subdomains and port).
        host_domain_name = self.get_host_domain_name(request)

        # Check if there is a redirect configuration for this domain.
        if self.redirect_config:
            redirect_domain = self.redirect_config.get(host_domain_name)

            # If a redirect is configured, return an HTTP 301 Permanent Redirect response.
            if redirect_domain:
                return HttpResponsePermanentRedirect(f'https://{redirect_domain}')

        # Process the request and route it to the appropriate URL configuration.
        if not self.process_request(request, host_domain_name):
            return HttpResponseNotFound()

        # Continue processing the request with the assigned URL configuration.
        response = self.get_response(request)
        return response

    def get_host_domain_name(self, request):
        """
        Extracts the base domain name from the host of the request.
        This method ensures that subdomains and port numbers are removed, leaving only
        the primary domain (e.g., 'sub.example.com' becomes 'example.com').
        """

        # Get the full host (domain + port) from the request.
        host_domain_name = request.get_host()

        # Remove the port number if it exists (split by ':').
        host_domain_name = host_domain_name.split(':')[0]

        # Split the domain into its parts (e.g., ['sub', 'example', 'com']).
        host_domain_part_list = host_domain_name.split('.')

        # If the domain has more than two parts (i.e., contains a subdomain), strip the subdomain.
        if len(host_domain_part_list) > 2:
            host_domain_part_list = host_domain_part_list[-2:] # Keep only the last two parts (e.g., 'example.com')

        # Reconstruct the domain without the subdomain.
        host_domain_name = f"{host_domain_part_list[0]}.{host_domain_part_list[1]}"

        return host_domain_name

    def process_request(self, request, host_domain_name):
        """
        Processes the incoming request by determining which URL configuration to apply.
        It dynamically merges the domain-specific URLs and common URLs (if defined in COMMON_URLS).
        """

        # If there is no MULTI_DOMAIN_CONFIG, return False (i.e., no domain-specific routing is set up).
        if not self.url_config:
            return False

        # Check if common URLs are defined in settings (COMMON_URLS).
        common_urls = getattr(settings, 'COMMON_URLS', None)

        # Prepare a list to store the combined URL patterns (specific to the domain + common).
        combined_urlpatterns = []

        # Get the URL configuration module for the specific domain from MULTI_DOMAIN_CONFIG.
        specific_urls_module = self.url_config.get(host_domain_name, None)

        # If no specific URLs are found and the project is in DEBUG mode, use DEFAULT_DOMAIN.
        if not specific_urls_module and settings.DEBUG:
            # Fallback to default domain configuration if DEBUG is True and domain was not found
            default_urls_module = self.url_config.get(settings.DEFAULT_DOMAIN, None)
            if default_urls_module:
                # Add the default domain's URL configuration to the combined URL patterns.
                combined_urlpatterns.append(path('', include(default_urls_module)))

        # If a specific URL module exists for the domain, add it to the combined URL patterns.
        if specific_urls_module:
            # Dynamically merge the domain-specific URLs with the common URLs.
            combined_urlpatterns.append(path('', include(specific_urls_module)))

        # If COMMON_URLS is defined, add it to the combined URL patterns as well.
        if common_urls:
            combined_urlpatterns.append(path('', include(common_urls)))

        # If there are any combined URL patterns, dynamically create a temporary URL configuration module.
        if combined_urlpatterns:
            # Name the temporary URL configuration module based on the domain or specific URL module.
            module_name_base = specific_urls_module if specific_urls_module else host_domain_name

            # Create a new temporary URL configuration object with the combined URL patterns.
            temp_urlconf_module = type(f"{module_name_base}_with_common", (object,), {
                "urlpatterns": combined_urlpatterns
            })

            # Assign the new URL configuration to the request, enabling Django to route the request properly.
            request.urlconf = temp_urlconf_module
            return True

        # If no valid URL configuration was found, return False.
        return False
