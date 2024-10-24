import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import json

class LoginView(APIView):
    """Handle user login by verifying credentials with Keycloak."""
    
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            # Define the Keycloak token URL
            token_url = f"{settings.KEYCLOAK_OAUTH2_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

            # Prepare the payload to exchange credentials for tokens
            data = {
                'grant_type': 'password',  # Use password grant type
                'client_id': settings.KEYCLOAK_CLIENT_ID,
                'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
                'username': email,  # Use email as the username
                'password': password,
            }

            # Make the POST request to Keycloak's token endpoint
            response = requests.post(token_url, data=data)

            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get('access_token')
                refresh_token = token_response.get('refresh_token')

                # Store tokens in HttpOnly cookies for secure access
                response = Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }, status=status.HTTP_200_OK)
                response.set_cookie('access_token', access_token, httponly=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True)

                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
