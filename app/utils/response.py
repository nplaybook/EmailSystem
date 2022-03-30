from typing import Dict, Any, List


def success_response(message: str, data: List[Dict[str, Any]] = []) -> Dict[str, Any]:
    """Generate template for success response
    
    :param message: simple message that tells request success
    :param data: data that will be delivered
    :return: dictionary that will be used as success response
    """

    if data is None:
        data = []
    return { "result": "Success", "message": message, "data": data }

def error_response(message: str, err: str) -> Dict[str, Any]:
    """Generate template for success response
    
    :param message: simple message that tells request fails
    :param err: error message that will be delivered
    :return: dictionary that will be used as fail response
    """

    return { "result": "Fail", "message": message, "err": err, "data": [] }