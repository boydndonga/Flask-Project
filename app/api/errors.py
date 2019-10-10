from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

# Define error_response
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'unknown_code')}
    if message:
        payload['message']=message
    response = jsonify(payload)
    response.status_code = status_code
    return response

# Define Bad Requests
def bad_request(message):
    return error_response(400, message)