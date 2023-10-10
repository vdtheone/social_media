from fastapi import HTTPException, Request
from jose import jwt, ExpiredSignatureError, JWTError
import os


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def get_current_user_id(request:Request): 
    try:
        access_token = request.headers.get("Authorization")
        access_token = access_token.split()[1]
        user_id = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM]).get('id')
        return user_id
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