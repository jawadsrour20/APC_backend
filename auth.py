# Server knows who is logged in through the JWT token
# It decodes the token, and now knows the username (which is unique for every user),
# Accordingly, it can manage that users information.

# pip install PyJWT ... not JWT
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import dotenv_values
from http_status_codes import HTTP_STATUS_CODE_UNAUTHORIZED
# HTTPException: used to raise errors for invalid tokens... returning a StatusCode for the user
# Security: used for Dependency Injection and will highlight routes that require authorization
# headers in the SwaggerUI and provide a way to enter a bearer token there
# HTTPBearer: used as part of the dependency injection to ensure that a valid authorization header is present
# HTTPAuthorizationCredentials: the object type that will be returned from the dependency injection
# CryptContext: used for hashing and to validate the hashed password
# datetime and timedelta are used to calculate the expiry time of the token

config = dotenv_values(".env")

# HS256 is a symmetric signing method.
# This means that the same secret key is used to both create and verify the signature.
# The issuer appends the JWT header and payload with the secret key,
# and hashes the result using SHA256, creating a signature.
HASHING_ALGORITHM = config.get('HASHING_ALGORITHM')


# Note on payload: Store all user-related data that would be needed in the payload, to do less queries to the database
# We might still just store the UNIQUE Value such as username or email of user in the payload, and query the database
class AuthHandler():
    security = HTTPBearer()
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = config.get("SECRET")

    def get_password_hash(self, password):
        return self.password_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_context.verify(plain_password, hashed_password)

    def encode_token(self, username, first_name, last_name, is_instructor, instructor_name):
        payload = \
        {
            "iat": datetime.now(),
            "exp": datetime.now() + timedelta(days=0, minutes=30),
            "sub": username,
            "name": f'{first_name} {last_name}',
            "is_instructor": is_instructor,
            "instructor_name": instructor_name
        }


        return jwt.encode(payload, self.secret, algorithm=HASHING_ALGORITHM)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[HASHING_ALGORITHM])
            return {
                "username": payload['sub'],
                "name": payload['name'],
                "is_instructor": payload['is_instructor'],
                "instructor_name": payload['instructor_name']
                }

        except jwt.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=HTTP_STATUS_CODE_UNAUTHORIZED, detail="Signature expired. Please log in again."
            ) from e # explicitly raise Exception from a previous error

        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=HTTP_STATUS_CODE_UNAUTHORIZED, detail="Invalid token. Please log in again."
            ) from e

    # Ensures Bearer Token has been supplied in the auth-header, but doesn't do anything
    # to validate the token, so once it passes that check, we validate the token ourselves
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):

        return self.decode_token(auth.credentials)

auth_handler = AuthHandler()