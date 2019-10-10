import json
import requests

data_upload = "http://192.168.0.3:8000/api/data_upload"

params1 = "E111585004FCC6224266200240005400"
params2 = "P111585004FCC6224266206D1CDF2B0988700000"


def upload(T):
    global data_upload
    params = {'DATA': T}
    headers = {'content-type': 'application/json'}
    response = requests.post(
        data_upload, data=json.dumps(params), headers=headers)
    # print(response)
    print(response.text)
    # return response.status_code
    # print(response.status_code)


if __name__ == "__main__":
    print(upload(params2))
    # print(upload('PA6d1cdf2b622776427098.87010.00'))
