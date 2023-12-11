from rest_framework_simplejwt.tokens import AccessToken

class JWTUtils:
    @staticmethod
    def fetch_user_id(request):
        """
        Extracts the user ID from the JWT token in the request.
        """
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if token:
            decoded_token = AccessToken(token)
            return decoded_token['user_id']
        return None