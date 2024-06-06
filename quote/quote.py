import os
# import pprint
import requests
import xmltodict
from enum import Enum

from utils import bool_to_str, get_current_date_as_tuple, pp
from shared_enums import PackageType, UnitsOfMeasurement, LimitedAccessOptions, ShipmentClasses

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
# pp = pprint.PrettyPrinter(indent=4)
# bool_to_str = lambda x: 'Y' if x else 'N'


class TradeshowDeliveryTypes(Enum):
    ADVANCED_WAREHOUSE = "AW"
    DIRECT_TO_TRADE_SHOW = "DTS"



class DeclaredTypes(Enum):
    NEW = 'N'
    OTHER_THAN_NEW = 'O'


class ShippingParty:
    def __init__(self,
                 street_address: str,
                 city: str,
                 state: str,
                 zip_code: str,
                 country: str,
                 name: str | None = None,
                 name_plus: str | None = None,
                 acct_number: str | None = None,
                 submitting_party: bool | None = None,
                 paying_party: bool | None = None):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip = zip_code
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
    def __init__(self, ship_month: int,
                 ship_day: int,
                 ship_year: int,
                 overall_cubic_feet: float | None = None,
                 overall_length: float | None = None,
                 overall_width: float | None = None,
                 overall_height: float | None = None,
                 measurement_unit: UnitsOfMeasurement | None = None):
        self.shipMonth = ship_month
        self.shipDay = ship_day
        self.shipYear = ship_year
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


class AdditionalServices:
    def __init__(self,
                 do_not_stack: bool | None = None,
                 arrival_notification: bool | None = None,
                 capacity_load: bool | None = None,
                 bond: bool | None = None,
                 excess_liability: bool | None = None,
                 declared_value: int | None = None,
                 declared_type: DeclaredTypes | None = None,
                 over_dimension: bool | None = None,
                 longest_side: int | None = None,
                 single_shipment: bool | None = None,
                 sort_and_segregate: bool | None = None,
                 num_to_sort_and_segregate: int | None = None,
                 truck_pack: bool | None = None,
                 truck_pack_count: int | None = None,
                 freeze_protection: bool | None = None,
                 shipper_loading: bool | None = None,
                 consignee_unloading: bool | None = None,
                 hazmat: bool | None = None,
                 pallet: bool | None = None,
                 terminal_delivery: bool | None = None,
                 terminal_pickup: bool | None = None):

        if declared_value is not None and declared_type is None:
            raise ValueError('If declared_value is provided, declared_type must be provided')

        self.do_not_stack = do_not_stack
        self.arrival_notification = arrival_notification
        self.capacity_load = capacity_load
        self.bond = bond
        self.excess_liability = excess_liability
        self.declared_value = declared_value
        self.declared_type = declared_type
        self.over_dimension = over_dimension
        self.longest_side = longest_side
        self.single_shipment = single_shipment
        self.sort_and_segregate = sort_and_segregate
        self.num_to_sort_and_segregate = num_to_sort_and_segregate
        self.truck_pack = truck_pack
        self.truck_pack_count = truck_pack_count
        self.freeze_protection = freeze_protection
        self.shipper_loading = shipper_loading
        self.consignee_unloading = consignee_unloading
        self.hazmat = hazmat
        self.pallet = pallet
        self.terminal_delivery = terminal_delivery
        self.terminal_pickup = terminal_pickup

        if self.excess_liability is not None and self.declared_value is None:
            raise ValueError('If excess liability is true, the declared value must be provided')
        if self.excess_liability is not None and self.declared_type is None:
            raise ValueError('If excess liability is true, the declared type must be provided')
        if self.sort_and_segregate is not None and self.num_to_sort_and_segregate is None:
            raise ValueError('If sort and segregate is true, '
                             'the number of packages to sort and separate must be provided')
        if self.truck_pack is not None and self.truck_pack_count is None:
            raise ValueError('If truck pack is true, the number of packages in the truck must be provided')

    def as_dict(self):
        return {key: value for key, value in {
            'Acc_NFOT': bool_to_str(self.do_not_stack),
            'Acc_ARR': bool_to_str(self.arrival_notification),
            'Acc_CAP': bool_to_str(self.capacity_load),
            'Acc_BOND': bool_to_str(self.bond),
            'Acc_ELC': bool_to_str(self.excess_liability),
            'DeclaredValue': self.declared_value,
            'DeclaredType': self.declared_type.value if self.declared_type else None,
            'Acc_OD': bool_to_str(self.over_dimension),
            'ODLongestSide': self.longest_side,
            'Acc_SS': bool_to_str(self.single_shipment),
            'Acc_SEG': bool_to_str(self.sort_and_segregate),
            'SegPieces': self.num_to_sort_and_segregate,
            'Acc_TRPACK': bool_to_str(self.truck_pack),
            'TPBoxes': self.truck_pack_count,
            'Acc_FRE': bool_to_str(self.freeze_protection),
            'Acc_SL': bool_to_str(self.shipper_loading),
            'Acc_CUL': bool_to_str(self.consignee_unloading),
            'Acc_HAZ': bool_to_str(self.hazmat),
            'Acc_PALLET': bool_to_str(self.pallet),
            'Acc_DOCKDEL': bool_to_str(self.terminal_delivery),
            'Acc_DOCKPU': bool_to_str(self.terminal_pickup),
        }.items() if value is not None}


