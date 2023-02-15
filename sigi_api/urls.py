from django.urls import path
from . import views

urlpatterns = [
  
 
    path('api_sigi/payment/validate', views.ValidationView.as_view(), name='validate'),
    path('api_sigi/payment', views.PaymentView.as_view(), name='confirmpayment'),
   
    

]