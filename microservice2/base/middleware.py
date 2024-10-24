# middleware.py
from django.http import JsonResponse
from django.conf import settings
import requests

class KeycloakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define public endpoints
        public_endpoints = ['/base/login/']  # Make sure this matches exactly

        # Allow access to public endpoints
        if request.path in public_endpoints:
            return self.get_response(request)  # Proceed without token validation

        # Retrieve the token from cookies or headers
        token = request.COOKIES.get('access_token') or request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None

        if token:
            # Validate token with Keycloak
            try:
                response = requests.get(
                    f"{settings.KEYCLOAK_OAUTH2_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/userinfo",
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.status_code != 200:
                    return JsonResponse({'error': 'Unauthorized'}, status=401)
            except requests.RequestException:
                return JsonResponse({'error': 'Keycloak unavailable'}, status=503)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)  # No token present

        return self.get_response(request)
