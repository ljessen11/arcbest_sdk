import os
from datetime import datetime
from enum import Enum
import pprint
import requests
import xmltodict

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


class ShipmentClasses(Enum):
    CLASS_50 = 50
    CLASS_55 = 55
    CLASS_60 = 60
    CLASS_65 = 65
    CLASS_70 = 70
    CLASS_77_5 = 77.5
    CLASS_85 = 85
    CLASS_92_5 = 92.5
    CLASS_100 = 100
    CLASS_110 = 110
    CLASS_125 = 125
    CLASS_150 = 150
    CLASS_175 = 175
    CLASS_200 = 200
    CLASS_250 = 250
    CLASS_300 = 300
    CLASS_400 = 400
    CLASS_500 = 500


class PackageType(Enum):
    BAG = "Bag"
    BL = "Bale"
    BRL = "Barrel"
    BSK = "Basket"
    BX = "Box"
    BKT = "Bucket"
    BLKH = "Bulkhead"
    BDL = "Bundle"
    CRB = "Carboy"
    CTN = "Carton"
    CS = "Case"
    CHT = "Chest"
    CL = "Coil"
    CRT = "Crate"
    CYL = "Cylinder"
    DR = "Drum"
    FIR = "Firkin"
    HMP = "Hamper"
    HHD = "Hogshead"
    KEG = "Keg"
    PKG = "Package"
    PL = "Pail"
    PLT = "Pallet"
    PC = "Piece"
    RK = "Rack"
    REL = "Reel"
    RL = "Roll"
    SKD = "Skid"
    SLP = "Slip Sheet"
    TOTE = "Tote"
    TRK = "Trunk"
    TB = "Tube"


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


class UnitsOfMeasurement(Enum):
    FT = "FT"
    IN = "IN"
    M = "M"


class ShipmentSpecifics:
    def __init__(self, shipMonth: int, shipDay: int, shipYear: int, overall_cubic_feet: float | None = None,
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


def get_quote(shipper: ShippingParty,
              consignee: ShippingParty,
              commodity: Commodity,
              shipment_specifics: ShipmentSpecifics,
              ):

    arcbest_quote_api_endpoint = 'https://www.abfs.com/xml/aquotexml.asp'
    arcbest_api_key = os.environ.get('ARCBEST_API_KEY')
    post_body = {**shipper.as_shipper_dict(), **consignee.as_consignee_dict(), **commodity.as_dict(),
                 **shipment_specifics.as_dict(), 'ID': arcbest_api_key}

    print(f'Arcbest API request: {post_body}')
    response = requests.post(url=arcbest_quote_api_endpoint, params={'api_key': arcbest_api_key}, data=post_body)

    if response.status_code == 200:
        print(f'Arcbest API response: {response.text}')
        response_dict = xmltodict.parse(response.text)
        print(f'Arcbest API response dict: {pp.pprint(response_dict)}')
    else:
        print(f'Arcbest API request failed with status code: {response.status_code}')

    # print(f'Arcbest API key: {arcbest_api_key}')  # Press ⌘F8 to toggle the breakpoint.

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
    get_quote(shipper=shipper, consignee=consignee, commodity=commodity, shipment_specifics=shipment_specifics)


