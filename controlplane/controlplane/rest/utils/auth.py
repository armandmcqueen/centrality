from typing import Callable
from functools import wraps
from controlplane.datastore.client import DatastoreClient
from fastapi import Request
from fastapi.security import HTTPBearer

security = HTTPBearer()


def auth(datastore_client: DatastoreClient):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request:
                # Pull the Authorization header from the request
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    return {"error": "Missing Authorization header"}, 401
                # Expected format is: Bearer <token>
                auth_header_parts = auth_header.split(" ")
                if len(auth_header_parts) != 2 or auth_header_parts[0] != "Bearer":
                    return {
                        "error": "Invalid Authorization header. Expected format is 'Bearer <token>'"
                    }, 401
                # Validate the token
                token = auth_header_parts[1]
                if not datastore_client.token_exists(token):
                    return {"error": "Invalid token"}, 401

            # Call the actual endpoint function
            response = func(*args, **kwargs)
            return response

        return wrapper

    return decorator
