import json
from pydantic import BaseModel


def json_loader(message_model):
    """
    This function is used to handle the json data and return the json data in a dictionary format.
    """
    return json.loads(message_model)


def json_dump(message_model: BaseModel):
    """
    This function is used to handle the json data and return the json data in a dictionary format.
    """
    return json.dumps(message_model.model_dump())
