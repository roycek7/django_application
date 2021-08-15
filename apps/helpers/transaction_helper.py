from rest_framework import status

from apps.common.base_action import BaseAction
from apps.common.exception import ActionException
from apps.helpers.base import VerifyCompany
from apps.helpers.utils.util import validate_company, purify_datetime
from setting.settings import logger


class FindTransactionMetric(VerifyCompany):
    """
    This class is responsible for getting the number of transaction between two companies given a date range.
    """
    def __init__(self, company_name, company_vendor, from_date, to_date):
        super(FindTransactionMetric, self).__init__(company_vendor)

        self.company = company_name
        self.from_date = from_date
        self.to_date = to_date

        self.transactions = None

    def get_data(self):
        """
        filters data from the database by companies and date_range
        """
        filtered_data = self.database[(self.database.company_name == self.company) &
                                      (self.database.vendor_name == self.third_party_company)]

        if not filtered_data.empty:
            filtered_data = filtered_data[(filtered_data.approved_date.astype('datetime64[ns]') > self.from_date) &
                                          (filtered_data.approved_date.astype('datetime64[ns]') <= self.to_date)]

        self.transactions = filtered_data.shape[0]
        logger.info(f'Found {self.transactions} number of transaction between {self.company} '
                    f'and {self.third_party_company}')

    def check_company(self):
        """
        check if company exists among users else raises exception
        """
        super().check_company()

        company_pool = list(set(self.database.company_name.to_list()))

        if not validate_company(self.company, company_pool):
            logger.error(f'Given company {self.company} does not exist in db.')
            raise ActionException(f'Company not found: {self.company}', status.HTTP_404_NOT_FOUND)

    def validate_datetime(self):
        """
        validates datetime into the set format and raises exception if from date is greater than to date
        """
        if self.from_date:
            self.from_date = purify_datetime(self.from_date)

        if self.to_date:
            self.to_date = purify_datetime(self.to_date)

        if self.from_date >= self.to_date:
            logger.error(f'{self.from_date} cannot be greater than {self.to_date}')
            raise ActionException('to_date, to_date must be bigger than from_date', status.HTTP_400_BAD_REQUEST)

    def validate_params(self):
        """
        check if parameters are valid
        """
        super(FindTransactionMetric, self).validate_params()

        if not self.company:
            logger.error(f'{self.company} cannot be empty.')
            raise ActionException("Company Name is missing!", status.HTTP_400_BAD_REQUEST)

        if not (self.from_date and self.to_date):
            logger.error(f'{self.from_date} and {self.to_date} cannot be empty.')
            raise ActionException("Date Range is missing!", status.HTTP_400_BAD_REQUEST)

    def do_action(self):
        """
        do action method is responsible for all the sequential steps required in the class
        """
        super(FindTransactionMetric, self).do_action()

        self.validate_datetime()
        self.get_data()

        return self


class CommercialCompanyRelationship(BaseAction):
    """
    This class is responsible for calling the main action class and sending success response
    """
    def __init__(self, request):
        super(CommercialCompanyRelationship, self).__init__()

        self.first_company = request.POST.get('company_name', None)
        self.second_company = request.POST.get('company_vendor', None)
        self.from_date = request.POST.get('from_date', None)
        self.to_date = request.POST.get('to_date', None)

    def _produce_response(self):
        """
        this method is only responsible for calling helper class and sending success response
        """
        vendor_verifier = FindTransactionMetric(
            self.first_company,
            self.second_company,
            self.from_date,
            self.to_date
        )
        entities = vendor_verifier.do_action()

        self.data = {
            'companies': f'{self.first_company} & {self.second_company}',
            'transactions': {entities.transactions}
        }
        self.http_status_code = status.HTTP_200_OK
