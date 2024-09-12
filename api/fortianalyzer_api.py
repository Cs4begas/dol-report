import requests
import os
from global_constant import GLOBAL_CONSTANT

def call_api_fortianalyzer_jsonrpc(data):
    
  headers = {'Content-Type': 'application/json'}
  response = requests.post(GLOBAL_CONSTANT.FORTIANALYZER_URL_JSONRPC, headers=headers, json=data, verify=False) # Disable SSL certificate verification if needed

  # Handle potential errors (e.g., check response status code)
  response.raise_for_status()
  return response