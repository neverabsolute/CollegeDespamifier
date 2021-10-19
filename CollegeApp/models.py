from django.db import models
from decimal import Decimal
# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    acceptance = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    grad_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    desirability = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    overall_rank = models.IntegerField(default=0)
    sat = models.IntegerField(default=0)
    act = models.IntegerField(default=0)
    undergrad_student_body = models.IntegerField(default=0)
    tuition = models.IntegerField(default=0)
    domain = models.CharField(max_length=255, default='')
    
    
    def __str__(self):
        return self.name