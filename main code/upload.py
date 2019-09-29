import json
import requests

data_upload = "http://192.168.0.3:8000/api/data_upload"

params1 = {"PA6d1cdf2b622776427098.87000.00"}


def upload(T):
    global data_upload
    params = {'DATA': T}
    headers = {'content-type': 'application/json'}
    response = requests.post(
        data_upload, data=json.dumps(params), headers=headers)
    # print(response)
    # print(response.text)
    return response.status_code
    # print(response.status_code)


if __name__ == "__main__":
    if upload('EA62242662024.0054.00') == 200:
        print("11200")
