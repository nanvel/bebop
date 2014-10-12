import arrow
import json
import logging
import requests

from initial_data import TVS


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    response = requests.get(url='http://localhost:5000')
    logging.info(response.text)
    for tv in TVS[:5]:
        tv['airdate'] = arrow.get(tv['airdate'], ['YYYY-MM-DD', 'MMMM D, YYYY']).timestamp
        response = requests.put(
            url='http://localhost:5000/episode/{number}'.format(number=tv['number']),
            data=json.dumps(tv))
        logging.info(response.text)
    # get episode data
    response = requests.get(
        url='http://localhost:5000/episode/{number}'.format(number=2))
    logging.info(response.text)
    # remove
    response = requests.delete(
        url='http://localhost:5000/episode/{number}'.format(number=3))
    logging.info(response.text)
    # scan items
    response = requests.get(
        url='http://localhost:5000/episodes?limit={limit}&last={last}'.format(
            limit=2, last=2))
    logging.info(response.text)
    # search
    logging.info('Search results:')
    response = requests.get(
        url='http://localhost:5000/search?q={q}'.format(q='Stray Dog Strut'))
    logging.info(response.text)
