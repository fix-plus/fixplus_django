import requests
from typing import Dict, Optional

from django.conf import settings


def get_geocoding(address: str) -> Optional[Dict]:
    # Input validation
    if not address or not isinstance(address, str) or not address.strip():
        raise ValueError("Invalid or empty address provided")

    # Clean and format address
    cleaned_address = ' '.join(address.strip().split())

    # API endpoint and headers
    url = f"https://api.neshan.org/v6/geocoding?address={cleaned_address}"
    headers = {"Api-Key": settings.NESHAN_SERVICE_API_KEY}

    try:
        # Make API request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse response
        data = response.json()

        # Check API status
        if data.get("status") != "OK":
            error_mapping = {
                "470": "CoordinateParseError: Invalid coordinates provided",
                "480": "KeyNotFound: Invalid or missing API key",
                "481": "LimitExceeded: API request limit exceeded",
                "482": "RateExceeded: Rate limit exceeded",
                "483": "ApiKeyTypeError: API key type mismatch",
                "484": "ApiWhiteListError: API key not authorized for this request",
                "485": "ApiServiceListError: Service not allowed for this API key",
                "500": "GenericError: Unknown server error"
            }

            error_code = str(data.get("status", "500"))
            error_message = error_mapping.get(error_code, f"Unknown error: {error_code}")
            raise Exception(error_message)

        # Return successful response
        return {
            "status": data["status"],
            "latitude": data["location"]["y"],
            "longitude": data["location"]["x"],
        }

    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error: {response.status_code} - {str(http_err)}")

    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to the Neshan API")

    except requests.exceptions.Timeout:
        raise Exception("Request to Neshan API timed out")

    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Request error: {str(req_err)}")

    except KeyError as key_err:
        raise Exception("Invalid response format from Neshan API")

    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")