class ActionException(Exception):
    def __init__(self, error=None, http_status_code=None):
        """
        Custom exception with parameters that can be accessed as attributes.
        """
        self.http_status_code = http_status_code
        self.error = error

        super(ActionException, self).__init__(self.error)
