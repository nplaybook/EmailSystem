from abc import ABC, abstractmethod
from typing import NoReturn, Union

from app.library.typing import JSON_ARRAY, JSON


class Response(ABC):

    def __init__(self) -> NoReturn:
        pass

    @abstractmethod
    def generate_response() -> JSON:
        pass


class SuccessResponse(Response):

    def __init__(self, message: str, data: JSON_ARRAY = None) -> NoReturn:
        """Generate template for success response

        :param message: simple message that tells request success
        :param data: data that will be delivered
        """
        self.message = message
        self.data = [] if isinstance(data, type(None)) else data

    def generate_response(self) -> JSON:
        """Generate response template.

        :return: JSON that will be send to client as success response
        """

        return {
            "result": "Success",
            "message": self.message,
            "data": self.data
            }


class ErrorResponse(Response):

    def __init__(
        self,
        message: str,
        error: Union[str, JSON_ARRAY]
    ) -> NoReturn:
        """Generate template for error response

        :param message: simple message that tells in general what error occur
        :param error: error detail
        """

        self.message = message
        self.error = error

    def generate_response(self) -> JSON:
        """Generate response template.

        :return: JSON that will be send to client as fail response
        """

        return {
            "result": "Fail",
            "message": self.message,
            "err": self.error,
            "data": []
            }
