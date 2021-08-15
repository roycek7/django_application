from django.urls import path

from . import views

urlpatterns = [
    path('verify/', views.VerifyCompany.as_view(), name='verify_company'),
    path('transaction/', views.TransactionsCompany.as_view(), name='transaction_frequency'),
]
