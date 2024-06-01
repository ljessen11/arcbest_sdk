import os
from datetime import datetime
import pprint
import requests
import xmltodict

from enumerations import ShipmentClasses, PackageType, UnitsOfMeasurement, LimitedAccessOptions, TradeshowDeliveryTypes

"""
https://www.abfs.com/xml/aquotexml.asp?
DL=2&
ID=BQNED065

ShipCity=DALLAS
ShipState=TX&
ShipZip=75201&
ShipCountry=US&

ConsCity=TULSA&
ConsState=OK&
ConsZip=74104&
ConsCountry=US&

FrtLng1=48&
FrtWdth1=48&
FrtHght1=48&
FrtLWHType=IN&
UnitNo1=3&
UnitType1=PLT&
Wgt1=400&
Class1=50.0&
ShipAff=Y&

ShipMonth=05&
ShipDay=30&
ShipYear=2024
"""
pp = pprint.PrettyPrinter(indent=4)
bool_to_str = lambda x: 'Y' if x else 'N'


class ShippingParty:
    def __init__(self,
                 street_address: str,
                 city: str,
                 state: str,
                 zip: str,
                 country: str,
                 name: str | None = None,
                 name_plus: str | None = None,
                 acct_number: str | None = None,
                 submitting_party: str | None = None,
                 paying_party: str | None = None):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.name = name
        self.name_plus = name_plus
        self.acct_number = acct_number
        self.submitting_party = submitting_party
        self.paying_party = paying_party

    def as_shipper_dict(self):
        return {key: value for key, value in {
            'ShipAff': bool_to_str(self.submitting_party),
            'ShipPay': bool_to_str(self.paying_party),
            'ShipName': self.name,
            'ShipNamePlus': self.name_plus,
            'ShipAddr': self.street_address,
            'ShipCity': self.city,
            'ShipState': self.state,
            'ShipZip': self.zip,
            'ShipCountry': self.country,
            'ShipAcct': self.acct_number,
        }.items() if value is not None}

    def as_consignee_dict(self):
        return {key: value for key, value in {
            'ConsAff': bool_to_str(self.submitting_party),
            'ConsPay': bool_to_str(self.paying_party),
            'ConsName': self.name,
            'ConsNamePlus': self.name_plus,
            'ConsAddr': self.street_address,
            'ConsCity': self.city,
            'ConsState': self.state,
            'ConsZip': self.zip,
            'ConsCountry': self.country,
            'ConsAcct': self.acct_number,
        }.items() if value is not None}

    def as_third_party_dict(self):
        return {key: value for key, value in {
            'TPBAff': bool_to_str(self.submitting_party),
            'TPBPay': bool_to_str(self.paying_party),
            'TPBName': self.name,
            'TPBNamePlus': self.name_plus,
            'TPBAddr': self.street_address,
            'TPBCity': self.city,
            'TPBState': self.state,
            'TPBZip': self.zip,
            'TPBCountry': self.country,
            'TPBAcct': self.acct_number,
        }.items() if value is not None}


    def __str__(self):
        return self.name


class Commodity:
    def __init__(self, weight,
                 line_number: int,
                 shipment_class: ShipmentClasses | None = None,
                 length: float | None = None,
                 width: float | None = None,
                 height: float | None = None,
                 unit_number: int | None = None,
                 packing_type: PackageType | None = None,
                 nmfc: int | None = None):
        self.weight = weight
        self.line_number = line_number
        self.shipment_class = shipment_class
        self.length = length
        self.width = width
        self.height = height
        self.unit_number = unit_number
        self.packaging_type = packing_type
        self.nmfc = nmfc

    def as_dict(self):
        return {key: value for key, value in {
            f'Wgt{self.line_number}': self.weight,
            f'Class{self.line_number}': self.shipment_class.value if self.shipment_class else None,
            f'FrtLng{self.line_number}': self.length,
            f'FrtWdth{self.line_number}': self.width,
            f'FrtHght{self.line_number}': self.height,
            f'UnitNo{self.line_number}': self.unit_number,
            f'UnitType{self.line_number}': self.packaging_type.name if self.packaging_type else None,
            f'NMFC{self.line_number}': self.nmfc,
        }.items() if value is not None}


class ShipmentSpecifics:
    def __init__(self, shipMonth: int,
                 shipDay: int,
                 shipYear: int,
                 overall_cubic_feet: float | None = None,
                 overall_length: float | None = None,
                 overall_width: float | None = None,
                 overall_height: float | None = None,
                 measurement_unit: UnitsOfMeasurement | None = None):
        self.shipMonth = shipMonth
        self.shipDay = shipDay
        self.shipYear = shipYear
        self.cubicFeet = overall_cubic_feet
        self.overall_length = overall_length
        self.overall_width = overall_width
        self.overall_height = overall_height
        self.measurement_unit: UnitsOfMeasurement = measurement_unit

    def as_dict(self):
        return {key: value for key, value in {
            'ShipMonth': self.shipMonth,
            'ShipDay': self.shipDay,
            'ShipYear': self.shipYear,
            'FrtLng': self.overall_length,
            'FrtWdth': self.overall_width,
            'FrtHght': self.overall_height,
            'CubicFeet': self.cubicFeet,
            'FrtLWHType': self.measurement_unit.value if self.measurement_unit else None
        }.items() if value is not None}


