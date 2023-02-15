from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from .serializers import ValidationSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
from rest_framework.exceptions import ValidationError
import requests, json
import sys
from datetime import datetime



base_url            = os.getenv('base_url')
auth                = os.getenv('auth')
cookie              = os.getenv('cookie')
integration_code    = os.getenv('integration_code')

headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
            'Cookie': cookie
}

def CheckValues(serializer):
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    integration_code = serializer.data.get("integration_code")
    payment_number = serializer.data.get("payment_number")
    return (
        (
            "success", True
            if payment_number else "Payment number cannot be empty", False
        )
        if integration_code
        else ("Integration code cannot be empty", False)
    )
    

class ValidationView(GenericAPIView):
    """
    To validate
    """
    # permission_classes = (IsAuthenticated, )
    serializer_class = ValidationSerializer
    url = f"{str(base_url)}/api/findPaymentByPaymentNumber"


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        status = CheckValues(serializer)

        if not status:
            return Response({"Response":{"message" :"Invalid status", "status":"Failed"}}, status=status.HTTP_400_BAD_REQUEST)
        data    = serializer.validated_data
        payload = {
                    "payment_number": data["payment_number"],
                    "integration_code": integration_code
                }
        try:
            response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                return Response({"Response":{"message": "We cannot establish connection","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
            res = response.json()
        except Exception:
            return Response({"Response":{"message": "An error in connection","status":"Failed"}} )
        # VAS requirement
        print({
            "vendor_url": self.url,
            "res": str(res) or None,
            "vas_payload": str(request.data),
            "vas_url": str(request.path),

        }, file=sys.stdout)
        return Response({"Response":{"message":res,"status":"Success"}})
        
class PaymentView(GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    
    serializer_class = PaymentSerializer
    url = f"{str(base_url)}/api/confirmPayment"

    def post(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        status = CheckValues(serializer)

        if not status:
            return Response({"Response":{"message" :"Pleasa enter correct details", "status":"Failed"}}, status=status.HTTP_400_BAD_REQUEST)
        print("Information is verified.")
        payload = {
                    "integration_code"      : integration_code,
                    "payer_number"          : request.data.get("payer_number"),
                    "payment_number"        : request.data.get("payment_number"),
                    "payment_ext_reference" : request.data.get("tranref"), 
                    "payment_date"          : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "payment_amount"        : request.data.get("payment_amount"),
                    "payment_description"   : request.data.get("payment_description")
        }
        try:
            response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload))
            res = response.json()
            try:
                if res["status"] != "P":
                    print(res)
                    return Response({"Response":{"message": res["status"],"status":"Failed"}} )
            except Exception as e:
                return Response({"Response":{"message": "Status not available. Check host connection","status":"Failed"}} )
        except Exception as e:
            return  Response({"Response":{"message":"Unable to make payment for now ", "status":"Failed"}})

        print({
            "vendor_url": self.url,
            "res": str(res) or None,
            "vas_payload": str(request.data),
            "vas_url": str(request.path),

        }, file=sys.stdout)
        
        return Response({"Response":{"message": "Payment completed successfully", "status":"Success"}})



























