import http
from pprint import pprint

import httpx
from dadata import Dadata


# token = "4d0edf2431bc01e0f64768bdcb7e893b61bde4f5"
token = "4d0edf2431bc01e0f64768bdcb7e893b"
# secret = "6c17e67baf5ad675a4c1e104e17cb5ff3a1d91ab"
secret = "6c17e67baf5ad675a4c1b"


try:
    with Dadata(token, secret) as dadata:
        result = dadata.suggest("address", query="новосибирск октябрьский район", count=1, language="ru")

        # result = result[0]
        #
        # print(result['data']['geo_lat'], result['data']['geo_lon'])
        # print(result['unrestricted_value'])
        # print(result['data']['fias_level'])
        print(result)
except httpx.HTTPStatusError as e:
    print("error")
    print(http.HTTPStatus.FORBIDDEN == 402)
    raise e