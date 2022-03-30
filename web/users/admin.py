from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User) #admin 패널에서 User 모델을 보고 싶다는 뜻의 decorator
class CustomUserAdmin(UserAdmin): #User를 컨트롤한 클래스는 이 클래스
    """Custom User Admin"""
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",{
                "fields":(
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            }
        ),
    )
    