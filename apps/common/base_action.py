from rest_framework.response import Response

from apps.common.exception import ActionException


class BaseAction:
    """
    This is a base action class responsible for catching any exception raised in the api endpoints. Returns
    response with the input parameters.
    """
    def __init__(self):
        self.http_status_code = None
        self.data = None

    def do_action(self):
        try:
            self._produce_response()
        except ActionException as e:
            self.http_status_code = e.http_status_code
            self.data = e.error
        except Exception:
            self.http_status_code = 500
            self.data = 'Something went wrong!'

        return self._process_response()

    def _produce_response(self):
        pass

    def _process_response(self):
        """
        Return response with data passed in either produce response or action exception.
        """
        return Response(self.data, status=self.http_status_code, content_type='application/json')
