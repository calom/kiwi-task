import time
import requests

HEADERS = {
    'Content-Type': 'application/json'
}
HTTPS = 'https'
SKYPICKER_DOMAIN = 'api.skypicker.com'
PARTNER_ID = 'checker969checker969'


def getLocationsInfo(city):
    params = {
        'term': {city},
        'locale': 'en-US',
        'location_types': 'airport',
        'limit': 10,
        'active_only': 'true',
        'sort': 'name'
    }
    url = f'{HTTPS}://{SKYPICKER_DOMAIN}/locations'
    r = requests.get(url, headers=HEADERS, params=params).json()
    return r


def getAirportCode(city):
    locations = getLocationsInfo(city)['locations']
    airport_code = locations[0]['code'] if locations is not None else 'invalid'
    # return getLocationsInfo(city)['locations']['code']
    return airport_code


def getBookingToken(city_from, city_to):
    params = {
        'partner': PARTNER_ID,
        'fly_from': f'airport:{city_from}',
        'fly_to': f'airport:{city_to}'
    }
    url = f'{HTTPS}://{SKYPICKER_DOMAIN}/flights'
    r = requests.get(url, headers=HEADERS, params=params).json()
    token = r['data'][0]['booking_token']
    return token


def checkFlights(token):
    params = {
        'v': 2,
        'booking_token': token,
        'bnum': 0,
        'pnum': 1,
        'affily': PARTNER_ID,
        'adults': 1,
        'children': 0,
        'infants': 0
    }
    url = f'{HTTPS}://booking-{SKYPICKER_DOMAIN}/api/v0.1/check_flights'
    r = requests.get(url, headers=HEADERS, params=params).json()
    return r


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    CITY_FROM = 'New York JFK'
    CITY_TO = 'Vienna'

    vienna_code = getAirportCode(CITY_FROM)
    jfk_to = getAirportCode(CITY_TO)

    # Verify JFK:
    jfk = getLocationsInfo(CITY_FROM)['locations'][0]
    assert jfk['name'] == 'John F. Kennedy International'
    assert jfk['int_id'] == 8353

    # Verify Vienna
    vienna = getLocationsInfo(CITY_TO)['locations'][0]
    assert vienna['name'] == 'Vienna International Airport'
    assert vienna['int_id'] == 6639
    booking_token = getBookingToken(vienna_code, jfk_to)

    while True:
        flights = checkFlights(booking_token)
        if flights['flights_invalid'] is False and flights['flights_checked'] is True and flights[
            'flights_to_check'] is False:
            break
        time.sleep(15)  # very basic but serves the purpose, async not necessary
    print('Flight successfully checked')