def get_quote(shipper: ShippingParty,
              consignee: ShippingParty,
              commodity: Commodity,
              shipment_specifics: ShipmentSpecifics,
              pickup_services: PickupServices | None = None,
              delivery_services: DeliveryServices | None = None,
              additional_services: AdditionalServices | None = None
              ) -> dict | None:

    response_dict = None

    arcbest_quote_api_endpoint = 'https://www.abfs.com/xml/aquotexml.asp'
    arcbest_api_key = os.environ.get('ARCBEST_API_KEY')
    post_body = {**shipper.as_shipper_dict(),
                 **consignee.as_consignee_dict(),
                 **commodity.as_dict(),
                 **shipment_specifics.as_dict(),
                 'ID': arcbest_api_key}

    if pickup_services is not None:
        post_body.update(pickup_services.as_dict())

    if delivery_services is not None:
        post_body.update(delivery_services.as_dict())

    if additional_services is not None:
        post_body.update(additional_services.as_dict())

    print(f'Arcbest API request: {post_body}')
    # NB: the response.text is XML!
    response = requests.post(url=arcbest_quote_api_endpoint, params={'api_key': arcbest_api_key}, data=post_body)

    if response.status_code == 200:
        # print(f'Arcbest API response: {response.text}')
        response_dict = xmltodict.parse(response.text)
        print(f'Arcbest API response dict: {pp.pprint(response_dict)}')
    else:
        print(f'Arcbest API request failed with status code: {response.status_code}')

    return response_dict


if __name__ == '__main__':
    shipper = ShippingParty('123 Main Street', 'Dallas', 'TX', '75201', 'US',
                            'Shipper', submitting_party=True, paying_party=True)
    consignee = ShippingParty('456 Main Street', 'Tulsa', 'OK',
                              '74104', 'US', 'Consignee')
    third_party = ShippingParty('789 Main Street', 'Seattle', 'WA',
                                '98101', 'US', 'Third Party')

    commodity = Commodity(weight=100, line_number=1, shipment_class=ShipmentClasses.CLASS_150, length=48, width=48, height=48, unit_number=1, packing_type=PackageType.PKG)
    today = get_current_date_as_tuple()
    shipment_specifics = ShipmentSpecifics(ship_day=today[0], ship_month=today[1], ship_year=today[2], measurement_unit=UnitsOfMeasurement.IN)
    pickup_services = PickupServices(lift_gate=True, residential=True)
    delivery_services = DeliveryServices(lift_gate=True, residential=True)
    # additional_services = AdditionalServices(excess_liability=True, declared_type=DeclaredTypes.NEW, declared_value=5000, pallet=True)
    get_quote(shipper=shipper,
              consignee=consignee,
              commodity=commodity,
              shipment_specifics=shipment_specifics,
              pickup_services=pickup_services,
              delivery_services=delivery_services)


