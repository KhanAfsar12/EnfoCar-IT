from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import PricingConfig
from datetime import datetime
from decimal import Decimal

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    
    try:
        distance = Decimal(str(data.get('distance', 0)))
        ride_time = Decimal(str(data.get('ride_time', 0)))
        waiting_time = Decimal(str(data.get('waiting_time', 0)))
        date_str = data.get('date', timezone.now().isoformat())
        
        ride_date = datetime.fromisoformat(date_str)
        day_of_week = ride_date.strftime('%a').upper()
        
        config = PricingConfig.objects.filter(is_active=True).first()
        if not config:
            return Response(
                {"error": "No active pricing configuration found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        applicable_days = [day.strip() for day in config.dbp_applicable_days.split(',')]
        if day_of_week not in applicable_days:
            return Response(
                {"error": f"No pricing configuration for {day_of_week}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if distance <= Decimal(config.dbp_max_km):
            dbp = Decimal(config.dbp_amount)
            additional_distance = Decimal(0)
        else:
            dbp = Decimal(config.dbp_amount)
            additional_distance = distance - Decimal(config.dbp_max_km)
        
        dap = additional_distance * Decimal(config.dap_amount)
        
        ride_hours = ride_time / Decimal(60)
        if ride_hours <= Decimal(1):
            tmf = Decimal(config.tmf_under_1h)
        elif ride_hours <= Decimal(2):
            tmf = Decimal(config.tmf_1h_to_2h)
        else:
            tmf = Decimal(config.tmf_after_2h)
        
        time_component = (ride_time / Decimal(60)) * tmf
        
        if waiting_time <= Decimal(config.wc_free_minutes):
            wc = Decimal(0)
        else:
            extra_waiting = waiting_time - Decimal(config.wc_free_minutes)
            blocks = extra_waiting / Decimal(config.wc_block_duration)
            if extra_waiting % Decimal(config.wc_block_duration) > Decimal(0):
                blocks += Decimal(1)
            wc = blocks * Decimal(config.wc_amount_per_block)
        
        price = dbp + dap + time_component + wc
        
        response_data = {
            "price": float(round(price, 2)),
            "components": {
                "distance_base_price": float(dbp),
                "distance_additional_price": float(dap),
                "time_multiplier_component": float(time_component),
                "waiting_charges": float(wc),
            },
            "config_used": config.name,
            "day_of_week": day_of_week
        }
        
        return Response(response_data)
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )