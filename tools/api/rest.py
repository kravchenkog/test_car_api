from collections import namedtuple
from json import dumps as json_dumps, JSONDecodeError
import logging

from dataclasses import dataclass
from .validators import JsonSchemaValidator
from requests import Session

Response = namedtuple('Response', ['status_code', 'body', 'json'])

LOGGER = logging.getLogger(__name__)

@dataclass(frozen=True)
class Method:
    post: str = "POST"
    get: str = "GET"
    put: str = "PUT"

class Rest:

    def __init__(self):
        """
        Initializing Base Api object \n
        :param session: Rest session
        """
        self.session = Session()

    def clear_cookies(self):
        """
        Method to clear rest session cookies inside BaseApi object
        """
        self.session.clear_cookies()

    def clear_auth_header(self):
        """
        Method to remove rest session authorization header (for session with Bearer token)
        """
        self.session.headers.pop("Authorization")

    def send_request(self,
                     method: str,
                     url: str,
                     log_request: bool = False,
                     log_response: bool = False,
                     auth=None,
                     **kwargs) -> Response:
        """
        Basic method for sending request

        :param method: HTTP method
        :param url: URL where request is to be sent
        :param log_request: Boolean value whether to log request body/params/data
        :param log_response: Boolean value whether to log response body
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code (int), body (str) and json (dict or None, if not in JSON format)
        """
        LOGGER.info(f"API: Request: {method} {url}")
        if log_request:
            for param, value in kwargs.items():
                if value:
                    LOGGER.info(json_dumps(value))
            
        response = self.session.request(method=method, url=url, auth=auth, **kwargs)
        # Prepare needed response attributes to build own Response object
        resp_status_code = response.status_code
        resp_body = response.text
        try:
            resp_json = response.json()
        except JSONDecodeError:
            resp_json = None

        # Log results
        LOGGER.info(f"API: Response status: {resp_status_code}")
        if log_response and resp_body:
            LOGGER.info(f"API: Response body: {resp_body}")
            
        resp = Response(status_code=resp_status_code,
                        body=resp_body,
                        json=resp_json)

        return resp

    def get(self,
            url: str,
            params: dict = None,
            log_request: bool = False,
            log_response: bool = False,
            **kwargs) -> Response:
        """
        GET request

        :param url: URL where request is to be sent
        :param params: request query parameters
        :param log_request: Boolean value whether to log request body/params/data
        :param log_response: Boolean value whether to log response body
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        return self.send_request(method="GET",
                                 url=url,
                                 params=params,
                                 log_request=log_request,
                                 log_response=log_response,
                                 **kwargs)

    def post(self,
             url: str,
             log_request: bool = False,
             log_response: bool = False,
             auth=None,
             **kwargs) -> Response:
        """
        POST request

        :param url: URL where request is to be sent
        :param body: Request body
        :param log_request: Boolean value whether to log request body/params/data
        :param log_response: Boolean value whether to log response body
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        return self.send_request(method="POST",
                                 url=url,
                                 log_request=log_request,
                                 log_response=log_response,
                                 auth=auth,
                                 **kwargs)

    def patch(self,
              url: str,
              body: dict = None,
              data: dict = None,
              log_request: bool = False,
              log_response: bool = False,
              **kwargs) -> Response:
        """
        PATCH request

        :param url: URL where request is to be sent
        :param body: Request body
        :param data: Request data (payload)
        :param log_request: Boolean value whether to log request body/params/data
        :param log_response: Boolean value whether to log response body
        :param kwargs: Additional arguments (body, payload etc)
        :return: Response object with status_code and body
        """
        return self.send_request(method="PATCH",
                                 url=url,
                                 json=body,
                                 data=data,
                                 log_request=log_request,
                                 log_response=log_response,
                                 **kwargs)
