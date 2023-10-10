import os

from fastapi import HTTPException, Request, status
from jose import ExpiredSignatureError, JWTError

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def access_token_required(func):
    def inner(*args):
        try:
            request = None
            for i in args:
                if isinstance(i, Request):
                    request = i

            if not request:
                raise HTTPException(status_code=500, detail="Request not found")

            access_token = request.headers.get("Authorization")

            if not access_token:
                # Handle the case where no access token is provided
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Access token is missing",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token = access_token.split()[1]

            # jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return func(*args)
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token Expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Provide valid Token")
        except IndexError:
            raise HTTPException(
                status_code=401, detail="list index out of range in token"
            )
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return inner
