# Developed by Ferhat Mousavi
from publicsuffix2 import get_sld
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
        - subdomain_config: Retrieves the MULTI_SUBDOMAIN_CONFIG setting to manage subdomain mappings.
        """
        self.get_response = get_response
        self.url_config = getattr(settings, 'MULTI_DOMAIN_CONFIG', None)
        self.redirect_config = getattr(settings, 'MULTI_REDIRECT_CONFIG', None)
        self.subdomain_config = getattr(settings, 'MULTI_SUBDOMAIN_CONFIG', None)

    def __call__(self, request):
        """
        Handles the incoming request.
        This method is executed for every HTTP request that passes through the middleware stack.
        """

        # Extract the domain name and subdomains from the request's host (excluding port if present).
        host_domain_name, subdomains = self.get_host_domain_and_subdomains(request)

        # Check if there is a redirect configuration for the current domain.
        if self.redirect_config:
            redirect_domain = self.redirect_config.get(host_domain_name)

            # If a redirect is configured for this domain, return an HTTP 301 response.
            if redirect_domain:
                return HttpResponsePermanentRedirect(f'https://{redirect_domain}')

        # Add subdomain information as attributes to the request object for later use.
        self.add_subdomains_to_request(request, subdomains)

        # Process the request by determining the appropriate URL configuration.
        if not self.process_request(request, host_domain_name):
            # If no valid configuration is found, return a 404 Not Found response.
            return HttpResponseNotFound()

        # If processing is successful, proceed to the next middleware or view.
        response = self.get_response(request)
        return response

    def get_host_domain_and_subdomains(self, request):
        """
        Extracts the base domain and subdomains from the request's host using the Public Suffix List.
        """

        # Extract the host name from the request (excluding the port number, if present).
        host = request.get_host().split(':')[0]

        # Get the second-level domain (SLD) using the public suffix list.
        sld = get_sld(host)

        if sld:
            # Split the full host into parts (e.g., subdomain.domain.com -> [subdomain, domain, com]).
            domain_parts = host.split('.')
            sld_parts = sld.split('.')

            # Determine the subdomains by excluding the SLD parts from the full host.
            subdomains = domain_parts[: -len(sld_parts)]
        else:
            # If get_sld fails, assume the entire host is the domain and there are no subdomains.
            sld = host
            subdomains = []

        # Return the base domain (SLD) and the list of subdomains.
        return sld, subdomains

    def add_subdomains_to_request(self, request, subdomains):
        """
        Adds subdomain parameters to the request object as attributes.
        """
        for idx, subdomain in enumerate(subdomains):
            # Check if a custom name for the subdomain is defined in MULTI_SUBDOMAIN_CONFIG.
            if self.subdomain_config and idx < len(self.subdomain_config):
                param_name = self.subdomain_config[idx]
            else:
                # Default parameter name: subdomain1, subdomain2, etc.
                param_name = f"subdomain{idx + 1}"

            # Add the subdomain as an attribute to the request object.
            setattr(request, param_name, subdomain)

    def process_request(self, request, host_domain_name):
        """
        Processes the incoming request by determining which URL configuration to apply.
        It dynamically combines domain-specific URLs with common URLs (if defined in settings).
        """

        # If MULTI_DOMAIN_CONFIG is not defined, domain-specific routing is not set up.
        if not self.url_config:
            return False

        # Check if common URLs are defined in settings (COMMON_URLS).
        common_urls = getattr(settings, 'COMMON_URLS', None)

        # Initialize an empty list to store the combined URL patterns.
        combined_urlpatterns = []

        # Get the URL configuration module specific to the current domain.
        specific_urls_module = self.url_config.get(host_domain_name, None)

        # If no specific URLs are found and the project is in DEBUG mode:
        if not specific_urls_module and settings.DEBUG:
            # Use the default domain's configuration (if available) as a fallback.
            default_urls_module = self.url_config.get(settings.DEFAULT_DOMAIN, None)
            if default_urls_module:
                # Add the default domain's URL configuration to the combined URL patterns.
                combined_urlpatterns.append(path('', include(default_urls_module)))

        # If specific URLs for the current domain are defined, add them to the list.
        if specific_urls_module:
            # If common URLs are defined, add them to the combined URL patterns.
            combined_urlpatterns.append(path('', include(specific_urls_module)))

        # If COMMON_URLS is defined, add it to the combined URL patterns as well.
        if common_urls:
            combined_urlpatterns.append(path('', include(common_urls)))

        # If there are any URL patterns, create a temporary URL configuration module.
        if combined_urlpatterns:
            # Name the temporary module based on the domain or specific URL module.
            module_name_base = specific_urls_module if specific_urls_module else host_domain_name

            # Create a temporary URL configuration object with the combined patterns.
            temp_urlconf_module = type(f"{module_name_base}_with_common", (object,), {
                "urlpatterns": combined_urlpatterns
            })

            # Assign the temporary URL configuration to the request object.
            request.urlconf = temp_urlconf_module
            return True

        # If no valid URL configuration was found, return False.
        return False
