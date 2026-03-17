import json
import requests
from flask import current_app

def log_api_request(method, url, payload=None, response=None, error=None):
    """Log details of external API requests and responses."""
    log_data = {
        "event": "external_api_call",
        "method": method,
        "url": url,
        "request_body": payload
    }
    
    if response is not None:
        log_data["response_status"] = response.status_code
        try:
            log_data["response_body"] = response.json()
        except Exception:
            log_data["response_body"] = response.text
            
    if error:
        log_data["error"] = str(error)
        
    current_app.logger.info(f"API Request Log: {json.dumps(log_data, indent=2)}")

def post(url, json_data=None, **kwargs):
    """Wrapper for requests.post with automatic logging."""
    response = None
    try:
        response = requests.post(url, json=json_data, **kwargs)
        log_api_request("POST", url, payload=json_data, response=response)
        return response
    except Exception as e:
        log_api_request("POST", url, payload=json_data, error=e)
        raise e

def get(url, params=None, **kwargs):
    """Wrapper for requests.get with automatic logging."""
    response = None
    try:
        response = requests.get(url, params=params, **kwargs)
        log_api_request("GET", url, payload=params, response=response)
        return response
    except Exception as e:
        log_api_request("GET", url, payload=params, error=e)
        raise e
