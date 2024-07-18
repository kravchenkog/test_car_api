from pytest import fixture, mark
from conftest import Api
import os

class TestCheckJettaReceiverBehavior_JsonSchema:
    @fixture(autouse=True, scope='function')
    def __get_fixture(self, api: Api):
        self.api = api
        
    @mark.api_tests
    def test_api_check_jetta_endpoint_sucessfully(self):
        """
        Check jetta enpoint response json shema
        schemas/jetta_schema.json
        """
        body = {
            "action": "add",
            "car": {
                "make": "Volkswagen",
                "model": "Jetta"}
            }
        response =  self.api.rest.post(
            url="http://my-server.com:5002/jetta-receiver",
            json=body
        )
        schema_path = os.path.join(self.api.jsv.path_to_schemas, "rotationByVoyage.json")
        assert self.api.jsv.is_response_valid(
            json_response=response,
            schema_path=os.path.join(self.api.jsv.root_path_schemas, "jetta_schema.json")
        )