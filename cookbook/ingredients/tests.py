from django.test import TestCase, Client
import json

class GraphQLTestCase(TestCase):

    def setUp(self) -> None:
        self._client = Client()

    def query(self, query: str, op_name: str = None, input: dict = None):
        body = {'query': query}
        if op_name:
            body['operation_name'] = op_name
        if input:
            body['variable'] = {'input': input}

        resp = self._client.post(
            '/graphql',
            json.dumps(body),
            content_type='application/json'
        )
        json_resp = json.loads(resp.content.decode())

        return json_resp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        self.assertNotIn('errors', resp, 'Response had errors')
        self.assertEqual(resp['data'], expected, 'Response has correct data')

    def test_all_categories(self):
        resp = self.query('{allCategories {id, name}}')
        expected = {
            "allCategories": [
              {
                "id": "1",
                "name": "Dairy"
              },
              {
                "id": "2",
                "name": "Meat"
              }
            ]
          }
        self.assertResponseNoErrors(resp, { "allCategories": []})
