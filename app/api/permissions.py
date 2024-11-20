from fastapi import Depends, HTTPException, status

from database.models import UsersORM
from user import current_user


def check_admin(user: UsersORM = Depends(current_user)):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )
    return user


def check_student_or_admin(user: UsersORM = Depends(current_user)):
    if user.role not in ["ADMIN", "STUDENT"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )
    return user
