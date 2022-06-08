from django.db import models


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=128,
        null=False,
        blank=False
    )

    name = models.CharField(
        max_length=128,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name
