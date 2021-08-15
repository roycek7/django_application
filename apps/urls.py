from django.urls import path

from . import views

urlpatterns = [
    path('verify/', views.VendorUserChecker.as_view(), name='verify_company'),
    path('transaction/', views.TransactionsBetweenCompanies.as_view(), name='transaction_frequency'),
]
