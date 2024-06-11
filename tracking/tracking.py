import os
from enum import Enum

import requests
import xmltodict

from utils import pp

class TrackingRefereceTypes(Enum):
    ArcBestPro = "A"
    BillOfLading = "B"
    PurchaseOrder = "P"
    CustomerReference = "C"
    PickupConfirmation = "K"


def get_tracking_data(tracking_number: str,
                      reference_type: TrackingRefereceTypes, arcbest_api_key: str,
                      arcbest_tracking_api_endpoint: str = "https://www.abfs.com/xml/tracexml.asp") -> dict | None:

    response_dict = None

    post_body = {
        'ID': arcbest_api_key,
        'RefNum': tracking_number,
        'RefType': reference_type.value
    }
    print(f"Arcbest API request: {post_body}")
    response = requests.post(url=arcbest_tracking_api_endpoint, params={'api_key': arcbest_api_key}, data=post_body)
    if response.status_code == 200:
        response_dict = xmltodict.parse(response.text)
        print(f'Arcbest API response dict: {pp.pprint(response_dict)}')
    else:
        print(f'Arcbest API request failed with status code: {response.status_code}')

    return response_dict


if __name__ == "__main__":
    pp.pprint(get_tracking_data(tracking_number='I169250841',
                            reference_type=TrackingRefereceTypes.ArcBestPro,
                            arcbest_api_key=os.environ.get('ARCBEST_API_KEY')))




