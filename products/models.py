from django.db import models

class Item(models.Model):
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'items'