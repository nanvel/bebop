import logging
import requests


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    response = requests.get('http://localhost:5000')
    logging.info(response.text)
