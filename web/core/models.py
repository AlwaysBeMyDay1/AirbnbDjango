from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True => model 처음 생성시 날짜 생성

    updated = models.DateTimeField(auto_now=True)
    # auto_now=True => model 수정시 날짜 업데이트

    class Meta:
        abstract: True
