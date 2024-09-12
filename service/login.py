from api.fortianalyzer_api import call_api_fortianalyzer_jsonrpc
from global_constant import GLOBAL_CONSTANT


def login_fotianalyzer():
    login_data = {
        "method": "exec",
        "params": [
            {
                "data": {
                    "passwd": "Pepsi2539!",
                    "user": "nattapan"
                },
                "url": "/sys/login/user"
            }
        ],
        "id": 1
    }
    response = call_api_fortianalyzer_jsonrpc(login_data)
    GLOBAL_CONSTANT.SESSION_ID = response.json()["session"]
