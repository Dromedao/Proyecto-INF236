import unittest
import requests
import json

class TestEmail(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000/send_email"

    @classmethod
    def tearDownClass(cls):
        pass

    # Pruebas del endpoint /send_email
    def test_send_email_invalid_types(self):
        """
        Test para verificar el envio de datos de distinto tipo
        """
        response = requests.get(self.base_url, json={
            "name": "John Doe",
            "email": "john.doe@usm.cl",
            "type_of": "",
            "state": "0",
            "decision": "1"
        })

        self.assertEqual(
            response.status_code,
            422
        )

    def test_send_email_invalid_payload(self):
        """
        Test para verificar el manejo de una carga util invalida al enviar un correo electronico.
        """
        response = requests.get(self.base_url, json={
            "name":"John Doe",
            "email": "invalid_email"
            })
        self.assertEqual(
            response.status_code,
            422
        )

class TestContactDecision(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:8000/contact_decision"

    @classmethod
    def tearDownClass(cls):
        pass

    def test_contact_decision_update_existing_contact(self):
        """
        Test para verificar el caso de intentar actualizar una tabla no existente
        """
        response = requests.patch(self.base_url, json={
            "name":"John Doe",
            "email": "invalid_email@gmail.com",
            "type_of": "",
            "decision": 0,
            "state": 0
            })
        self.assertEqual(
            response.status_code,
            422
        )

    def test_contact_decision_invalid_values(self):
        """
        Test para verificar el caso de intentar actualizar con datos invalidos
        """
        response = requests.patch(self.base_url, json={
            "name": 1, #Debería ser STRING
            "email": "Rocopintura@gmail.Com",
            "type_of": "",
            "decision": "0", #Debería ser INT
            "state": "0" #Debería ser INT
            })
        self.assertEqual(
            response.status_code,
            404
        )

if __name__ == "__main__":
    unittest.main()