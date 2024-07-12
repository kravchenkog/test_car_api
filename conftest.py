import pytest
import os
from dataclasses import dataclass

from tools.api.rest import Rest
from tools.api.validators import JsonSchemaValidator


@dataclass
class Api:
    rest: Rest
    jsv: JsonSchemaValidator
    
@pytest.fixture(autouse=False)
def api(rest, json_validation):
    return Api(
        rest=rest,
        jsv=json_validation
        )

@pytest.fixture(autouse=False)
def rest():
    return Rest()

@pytest.fixture(autouse=False)
def json_validation():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "schemas"
        )
    return JsonSchemaValidator(root_path_schemas=path)

