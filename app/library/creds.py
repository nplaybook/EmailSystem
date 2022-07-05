import base64
from typing import NoReturn, Union


class CredUtils:

    def __init__() -> NoReturn:
        pass

    @staticmethod
    def encode(
        text: str,
        method: str = "utf-8",
        as_string: bool=True
    ) -> Union[str, bytes]:
        """Encode inputed string via a specific method

        :param text: string value that will be encoded
        :param method: any transformation method available
        :param as_string: whether the return value is formatted as
        string or keep as bytes
        """

        encoded_text = base64.b64encode(text.encode(method))
        return encoded_text.decode(method) if as_string else encoded_text

    @staticmethod
    def decode(
        text: Union[str, bytes],
        method: str = "utf-8",
    ) -> Union[str, bytes]:
        """Decode inputed string via a specific method

        :param text: encode input that will be decoded
        :param method: any transformation method available
        """

        return base64.b64decode(text).decode(method)
