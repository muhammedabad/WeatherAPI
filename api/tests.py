import pytest
import responses
from django.conf import settings

from rest_framework.test import RequestsClient, APIClient
from api_clients.weather_api import WeatherApiClient, WeatherApiClientException


class TestWeatherApiClient:
    def test_init(self):
        """
        Tests the instantation of the WeatherApiClient class.
        """

        # Instantiate client
        client = WeatherApiClient()

        # Ensure core values are correct
        assert client.api_key == settings.WEATHER_API_KEY
        assert client.base_url == settings.WEATHER_API_BASE_URL

    @responses.activate
    def test_weather_api(self, mock_centurion_weather_response):
        """
        Tests the API endpoint that processes data from weatherapi.com .
        """

        # Create mock response data
        weather_api_response = responses.Response(
            method="GET",
            url=f"{settings.WEATHER_API_BASE_URL}?q=centurion&days=2&key={settings.WEATHER_API_KEY}",
            json=mock_centurion_weather_response
        )

        # Register the response
        responses.add(weather_api_response)

        # Instantiate DRF test client
        client = APIClient()

        # Make a call to the weather endpoint and store the response json
        response = client.get('/api/locations/centurion/?days=2')
        result = response.json()

        # Ensure the correct response code is returned
        assert response.status_code == 200

        # Ensure the temperature values are correct
        assert result["maximum"] == 29.7
        assert result["minimum"] == 14.3
        assert result["average"] == 20.9
        assert result["median"] == 19.7

    def test_weather_api_invalid_days(self):
        """
        Tests the API endpoint will not accept an invalid value for the `days` query param.
        """

        # Instantiate DRF test client
        client = APIClient()

        # Make a call to the weather endpoint and store the response json
        response = client.get('/api/locations/centurion/?days=200')

        # Ensure the 400 was raised
        assert response.status_code == 400

    @responses.activate
    def test_weather_api_failed_response(self, mock_centurion_weather_response):
        # Create mock response data
        weather_api_response = responses.Response(
            method="GET",
            url=f"{settings.WEATHER_API_BASE_URL}?q=centurion&days=2&key={settings.WEATHER_API_KEY}",
            json={"detail": "An error occurred, please try again later."},
            status=500
        )

        # Register the response
        responses.add(weather_api_response)

        # Instantiate DRF test client
        client = APIClient()

        # Make a call to the weather endpoint and store the response json
        with pytest.raises(WeatherApiClientException):
            client.get('/api/locations/centurion/?days=2')
