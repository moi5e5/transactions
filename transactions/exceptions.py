from rest_framework             import status
from rest_framework.exceptions  import ValidationError, PermissionDenied

class LogicException(PermissionDenied):
    status_code    = status.HTTP_400_BAD_REQUEST
    default_detail = ""
    default_code   = ""

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
