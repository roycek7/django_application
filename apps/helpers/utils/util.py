from datetime import datetime

from rest_framework import status

from apps.common.exception import ActionException
from apps.config import datetime_format
from setting.settings import logger


def validate_company(company, company_pool):
    """
    check company exists in users
    """
    return True if company in company_pool else False


def purify_datetime(subject):
    """
    purify datetime into the given format
    """
    try:
        logger.info(f'Purifying Datetime {subject}')
        return datetime.strptime(subject, datetime_format)
    except Exception:
        raise ActionException('Date: invalid_format', status.HTTP_400_BAD_REQUEST)
