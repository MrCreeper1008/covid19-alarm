from typing import Dict

"""Represent HTTP status code 400 Bad Request"""
HTTP_BAD_REQUEST = 400

"""Indicates that the request contains invalid parameters"""
ERRCODE_INVALID_PARAMETERS = "INVALID_PARAMETERS"


def http_response(status: str, data: Dict[str, str]) -> Dict[str, any]:
    """
    Returns a standardized response of this server in the shape of:
    {
        "status": "..." // Can be: error, success.
        "data": {...} // The data associated with this response.
    }
    """
    return {
        "status": status,
        "data": data,
    }


def http_error_response(code: str, details: str) -> Dict[str, str]:
    """
    Returns an error response with the following shape:
    {
        "status": "error",
        "data": {
            "error": "..." // The error code of the request
            "details:": "..." // Details about the error
        }
    }

    :params code: The error code of the request
    :params details: Details about the error
    """
    return http_response(
        status="error",
        data={
            "error": code,
            "details": details,
        },
    )


def http_success_response(payload: Dict[str, any]) -> Dict[str, any]:
    """
    Returns a success response in the following shape:
    {
        "status": "success",
        "data": {...} // the given payload
    }

    :params payload: The data associated with the response
    """
    return http_response(
        status="success",
        data=payload,
    )
