import requests
import json
from config import currency


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(
                f'Невозможно перевести одинаковые валюты "{base}".')

        try:
            base_ticker = currency[base][0]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту "{base}".\n\n' \
                'Узнать список доступных валют по команде: /values'
            )
        try:
            quote_ticker = currency[quote][0]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту "{quote}".\n\n' \
                'Узнать список доступных валют по команде: /values'
            )
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(
                f'Не удалось обработать количество "{amount}".')

        url = 'https://min-api.cryptocompare.com/data/price?fsym='
        r = requests.get(f'{url}{base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[currency[quote][0]]

        return total_base
