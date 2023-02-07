from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from .serializers import ValidationSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
import requests, json

base_url = os.getenv('base_url')

headers = {
            'Authorization': 'Basic ZGdpLXd5czpkZ2ktd3lzLWludGVncmF0aW9uLXYz',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=ACAD8AA4116EBB2F297259DEF4D3F93C'
}

def CheckValues(serializer):
    serializer.is_valid()
    integration_code = serializer.data.get("integration_code", False)
    payment_number = serializer.data.get("payment_number", False)
    
    if (integration_code == False):
        return "integration_code empty"
    if (payment_number == False):
        return "payment_number empty"
   
    return True
    
def validation_req(self, data, request):
        
        try:
            serializer = self.get_serializer(data=request.data)
            ans = CheckValues(serializer)
            
            if (ans == "integration_code empty"):
                return ({"message" :"integration_code empty is empty.", "status":"failed"}, False)
            if (ans == "payment_number empty"):
                return ({"message" :"tin_number empty is empty.", "status":"failed"}, False)
            if not serializer.is_valid(raise_exception=True):
                return ({"message" :" Please enter the correct details", "status":"failed"}, False)
            print("Information is verified.")
        except Exception as e:
            print(e.args[0])
            return ( e.args[0],  False)
        data    = serializer.validated_data
        path    = "/api/findPaymentByPaymentNumber"
        url     = str(base_url) + str(path)
        payload = {
                "integration_code":data["integration_code"] ,
                "payment_number":data["payment_number"],
                }
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            print("The url "+url+" went through.")
            
        except:
            return ( "We cannot connect to the host ", False)
            
        try:
            if response.status_code== 200:
                res = response.json()
                return (res, True)
            else:
                print(response.status_code)
                return ( "Line 67", False)
        except:
            return ( "We cannot connect to the ", False)
        
       
# class ValidationView(GenericAPIView):
#     """
#     To validate 
#     """
    
#     # permission_classes = (IsAuthenticated, )
#     serializer_class        = ValidationSerializer
#     def post(self, request, *args, **kwargs):
      
#         data = request.data
#         try:
#             resp, status = validation_req(self, data, request)
#         except:
#             return Response({"Response":{"message":"Validation Failed.","status":"Failed"}})
      
#         if status:
#             print("This is Response for Successful Validation: ", resp)
#             return Response({"Response": {"Customer" :"Validation Successful","status":"Success"}})
#         else:
#             print("This is Response for failed Validation: ", resp)
#             return ({"Response":{"message":"Failed transaction","status":"Failed"}})


class PaymentView(GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    
    serializer_class        = PaymentSerializer
    def post(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        ans = CheckValues(serializer)
            
        if not serializer.is_valid(raise_exception=True):
            return Response({"Response":{"message" :" Please enter the correct details", "status":"Failed"}}, status=status.HTTP_400_BAD_REQUEST)
        print("Information is verified.")
        
        data    = serializer.validated_data
        path = "/api/confirmPayment"
        url = str(base_url) + str(path)
        payload = {
                    "integration_code"      : request.data.get("integration_code"),
                    "payer_number"          : request.data.get("payer_number"),
                    "payment_number"        : request.data.get("payment_number"),
                    "payment_ext_reference" : request.data.get("tranref"),
                    "payment_date"          : request.data.get("payment_date"),
                    "payment_amount"        : request.data.get("payment_amount"),
                    "payment_description"   : request.data.get("payment_description"),
        }
       
        try:
            response = requests.request("POST", url, headers=headers,data=json.dumps(payload))
            print("Payment processing")
            res = response.json()
            if res.get("status") == "P":
                return Response({"Response":{"message": "Payment completed successfully", "status":"Success"}})
            else:
                return Response({"Response":{"message": "Line 128","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.args[0])
            return  Response({"Response":{"message":"We cannot connect to the ", "status":"Failed"}})

class ValidationView(GenericAPIView):
    """
    To search for payment use payment_number in the request body.
    
    """
    # permission_classes = (IsAuthenticated, )
    serializer_class        = ValidationSerializer
    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        ans = CheckValues(serializer)
        if (ans == "payment_number empty"):
            return Response({"Response":{"message" :"payment_number is empty.", "status":"Failed"}}, status=status.HTTP_400_BAD_REQUEST)
            
        if not serializer.is_valid(raise_exception=True):
            return Response({"Response":{"message" :" Please enter the correct details", "status":"Failed"}}, status=status.HTTP_400_BAD_REQUEST)
        print("Information is verified.")
        
        data    = serializer.validated_data
        path    = "/api/findPaymentByPaymentNumber"
        url     = str(base_url) + str(path)
        payload = {
                    "payment_number": data["payment_number"],
                    "integration_code": data["integration_code"]
            
                }
        
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            print("The url "+url+" went through.")
            if response.status_code== 200:
                res = response.json()
                return Response({"Response":{"message":res,"status":"Success"}})
            else:
                return Response({"Response":{"message": "Line 178","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Response":{"message": "Line 180","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
        
        
        