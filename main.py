from typing import Optional, Dict, Any
from urllib.parse import urlencode
import requests

BaseAPIURL = "https://api.ghanapostgps.com/v2/PublicGPGPSAPI.aspx"

CorsByPass = [
    "Base-Url",
    "Client-IP",
    "Http-Url",
    "Proxy-Host",
    "Proxy-Url",
    "Real-Ip",
    "Redirect",
    "Referer",
    "Referrer",
    "Refferer",
    "Request-Uri",
    "Uri",
    "Url",
    "X-Client-Ip",
    "X-Forwarded-For",
    "Cf-Connecting-Ip",
    "X-Client-IP",
    "X-Custom-IP-Authorization",
    "X-Forward-For",
    "X-Forwarded-By",
    "X-Forwarded-By-Original",
    "X-Forwarded-For-Original",
    "X-Forwarded-For",
    "X-Forwarded-Host",
    "X-Forwarded-Server",
    "X-Forwarder-For",
    "X-HTTP-Destinationurl",
    "X-Http-Host-Override",
    "X-Original-Remote-Addr",
    "X-Original-Url",
    "X-Originating-IP",
    "X-Proxy-Url",
    "X-Remote-Addr",
    "X-Remote-IP",
    "X-Rewrite-Url",
    "X-True-IP",
    "Fastly-Client-Ip",
    "True-Client-Ip",
    "X-Cluster-Client-Ip",
    "X-Forwarded",
    "Forwarded-For",
    "Forwarded",
    "X-Real-Ip",
]

Config = {
    "ApiURL": BaseAPIURL,
    "Authorization": "QW5kcm9pZEtleTpTV3RsYm01aFFGWnZhMkZqYjIwMFZRPT0:",
    "AsaaseUser": "SWtlbm5hQFZva2Fjb200VQ==",
    "LanguageCode": "en",
    "Language": "English",
    "DeviceId": "AndroidKey",
    "AndroidCert": "49:DD:00:18:04:D3:47:D0:77:44:A0:B3:93:47:4F:BE:B6:7E:D7:67",
    "AndroidPackage": "com.ghanapostgps.ghanapost",
    "Country": "GH",
    "CountryName": "Ghana",
}


def get_api_keys(config) -> str:
    """Return env-like multiline string containing the API keys/values."""
    env_data = (
        f'GPGPS_apiURL="{config.get("ApiUrl")}"\n'
        f'GPGPS_authorization="{config.get("Authorization")}"\n'
        f'GPGPS_asaaseUser="{config.get("AsaaseUser")}"\n'
        f'GPGPS_languageCode="{config.get("LanguageCode")}"\n'
        f'GPGPS_language="{config.get("Language")}"\n'
        f'GPGPS_deviceId="{config.get("DeviceId")}"\n'
        f'GPGPS_androidCert="{config.get("AndroidCert")}"\n'
        f'GPGPS_androidPackage="{config.get("AndroidPackage")}"\n'
        f'GPGPS_countryName="{config.get("CountryName")}"\n'
        f'GPGPS_country="{config.get("Country")}"'
    )
    return env_data


def get_data_request(values: Dict[str, Any]):
    """Encode form values into application/x-www-form-urlencoded string."""
    return urlencode(values)


def api_request(method: str, config, payload: Optional[str]):
    """
    Make an HTTP request using the given method to params.ApiURL with the provided payload.
    payload should be the urlencoded string (from get_data_request).
    Returns response text (or exception text on error).
    """
    headers = {
        "Authorization": "Basic " + config.get("Authorization")
        if config.get("Authorization")
        else "",
        "LanguageCode": config.get("LanguageCode"),
        "Language": config.get("Language"),
        "CountryName": config.get("CountryName"),
        "DeviceId": config.get("DeviceId"),
        "X-Android-Cert": config.get("AndroidCert"),
        "AsaaseUser": config.get("AsaaseUser"),
        "Country": config.get("Country"),
        "X-Android-Package": config.get("AndroidPackage"),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Add all the CORS bypass headers with a dummy value as in the original
    for h in CorsByPass:
        headers[h] = "127.0.0.1"

    try:
        print(headers)
        resp = requests.request(
            method=method.upper(),
            url=config.get("ApiURL"),
            data=payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        # Mimic the Go code's loose error handling by returning the error string
        return str(e)


def get_location(code: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "GetLocation",
        "GPSName": code,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def get_address(latitude: str, longitude: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "GetGPSName",
        "Lati": latitude,
        "Longi": longitude,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def format_string(address: str):
    # Equivalent to: strings.ToUpper(strings.Trim(address, "")) then split on "-" and join.
    # Trim with empty cutset does nothing in Go, so we just strip whitespace in Python.
    return "".join(address.strip().upper().split("-"))


def is_valid_gp_address(address: str):
    address = format_string(address)
    is_valid = True
    if len(address) < 9:
        is_valid = False
    return is_valid, address


def get_user_address(phone: str, uuid: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "GetUserAddress",
        "MSISDN": phone,
        "DeviceID": uuid,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def sip_details(phone: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "GetSIPDetails",
        "MSISDN": phone,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def add_customer(
    first_name: str, last_name: str, phone: str, uuid: str, defaults: Dict
) -> str:
    values = {
        "AsaaseLogs": "",
        "Action": "AddCustomer",
        "FirstName": first_name,
        "LastName": last_name,
        "MobileNumber": phone,
        "Msisdn": phone,
        "IMSI": phone,
        "IMEI": phone,
        "DeviceID": uuid,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def verify_sms(phone: str, code: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "VerifyCode",
        "GPSName": code,
        "MSISDN": phone,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def send_login_sms(phone: str, defaults: Dict):
    values = {
        "AsaaseLogs": "",
        "Action": "SendSMS",
        "GPSName": phone,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)


def print_(*data):
    print(*data)


if __name__ == "__main__":
    # Small usage example (replace values with real ones)
    defaults = { 
        "ApiURL":BaseAPIURL,
        "Authorization":"QW5kcm9pZEtleTpTV3RsYm01aFFGWnZhMkZqYjIwMFZRPT0=",
        "AsaaseUser":"SWtlbm5hQFZva2Fjb200VQ==",
        "LanguageCode":"en",
        "Language":"English",
        "DeviceId":"AndroidKey",
        "AndroidCert":"49:DD:00:18:04:D3:47:D0:77:44:A0:B3:93:47:4F:BE:B6:7E:D7:67",
        "AndroidPackage":"com.ghanapostgps.ghanapost",
        "Country":"GH",
        "CountryName":"Ghana",
}

    # Example: get location by GPS code
    example_code = ""
    print_("Requesting location for", example_code)
    response = get_user_address("+233244079765",defaults.get("DeviceId"), defaults)
    # response = sip_details("+233531810252", defaults)
    print_("Response:", response)
