from django.contrib import admin
from .models import PricingConfig, PricingConfigLog
from django import forms

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = '__all__'
    
    def clean_dbp_applicable_days(self):
        data = self.cleaned_data['dbp_applicable_days']
        days = [day.strip() for day in data.split(',')]
        valid_days = [choice[0] for choice in PricingConfig.DAY_CHOICES]
        
        for day in days:
            if day not in valid_days:
                raise forms.ValidationError(f"Invalid day: {day}. Valid options are: {', '.join(valid_days)}")
        
        return data

class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    list_display = ('name', 'is_active', 'dbp_amount', 'dbp_max_km', 'dap_amount')
    list_filter = ('is_active',)
    
    def save_model(self, request, obj, form, change):
        if change:
            original_obj = PricingConfig.objects.get(pk=obj.pk)
            changes = []
            for field in obj._meta.fields:
                if getattr(original_obj, field.name) != getattr(obj, field.name):
                    changes.append(
                        f"{field.name} changed from {getattr(original_obj, field.name)} to {getattr(obj, field.name)}"
                    )
            
            if changes:
                PricingConfigLog.objects.create(
                    config=obj,
                    changed_by=request.user,
                    changes="\n".join(changes)
                )
        
        super().save_model(request, obj, form, change)

admin.site.register(PricingConfig, PricingConfigAdmin)
admin.site.register(PricingConfigLog)