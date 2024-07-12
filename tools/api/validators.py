"""
Response validator wrapper
"""
from typing import List
from json import dumps as json_dumps
from os import path
import jsonref
from pathlib import Path

import jsonschema


class JsonSchemaValidator:
    """
    Class of JSON schema validator
    """           

    def __init__(self, root_path_schemas):
        self.validator = jsonschema.Draft7Validator
        self.root_path_schemas = path.abspath(root_path_schemas)

    @staticmethod
    def get_schema_from_the_file(path_to_file: str, encoding=None) -> dict:
        path = Path(path_to_file).absolute()
        with open(path_to_file, encoding=encoding) as schema_file:
            return jsonref.loads(schema_file.read(), base_uri=path.as_uri())
    
    
    def is_response_valid(self, json_response,
                          schema_path: str = None,
                          schema = None,
                          encoding=None) -> bool:
        """
        Method to validate JSON according to the schema

        :param json_response: Response received from API in JSON format (dict)
        :param schema_path: Path to json schema
        :param schema dict: parsed schema
        :param encoding: Encoding (None by default)
        :return: bool result with status (True) or raises AssertionError with error message
        """
        
        if not schema_path and not schema:
            raise Exception("at least one argument is required: schema_path or schema")
        
        if schema_path and schema:
            raise Exception("we can not use both argumens at the same time: schema_path AND schema")
        
        if json_response is None:
            raise AssertionError('Validator: Received response is not in JSON format')
        if not schema:
            schema: dict = self.get_schema_from_the_file(path_to_file=schema_path, encoding=encoding)
        ref = jsonschema.RefResolver(base_uri=f"file://{self.root_path_schemas}/", referrer=None)
        validator = self.validator(schema, resolver=ref)
        errors = validator.iter_errors(json_response)
        errors_examples = self.__get_error_examples(errors=errors)
        if errors_examples:
            errors_examples.insert(0, {"abspath": schema_path})
            error_msg = f"JSON Validator: Validation failed with error(s): {json_dumps(errors_examples, indent=2)}"
            raise AssertionError(error_msg)
        return True
    
    @staticmethod
    def __get_error_examples(errors) -> List:
        """
        Method for creating unique examples list

        :param errors: Errors object from validator
        :return: List of errors with its details
        """
        errors_examples = []
        unique_schema_path = []
        for e in errors:
            if set(e.relative_schema_path) not in unique_schema_path:
                unique_schema_path.append(set(e.relative_schema_path))
                errors_examples.append({
                    "schema_path": list(e.relative_schema_path),
                    "error_message": e.message,
                    "response_path": "".join([f"['{i}']" for i in list(e.relative_path)])
                })
        return errors_examples