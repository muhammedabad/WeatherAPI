from typing import Any

from rest_framework import viewsets, status
from rest_framework.response import Response

from api_clients.weather_api import WeatherApiClient


class WeatherApiViewset(viewsets.ViewSet):
    def list(self, request: Any, city: str) -> Response:
        # Determine number of days, default to 1 if not provided.
        number_of_days = request.query_params.get("days", 1)

        # Raise a 400 if the number of days value is invalid.
        if not number_of_days.isdigit() or int(number_of_days) > 10:
            return Response(
                {"detail": "The value for `days` must be a valid integer not greater than 10."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Instantiate API client and get the weather forecast
        weather_api_client = WeatherApiClient()
        weather_forecast = weather_api_client.get_weather_forecast(city=city, number_of_days=number_of_days)

        # Get min/max_temperature_values
        forecast_temperatures = weather_api_client.get_forecast_temperatures(data=weather_forecast)

        # Combine all min/max values into a single list to calculate average and median temperatures.
        all_temperatures = forecast_temperatures["min_temperatures"] + forecast_temperatures["max_temperatures"]

        # Return the min, max, average and median temperatures
        response = {
            "maximum": weather_api_client.get_maximum_temperature(forecast_temperatures["max_temperatures"]),
            "minimum": weather_api_client.get_minimum_temperature(forecast_temperatures["min_temperatures"]),
            "average": weather_api_client.get_average_temperature(all_temperatures),
            "median": weather_api_client.get_median_temperature(all_temperatures),
        }

        return Response(response)
