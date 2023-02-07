from rest_framework import serializers
import datetime
from datetime import datetime



# class SearchSerializer(serializers.Serializer):
#    integration_code = serializers.RegexField(required=True, regex=r"[0-9A-Za-z]+")
#    payment_number = serializers.RegexField(required = True, regex=r"[0-9A-Za-z]+")

   
   
   
   
class PaymentSerializer(serializers.Serializer):
   integration_code     = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   payer_number         = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   payment_number       = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   tranref              = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   payment_date         = serializers.DateTimeField(default=datetime.now)
   payment_amount       = serializers.DecimalField(max_digits=11, decimal_places=2)
   payment_description  = serializers.CharField()


   
   
   
   
class ValidationSerializer(serializers.Serializer):
   payment_number = serializers.RegexField(required = True, regex=r"[0-9A-Za-z]+")
   integration_code = serializers.RegexField(required=True, regex=r"[0-9A-Za-z]+")
   
   def CheckValues(serializer):
      serializer.is_valid()
      payment_number = serializer.data.get("payment_number", False)
      integration_code = serializer.data.get("integration_code", False)
    
      if (payment_number == False):
         return "payment_number empty"
      if (integration_code == False):
         return "payment_number empty"
      
      return True
    
    
    