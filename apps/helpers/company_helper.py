from rest_framework import status

from apps.common.base_action import BaseAction
from apps.helpers.base import VerifyCompany
from apps.helpers.utils.util import validate_company
from setting.settings import logger


class VendorHelper(VerifyCompany):
    """
    This class is responsible for checking if vendor_name exist among company_users. Authentication variable
    can be access as a property.
    """
    def __init__(self, name):
        super(VendorHelper, self).__init__(name)

        self._authentication = False

    @property
    def authentication_status(self):
        return self._authentication

    def check_user(self):
        """
        checks if third party company exists among list of company users.
        """
        if validate_company(self.third_party_company, list(set(self.database.company_name.to_list()))):
            self._authentication = True
            logger.info(f'Found {self.third_party_company} as user in db.')

    def do_action(self):
        """
        do action method is responsible for all the sequential steps required in the class
        """
        super(VendorHelper, self).do_action()

        self.check_user()


class ThirdPartyUserVerifier(BaseAction):
    """
    This class is responsible for calling the main action class and sending success response
    """
    def __init__(self, request):
        super(ThirdPartyUserVerifier, self).__init__()

        self.vendor_name = request.POST.get('third_party_company_name', None)

    def _produce_response(self):
        """
        this method is only responsible for calling helper class and sending success response
        """
        vendor_verifier = VendorHelper(
            self.vendor_name
        )
        vendor_verifier.do_action()

        data = {
            'vendor_company': {self.vendor_name},
            'user': {vendor_verifier.authentication_status}
        }

        self.data = data
        self.http_status_code = status.HTTP_200_OK
