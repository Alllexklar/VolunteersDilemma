# In your extra_models.py (or another dedicated module)
from django.db import models

class LockDummy(models.Model):
    id = models.AutoField(primary_key=True)
    dummy = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        db_table = 'lock_dummy'
