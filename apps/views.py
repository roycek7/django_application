from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from .helpers.company_helper import ThirdPartyUserVerifier
from .helpers.transaction_helper import CommercialCompanyRelationship


class VendorUserChecker(APIView):

    @permission_classes((permissions.AllowAny,))
    def post(self, request):
        action = ThirdPartyUserVerifier(request)
        return action.do_action()


class TransactionsBetweenCompanies(APIView):

    @permission_classes((permissions.AllowAny,))
    def post(self, request):
        action = CommercialCompanyRelationship(request)
        return action.do_action()
