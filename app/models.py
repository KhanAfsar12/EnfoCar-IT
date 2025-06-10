from django.db import models
from django.contrib.auth.models import User

class PricingConfig(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Distance Base Price
    dbp_amount = models.DecimalField(max_digits=10, decimal_places=2)
    dbp_max_km = models.DecimalField(max_digits=5, decimal_places=2)
    dbp_applicable_days = models.CharField(max_length=50, help_text="Comma-separated days (e.g. MON,TUE,WED)")
    
    # Distance Additional Price
    dap_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Time Multiplier Factor
    tmf_under_1h = models.DecimalField(max_digits=5, decimal_places=2)
    tmf_1h_to_2h = models.DecimalField(max_digits=5, decimal_places=2)
    tmf_after_2h = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Waiting Charges
    wc_free_minutes = models.PositiveIntegerField(default=3)
    wc_amount_per_block = models.DecimalField(max_digits=5, decimal_places=2)
    wc_block_duration = models.PositiveIntegerField(default=3, help_text="Minutes per block")
    
    def __str__(self):
        return self.name

class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()
    
    def __str__(self):
        return f"{self.config.name} updated by {self.changed_by} at {self.changed_at}"