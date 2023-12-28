from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request: Request) -> tuple:
        """
        Authenticates a request by extracting the token from the
        header or cookie, validating it, and returning the user
        associated with the token along with the validated token.

        Parameters:
            request (object): The request object containing the header
            and cookie information.

        Returns:
            tuple: A tuple containing the user associated with the validated
            token and the validated token itself. If the request does not
            contain a valid token, None is returned.
        """
        header = self.get_header(request)

        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = self.get_raw_token_cookie(request)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_raw_token_cookie(self, request: Request) -> str:
        """
        Retrieve the raw JWT token from the request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            str: The raw JWT token from the request cookies.
        """
        return request.COOKIES.get('jwt')
