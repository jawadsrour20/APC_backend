"""
DEFINITION OF HTTP STATUS CODES

"""

HTTP_STATUS_CODE_OK = 200
HTTP_STATUS_CODE_CREATED = 201
HTTP_STATUS_CODE_BAD_REQUEST = 400 # server won't process the request due to a client error(example: malformed request syntax)
HTTP_STATUS_CODE_UNAUTHORIZED = 401 # un-authenticated user
HTTP_STATUS_CODE_FORBIDDEN = 403 # unauthorized to access a certain route (example: not admin user)
HTTP_STATUS_CODE_NOT_FOUND = 404