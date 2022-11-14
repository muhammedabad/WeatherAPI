import statistics

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError, APIException


class RequestMethods:
    GET = "get"


class WeatherApiClientException(Exception):
    pass


class WeatherApiClient:
    def __init__(self) -> None:
        """
        Set global attrs for this class as required.
        """
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_BASE_URL

    def execute(self, method: str, request_params: dict) -> dict | APIException:
        """
        Executes the given request with provided parameters.
        """

        # Add API key to request params
        request_params["key"] = self.api_key

        # Execute the request
        response = getattr(requests, method)(url=self.base_url, params=request_params)

        # Ensure request was successful, otherwise raise a suitable exception
        if response.ok:
            return response.json()

        if response.status_code == 400:
            raise ValidationError(
                detail={"detail": "Invalid request, please check your input parameters and try again."},
            )

        raise WeatherApiClientException("There was a problem processing your request, please try again later.")

    def get_weather_forecast(self, city: str, number_of_days: int) -> dict:
        """
        Returns the forecast for the provided city and number of days.
        """

        # Define params for this API call
        url_params = {
            "q": city,
            "days": number_of_days
        }

        # Execute the request
        response = self.execute(
            method=RequestMethods.GET,
            request_params=url_params
        )

        # Return response data
        return response

    @staticmethod
    def get_forecast_temperatures(data: dict) -> dict:
        """
        Extract temperature values from API response.
        """

        # Define lists to store min/max temperature values.
        min_temperatures = []
        max_temperatures = []

        # For each day, append to the relevant list
        for day in data["forecast"]["forecastday"]:
            min_temperatures.append(day["day"]["mintemp_c"])
            max_temperatures.append(day["day"]["maxtemp_c"])

        # Return the result
        return {
            "min_temperatures": min_temperatures,
            "max_temperatures": max_temperatures
        }

    @staticmethod
    def get_minimum_temperature(data: list) -> float:
        return min(data)

    @staticmethod
    def get_maximum_temperature(data: list) -> float:
        return max(data)

    @staticmethod
    def get_average_temperature(data: list) -> float:
        return round(sum(data) / len(data), 1)

    @staticmethod
    def get_median_temperature(data: list) -> float:
        return round(statistics.median(data), 1)




