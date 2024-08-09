from fastapi import HTTPException, Depends, status
from lib.connection import connection
import lib.acl as ACL
from typing import List

def get_user_permissions(user_id: int) -> List[str]:
    try:
        with connection() as conn:
            with conn as cur:
                cur.execute('''
                    SELECT permission_name
                    FROM users.get_user_permissions(%s)
                ''', (user_id,))
                permissions = cur.fetchall()
        return [perm[0] for perm in permissions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {str(e)}"
        )   

def check_user_permission(permission: str, token: str):
    decoded_token = ACL.decodeJWT(token)
    user_id = decoded_token.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_permissions = get_user_permissions(user_id)
    if permission not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permission"
        )

# Dependency to check permission
def permission_dependency(*permissions: str):
    def wrapper(token: str = Depends(ACL.JWTBearer())):
        decoded_token = ACL.decodeJWT(token)
        user_id = decoded_token.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user_permissions = get_user_permissions(user_id)
        if not any(permission in user_permissions for permission in permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required permission"
            )
    return wrapper













