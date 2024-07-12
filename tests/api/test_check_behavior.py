from pytest import fixture, mark
from conftest import Api

class TestCheckJettaReceiverBehavior:
    @fixture(autouse=True, scope='function')
    def __get_fixture(self, api: Api):
        self.api = api
        
    @mark.api_tests
    def test_api_check_jetta_endpoint_sucessfully(self):
        """
        Check jetta enpoint sucessfull 
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
        assert response.status_code == 200, "The response status code is not 200"
        assert response.json['result'] == "added successfully", f"The result of the response is incorect: \
                actual  {response.json['result']}"
        
    @mark.api_tests
    def test_api_check_jetta_endpoint_validity(self):
        """
        Check jetta enpoint sucessfull 
        """
        make = "Volkswagen"
        model = "Jetta"
        body = {
            "action": "add",
            "car": {
                "make": make,
                "model": model}
            }
        response =  self.api.rest.post(
            url="http://my-server.com:5002/jetta-receiver",
            json=body
        )
        assert response.json['car']['make'] == make, f"The make in the response is incorrect: \
                        expected {make}, actual {response.json['car']['make']}"
        assert response.json['car']['model'] == model, f"The model in the response is incorrect: \
                        expected {model}, actual {response.json['car']['model']}"
                        
                        
    @mark.api_tests
    def test_api_check_jetta_endpoint_invalid_data(self):
        """
        Check jetta enpoint invalid data 
        """
        body = {
            "action": "add",
            "car": {
                "make": "",
                "model": ""}
            }
        response =  self.api.rest.post(
            url="http://my-server.com:5002/jetta-receiver",
            json=body
        )
        assert response.status_code == 204, "The response status code is not 200"
        assert response.json['result'] == "No Content", f"The result of the response is incorect: \
                actual  {response.json['result']}"
                
    @mark.api_tests
    def test_api_check_jetta_endpoint_get(self):
        """
        Check jetta enpoint get 
        """
        response =  self.api.rest.get(
            url="http://my-server.com:5002/jetta-receiver",
        )
        assert response.status_code == 405, f"The response status code is not 405, actual {response.status_code}"
    
        
        