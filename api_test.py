import unittest
import requests

class Test(unittest.TestCase):

    def test_invalid_get(self):
        result = requests.get('http://localhost:8080/qwerty/')
        response_body = str(result.content)
        self.assertIn('Unknown time zone', response_body)

    def test_get_gmt(self):
        result = requests.get('http://localhost:8080/')
        response_body = str(result.content)
        self.assertIn('GMT', response_body)
    
    def test_get_moscow(self):
        result = requests.get('http://localhost:8080/Europe/Moscow')
        response_body = str(result.content)
        self.assertIn('MSK', response_body)

    def test_invalid_post(self):
        result = requests.post('http://localhost:8080/qwerty/')
        response_body = str(result.content)
        self.assertIn('Unknown request', response_body)

    def test_post_invalid_convert(self):
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        data = '{"date": "invalid-date", "tz": "EST", "target_tz": "Europe/Moscow"}'
        params = ""
        result = requests.post('http://localhost:8080/api/v1/convert', params=params, headers=headers, data=data)
        response_body = str(result.content)
        self.assertIn('Invalid input data', response_body)
    
    def test_post_invalid_diffdate(self):
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        data = '{"first_date": "12.06.2024 22:21:05", "first_tz": "PPP","second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"}'
        params = ""
        result = requests.post('http://localhost:8080/api/v1/datediff', params=params, headers=headers, data=data)
        response_body = str(result.content)
        self.assertIn('Invalid input data', response_body)

    def test_invalid_post_path(self):
        result = requests.post('http://localhost:8080/api/v1/qwerty')
        response_body = str(result.content)
        self.assertIn('Unknown request', response_body)
        
    def test_post_convert(self):
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        data = '{"date": "12.20.2021 22:21:05", "tz": "EST"}'
        params = ""
        result = requests.post('http://localhost:8080/api/v1/convert/GMT', params=params, headers=headers, data=data)
        response_body = str(result.content)
        self.assertIn('GMT', response_body)

    def test_post_datediff(self):
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        data = '{"first_date": "12.06.2024 22:21:05", "first_tz": "EST","second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"}'
        params = ""
        result = requests.post('http://localhost:8080/api/v1/datediff', params=params, headers=headers, data=data)
        response_body = str(result.content)
        self.assertIn('11468345.0', response_body)

if __name__ == '__main__':
    unittest.main()
