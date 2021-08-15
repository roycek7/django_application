from abc import ABC, abstractmethod

from rest_framework import status

from apps.common.exception import ActionException
from apps.helpers.utils.util import validate_company
from setting.settings import database
from setting.settings import logger


class AbstractCompany(ABC):
    """
    Base abstract class to force function implementation.
    """
    @abstractmethod
    def check_company(self):
        pass

    @abstractmethod
    def validate_params(self):
        pass

    @abstractmethod
    def do_action(self):
        pass


class VerifyCompany(AbstractCompany):
    """
    Common attributes in both the endpoints are validated here
    """
    def __init__(self, name):
        self.third_party_company = name
        self.database = database

    def check_company(self):
        if not validate_company(self.third_party_company, list(set(self.database.vendor_name.to_list()))):
            logger.error(f'Given company {self.third_party_company} does not exist in vendor list.')
            raise ActionException(f'{self.third_party_company} Vendor Does Not Exist!', status.HTTP_404_NOT_FOUND)

    def validate_params(self):
        if not self.third_party_company:
            logger.error(f'Given vendor company {self.third_party_company} cannot be empty.')
            raise ActionException("Vendor Name is required!", status.HTTP_400_BAD_REQUEST)

    def do_action(self):
        self.validate_params()
        self.check_company()