class PickupServices:
    def __init__(self, lift_gate: bool | None = None,
                 inside: bool | None = None,
                 limited_access: bool | None = None,
                 type_of_limited_access: LimitedAccessOptions | None = None,
                 residential: bool | None = None,
                 trade_show: bool | None = None):

        if limited_access is not None and type_of_limited_access is None:
            raise ValueError('If limited_access is true, type_of_limited_access must be provided')

        self.lift_gate = lift_gate
        self.inside = inside
        self.limited_access = limited_access
        self.type_of_limited_access = type_of_limited_access
        self.residential = residential
        self.trade_show = trade_show

    def as_dict(self):
        return {key: value for key, value in {
            'Acc_GRD_PU': bool_to_str(self.lift_gate),
            'Acc_IPU': bool_to_str(self.inside),
            'Acc_LAP': bool_to_str(self.limited_access),
            'LAPType': self.type_of_limited_access.value if self.type_of_limited_access else None,
            'Acc_RPU': bool_to_str(self.residential),
            'Acc_TRDSHWO': bool_to_str(self.trade_show),
        }.items() if value is not None}


class DeliveryServices:
    def __init__(self,
                 construction_site: bool | None = None,
                 lift_gate: bool | None = None,
                 inside: bool | None = None,
                 limited_access: bool | None = None,
                 type_of_limited_access: LimitedAccessOptions | None = None,
                 residential: bool | None = None,
                 flat_bed: bool | None = None,
                 trade_show: bool | None = None,
                 trade_show_type: TradeshowDeliveryTypes | None = None):

        if limited_access is not None and type_of_limited_access is None:
            raise ValueError('If limited_access is true, the type of limited access must be provided')
        if trade_show is not None and trade_show_type is None:
            raise ValueError('If trade_show is true, the type of trade show must be provided')

        self.construction_site = construction_site
        self.lift_gate = lift_gate
        self.inside = inside
        self.limited_access = limited_access
        self.type_of_limited_access = type_of_limited_access
        self.residential = residential
        self.flat_bed = flat_bed
        self.trade_show = trade_show
        self.trade_show_type = trade_show_type

    def as_dict(self):
        return {key: value for key, value in {
            'Acc_CSD': bool_to_str(self.construction_site),
            'Acc_GRD_DEL': bool_to_str(self.lift_gate),
            'Acc_IDEL': bool_to_str(self.inside),
            'ACC_LAD': bool_to_str(self.limited_access),
            'LADType': self.type_of_limited_access.value if self.type_of_limited_access else None,
            'Acc_RDEL': bool_to_str(self.residential),
            'Acc_FLATBD': bool_to_str(self.flat_bed),
            'Acc_TRDSHWD': bool_to_str(self.trade_show),
            'TRDSHWDType': self.trade_show_type.value if self.trade_show_type else None,
        }.items() if value is not None}


def get_quote(shipper: ShippingParty,
              consignee: ShippingParty,
              commodity: Commodity,
              shipment_specifics: ShipmentSpecifics,
              pickup_services: PickupServices,
              delivery_services: DeliveryServices
              ):

    arcbest_quote_api_endpoint = 'https://www.abfs.com/xml/aquotexml.asp'
    arcbest_api_key = os.environ.get('ARCBEST_API_KEY')
    post_body = {**shipper.as_shipper_dict(),
                 **consignee.as_consignee_dict(),
                 **commodity.as_dict(),
                 **shipment_specifics.as_dict(),
                 **pickup_services.as_dict(),
                 **delivery_services.as_dict(),
                 'ID': arcbest_api_key}

    print(f'Arcbest API request: {post_body}')
    # NB: the response is in XML!
    response = requests.post(url=arcbest_quote_api_endpoint, params={'api_key': arcbest_api_key}, data=post_body)

    if response.status_code == 200:
        # print(f'Arcbest API response: {response.text}')
        response_dict = xmltodict.parse(response.text)
        print(f'Arcbest API response dict: {pp.pprint(response_dict)}')
    else:
        print(f'Arcbest API request failed with status code: {response.status_code}')


def get_current_date() -> tuple:
    now = datetime.now()
    return (now.day, now.month, now.year)

if __name__ == '__main__':
    shipper = ShippingParty('123 Main Street', 'Dallas', 'TX', '75201', 'US',
                            'Shipper', submitting_party=True, paying_party=True)
    consignee = ShippingParty('456 Main Street', 'Tulsa', 'OK',
                              '74104', 'US', 'Consignee')
    third_party = ShippingParty('789 Main Street', 'Seattle', 'WA',
                                '98101', 'US', 'Third Party')

    commodity = Commodity(weight=100, line_number=1, shipment_class=ShipmentClasses.CLASS_150, length=48, width=48, height=48, unit_number=1, packing_type=PackageType.PKG)
    today = get_current_date()
    shipment_specifics = ShipmentSpecifics(shipDay=today[0], shipMonth=today[1], shipYear=today[2], measurement_unit=UnitsOfMeasurement.IN)
    pickup_services = PickupServices(lift_gate=True, residential=True)
    delivery_services = DeliveryServices(lift_gate=True, residential=True)

    get_quote(shipper=shipper,
              consignee=consignee,
              commodity=commodity,
              shipment_specifics=shipment_specifics,
              pickup_services=pickup_services,
              delivery_services=delivery_services)


