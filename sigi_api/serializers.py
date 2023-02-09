from rest_framework import serializers
from datetime import datetime
from phonenumber_field.serializerfields import PhoneNumberField
   

class PaymentSerializer(serializers.Serializer):
   payer_number         = PhoneNumberField(allow_blank=False, required=True)
   payment_number       = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   tranref              = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   payment_amount       = serializers.DecimalField(max_digits=11, decimal_places=2)
   payment_description  = serializers.CharField()
   


   
   
   
   
class ValidationSerializer(serializers.Serializer):
   payment_number = serializers.RegexField(required = True, regex=r"[0-9A-Za-z]+")
   
   def CheckValues(serializer):
      serializer.is_valid()
      payment_number = serializer.data.get("payment_number", False)
      
    
      if (payment_number == False):
         return "payment_number empty"
      
      
      return True
    
    
    