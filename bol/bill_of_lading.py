import os
import pprint
import re
from datetime import date
from enum import Enum
from typing import List

import requests
import xmltodict
from email_validator import validate_email, EmailNotValidError

from bol.shipping_party import ShippingParty
from commodity import Commodity
from shared_enums import UnitsOfMeasurement, LimitedAccessOptions, PackageType, ShipmentClasses
from utils import bool_to_str

pp = pprint.PrettyPrinter(indent=4)


class RequestorTypes(Enum):
    CONSIGNEE = 1
    SHIPPER = 2
    THIRD_PARTY = 3


class PayTerms(Enum):
    PREPAID = 'P'
    COLLECT = 'C'


class ShipmentSpecifics:
    def __init__(self,
                 ship_date: date | None = None,
                 other_carrier: str | None = None,
                 pro_number: int | None = None,
                 pro_number_check_digit: int | None = None,
                 auto_assign_pro_number: bool | None = None,
                 quote_id: str | None = None,
                 instructions: str | None = None,
                 total_cube: float | None = None,
                 cube_unit_of_measurement: UnitsOfMeasurement | None = None):
        self.shipDate = ship_date
        self.formatted_ship_date = ship_date.strftime("%m/%d/%y")
        self.other_carrier = other_carrier
        self.pro_number = pro_number
        self.pro_number_check_digit = pro_number_check_digit
        self.auto_assign_pro_number = auto_assign_pro_number
        self.quote_id = quote_id
        self.instructions = instructions
        self.total_cube = total_cube
        self.cube_unit_of_measurement = cube_unit_of_measurement

    def as_dict(self):
        return {key: value for key, value in {
                'ShipDate'     : self.formatted_ship_date,
                'OtherCarrier' : self.other_carrier,
                'ProNumber'    : self.pro_number,
                'CheckDigit'   : self.pro_number_check_digit,
                'ProAutoAssign': self.auto_assign_pro_number,
                'QuoteID'      : self.quote_id,
                'Instructions' : self.instructions,
                'TotalCube'    : self.total_cube,
                'LWHType'      : self.cube_unit_of_measurement.value if self.cube_unit_of_measurement else None,
        }.items() if value is not None}


class DeliveryDateTypes(Enum):
    BY = 'by'
    ON = 'on'
    BETWEEN = 'between'


class DeliveryTimeTypes(Enum):
    BY = 'by'
    BETWEEN = 'between'


def is_valid_time(time_str: str) -> bool:
    # Define the regex pattern to match the format HH:MM
    pattern = r"^(09|1[0-7]):(00|15|30|45)$"

    # Check if the input string matches the pattern
    if re.match(pattern, time_str):
        return True
    else:
        return False


class TimeCriticalShipmentSpecifics:
    def __init__(self,
                 is_time_critical: bool | None = True,
                 delivery_date_type: DeliveryDateTypes | None = None,
                 delivery_date_min: date | None = None,
                 delivery_date_max: date | None = None,
                 delivery_time_type: DeliveryTimeTypes | None = None,
                 delivery_time: str | None = None,
                 delivery_time_min: str | None = None,
                 delivery_time_max: str | None = None):

        if delivery_time_min is None:
            raise ValueError('DeliveryTimeMin is required to be in the format for all delivery time fields:'
                             ' hh:MM in military format (24-hour) in fifteen-minute increments'
                             ' between 9:00 and 17:00')
        if delivery_time_max is None:
            raise ValueError('DeliveryTimeMax is required to be in the format for all delivery time fields:'
                             ' hh:MM in military format (24-hour) in fifteen-minute increments'
                             ' between 9:00 and 17:00')

        self.isTimeCritical = is_time_critical
        self.delivery_date_type = delivery_date_type
        self.delivery_date_min = delivery_date_min
        self.delivery_date_max = delivery_date_max
        self.delivery_time_type = delivery_time_type
        self.delivery_time = delivery_time
        self.delivery_time_min = delivery_time_min
        self.delivery_time_max = delivery_time_max

    def as_dict(self):
        return {key: value for key, value in {
                'TimeKeeper'      : bool_to_str(self.isTimeCritical),
                'DeliveryDateType': self.delivery_date_type.value if self.delivery_date_type else None,
                'DeliveryDateMin' : self.delivery_date_min.strftime("%m/%d/%y") if self.delivery_date_min else None,
                'DeliveryDateMax' : self.delivery_date_max.strftime("%m/%d/%y") if self.delivery_date_max else None,
                'DeliveryTimeType': self.delivery_time_type.value if self.delivery_time_type else None,
                'DeliveryTime'    : self.delivery_time,
                'DeliveryTimeMin' : self.delivery_time_min,
                'DeliveryTimeMax' : self.delivery_time_max,
        }.items() if value is not None}


class ReferenceNumbers:
    # the po_index is an index between 1 and 10 and is added as a suffix to the keys for the submitted data
    def __init__(self,
                 bol_number: str | None = None,
                 po_index: int | None = None,
                 actual_po_number: str | None = None,
                 po_pieces: int | None = None,
                 po_weight: float | None = None,
                 po_department: str | None = None,
                 customer_reference_number: str | None = None):
        if actual_po_number is not None and po_index is not None and (po_index == 0 or po_index > 10):
            raise ValueError('If PO_number is provided, an index must be providedbetween 1 and 10')
        self.bol_number = bol_number
        self.po_number = po_index
        self.actual_po_number = actual_po_number
        self.po_pieces = po_pieces
        self.po_weight = po_weight
        self.po_department = po_department
        self.customer_reference_number = customer_reference_number

    def as_dict(self):
        return {key: value for key, value in {
                'Bol'                      : self.bol_number,
                f'PO{self.po_number}'      : self.actual_po_number,
                f'POPiece{self.po_number}' : self.po_pieces,
                f'POWeight{self.po_number}': self.po_weight,
                f'PODept{self.po_number}'  : self.po_department,
                f'CRN{self.po_number}'     : self.customer_reference_number
        }.items() if value is not None}


class CopyConfirmation:
    def __init__(self, bol_to_shipper: bool | None = None,
                 bol_to_consignee: bool | None = None,
                 bol_to_third_party: bool | None = None,
                 bol_to_emails: list[str] | None = None,
                 shipping_lables_to_shipper: bool | None = None,
                 shipping_labels_to_consignee: bool | None = None,
                 shipping_labels_to_third_party: bool | None = None,
                 shipping_labels_to_emails: list[str] | None = None):

        self.validate_emails()

        self.bol_to_shipper = bol_to_shipper
        self.bol_to_consignee = bol_to_consignee
        self.bol_to_third_party = bol_to_third_party
        self.bol_to_emails = bol_to_emails
        self.shipping_lables_to_shipper = shipping_lables_to_shipper
        self.shipping_labels_to_consignee = shipping_labels_to_consignee
        self.shipping_labels_to_third_party = shipping_labels_to_third_party
        self.shipping_labels_to_emails = shipping_labels_to_emails

    def validate_emails(self):
        invalid_emails = []

        if self.bol_to_emails:
            for email in self.bol_to_emails:
                if not self.is_valid_email(email):
                    invalid_emails.append(email)

        if self.shipping_labels_to_emails:
            for email in self.shipping_labels_to_emails:
                if not self.is_valid_email(email):
                    invalid_emails.append(email)

        if invalid_emails:
            raise ValueError(f"Invalid email addresses: {invalid_emails}")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def as_dict(self):
        return {key: value for key, value in {
                'BolCopyShip'     : bool_to_str(self.bol_to_shipper),
                'BolCopyCons'     : bool_to_str(self.bol_to_consignee),
                'BolCopyTPB'      : bool_to_str(self.bol_to_third_party),
                'BolCopyAdd'      : ','.join(self.bol_to_emails) if self.bol_to_emails else None,
                'BolCopyLabelShip': bool_to_str(self.shipping_lables_to_shipper),
                'BolCopyLabelCons': bool_to_str(self.shipping_labels_to_consignee),
                'BolCopyLabelTPB' : bool_to_str(self.shipping_labels_to_third_party),
                'BolCopyLabelAdd' : ','.join(self.shipping_labels_to_emails) if self.shipping_labels_to_emails else None
        }.items() if value is not None}


class PickupOptions:
    def __init__(self,
                 liftgate: bool | None = None,
                 inside: bool | None = None,
                 limited_access: bool | None = None,
                 limited_access_type: LimitedAccessOptions | None = None,
                 residential_pickup: bool | None = None):
        self.liftgate = liftgate
        self.inside = inside
        self.limited_access = limited_access
        self.limited_access_type = limited_access_type
        self.residential_pickup = residential_pickup

    def as_dict(self):
        return {key: value for key, value in {
                'Acc_GRD_PU': bool_to_str(self.liftgate),
                'Acc_IPU'   : bool_to_str(self.inside),
                'Acc_LAP'   : bool_to_str(self.limited_access),
                'LAPType'   : self.limited_access_type.value if self.limited_access_type else None,
                'Acc_RPU'   : bool_to_str(self.residential_pickup),
        }.items() if value is not None}


class DeliveryOptions:
    def __init__(self,
                 construction_site: bool | None = None,
                 on_date: bool | None = None,
                 liftgate: bool | None = None,
                 inside: bool | None = None,
                 limited_access: bool | None = None,
                 limited_access_type: LimitedAccessOptions | None = None,
                 residential_delivery: bool | None = None,
                 flatbed: bool | None = None,
                 ):
        self.construction_site = construction_site
        self.on_date = on_date
        self.liftgate = liftgate
        self.inside = inside
        self.limited_access = limited_access
        self.limited_access_type = limited_access_type
        self.residential_delivery = residential_delivery
        self.flatbed = flatbed

    def as_dict(self):
        return {key: value for key, value in {
                'Acc_CSD'    : bool_to_str(self.construction_site),
                'Acc_DELON'  : bool_to_str(self.on_date),
                'Acc_GRD_DEL': bool_to_str(self.liftgate),
                'Acc_IDEL'   : bool_to_str(self.inside),
                'Acc_LAD'    : bool_to_str(self.limited_access),
                'LADType'    : self.limited_access_type.value if self.limited_access_type else None,
                'Acc_RDEL'   : bool_to_str(self.residential_delivery),
                'Acc_FLATBD' : bool_to_str(self.flatbed),
        }.items() if value is not None}


class AdditionalServices:
    def __init__(self,
                 arrival_notification: bool | None = None,
                 capacity_load: bool | None = None,
                 customs_or_in_bond_freight: bool | None = None,
                 excess_liablity_coverage: bool | None = None,
                 declared_value: float | None = None,
                 over_dimension: bool | None = None,
                 longest_dimension: float | None = None,
                 single_shipment: bool | None = None,
                 sort_and_segregate: bool | None = None,
                 number_of_pieces_to_sort_and_segregate: int | None = None,
                 truck_pack_shipment: bool | None = None,
                 number_truck_pack_boxes: int | None = None,
                 secure_shipment_divider: bool | None = None,
                 freeze_protection: bool | None = None
                 ):

        if (number_of_pieces_to_sort_and_segregate is not None
                and number_of_pieces_to_sort_and_segregate is not None
                and number_of_pieces_to_sort_and_segregate < 1):
            raise ValueError('Number of pieces to sort and segregate must be greater than 0')

        if (number_truck_pack_boxes is not None
                and number_truck_pack_boxes is not None
                and number_truck_pack_boxes < 1):
            raise ValueError('Number of truck pack boxes must be greater than 0')

        self.arrival_notification = arrival_notification
        self.capacity_load = capacity_load
        self.customs_or_in_bond_freight = customs_or_in_bond_freight
        self.excess_liability_coverage = excess_liablity_coverage
        self.declared_value = declared_value
        self.over_dimension = over_dimension
        self.longest_dimension = longest_dimension
        self.single_shipment = single_shipment
        self.sort_and_segregate = sort_and_segregate
        self.number_of_pieces_to_sort_and_segregate = number_of_pieces_to_sort_and_segregate
        self.truck_pack_shipment = truck_pack_shipment
        self.number_truck_pack_boxes = number_truck_pack_boxes
        self.secure_shipment_divider = secure_shipment_divider
        self.freeze_protection = freeze_protection

    def as_dict(self):
        return {key: value for key, value in {
                'Acc_AR'       : self.arrival_notification,
                'Acc_CAP'      : self.capacity_load,
                'Acc_BOND'     : self.customs_or_in_bond_freight,
                'Acc_ELC'      : self.excess_liability_coverage,
                'DeclaredValue': self.declared_value,
                'Acc_OD'       : self.over_dimension,
                'ODLongestSide': self.longest_dimension,
                'Acc_SS'       : self.single_shipment,
                'Acc_SEG'      : self.sort_and_segregate,
                'SegPieces'    : self.number_of_pieces_to_sort_and_segregate,
                'Acc_TRPACK'   : self.truck_pack_shipment,
                'TPBoxes'      : self.number_truck_pack_boxes,
                'Acc_BLKH'     : self.secure_shipment_divider,
                'Acc_FRE'      : self.freeze_protection
        }.items() if value is not None}


class FileFormats(Enum):
    A = "A"  # Adobe acrobat
    H = "H"  # HTML


class LabelFormats(Enum):
    """
    6 per page - Compatible with Avery Shipping Labels 5164, 5264, 5524, 8164, 8254, 8464, 48464, 55164, 58164
    4 per page - Compatible with Avery Shipping Labels 5168, 6878
    2 per page - Compatible with Avery Shipping Labels 5126, 5526, 8126, 15516, 18126
    1 per page - Compatible with Avery Shipping Labels 5165, 5265, 5353, 8165, 8255, 8264, 8665, 18665
    Zebra - Compatible with 4" x 6" Zebra Labels
    """
    SIX_PER_PAGE = "6"
    FOUR_PER_PAGE = "4"
    TWO_PER_PAGE = "2"
    ONE_PER_PAGE = "1"
    ZEBRA = "Z"


class DocLabelInfo:
    def __init__(self,
                 file_format: FileFormats | None = FileFormats.A,
                 using_inject_printer: bool | None = None,
                 label_format: LabelFormats | None = None,
                 number_shipping_labels_to_create: int | None = None,
                 start_position_avery_5264: int | None = None,
                 number_pro_labels: int | None = None,
                 starting_page_avery_5160: int | None = None
                 ):
        self.file_format = file_format
        self.using_inject_printer = using_inject_printer
        self.label_format = label_format
        self.number_shipping_labels_to_create = number_shipping_labels_to_create
        self.start_position_avery_5264 = start_position_avery_5264
        self.number_pro_labels = number_pro_labels
        self.starting_page_avery_5160 = starting_page_avery_5160

    def as_dict(self):
        return {key: value for key, value in {
                'FileFormat'            : self.file_format.value if self.file_format else None,
                'InkJetPrinter'         : bool_to_str(self.using_inject_printer),
                'LabelFormat'           : self.label_format.value if self.label_format else None,
                'LableNum'              : self.number_shipping_labels_to_create,
                'StartPositionAvery5264': self.start_position_avery_5264,
                'ProLabelNum'           : self.number_pro_labels,
                'ProLabelStart'         : self.starting_page_avery_5160
        }.items() if value is not None}


class Requestor:
    def __init__(self,
                 payment_terms: PayTerms,
                 requestor_type: RequestorTypes | None = RequestorTypes.SHIPPER,
                 name: str | None = None,
                 email: str | None = None,
                 phone: str | None = None,
                 phone_ext: str | None = None,
                 fax: str | None = None):

        self.payment_terms = payment_terms
        self.requestor_type = requestor_type
        self.name = name
        self.email = email
        self.phone = phone
        self.phone_ext = phone_ext
        self.fax = fax

    def as_dict(self):
        return {key: value for key, value in {
                'PayTerms'         : self.payment_terms.value,
                'RequestorType'    : self.requestor_type.value if self.requestor_type else None,
                'RequestorName'    : self.name,
                'RequestorEmail'   : self.email,
                'RequestorPhone'   : self.phone,
                'RequestorPhoneExt': self.phone_ext,
                'RequestorFax'     : self.fax
        }.items() if value is not None}


def get_bol(
        requestor: Requestor,
        shipping_party: ShippingParty,
        consignee: ShippingParty,
        commodity_lines: List[Commodity],
        shipment_specifics: ShipmentSpecifics,
        app_id: str | None = None,
        testing: bool = True,
        time_critical_specifics: TimeCriticalShipmentSpecifics | None = None,
        reference_numbers: List[ReferenceNumbers] | None = None,
        copy_confirmation: CopyConfirmation | None = None,
        pickup_options: PickupOptions | None = None,
        delivery_options: DeliveryOptions | None = None,
        additional_services: AdditionalServices | None = None,
        doc_label_info: DocLabelInfo | None = None,
        arcbest_bol_endpoint: str = 'https://www.abfs.com/xml/bolxml.asp',
        arcbest_api_key: str = os.environ.get('ARCBEST_API_KEY'),
) -> dict | None:

    response_dict = None

    post_body = {
            'testing': bool_to_str(testing),
            **requestor.as_dict(),
            **shipping_party.as_shipper_dict(),
            **consignee.as_consignees_dict()
    }

    if app_id is not None:
        post_body.update({'AppID': app_id})

    for commodity_line in commodity_lines:
        post_body.update(commodity_line.as_dict())

    if shipment_specifics is not None:
        post_body.update(shipment_specifics.as_dict())
    if time_critical_specifics is not None:
        post_body.update(time_critical_specifics.as_dict())

    if reference_numbers is not None:
        for ref_num_line in reference_numbers:
            post_body.update(ref_num_line.as_dict())

    if copy_confirmation is not None:
        post_body.update(copy_confirmation.as_dict())
    if pickup_options is not None:
        post_body.update(pickup_options.as_dict())
    if delivery_options is not None:
        post_body.update(delivery_options.as_dict())
    if additional_services is not None:
        post_body.update(additional_services.as_dict())
    if doc_label_info is not None:
        post_body.update(doc_label_info.as_dict())

    print(f"ArcBest BOL post data: {post_body}")
    # NB: the response.text is XML!
    response = requests.post(url=arcbest_bol_endpoint, params={'api_key': arcbest_api_key}, data=post_body)

    if response.status_code == 200:
        print(f"ArcBest BOL response: {response.text}")
        response_dict = xmltodict.parse(response.text)
        print(f"ArcBest BOL response dict: {pp.pprint(response_dict)}")
    else:
        print(f"ArcBest BOL request failed with status code: {response.status_code}")

    return response_dict


"""
https://www.abfs.com/xml/bolxml.asp?
DL=2&
ID=BQNED065&
Test=Y&
# Requestor 
RequesterType=1&PayTerms=P&RequesterName=JOHN+BLACK&RequesterPhone=5555555555&

Shipping Party / shipper
ShipName=XYZ+Corp&ShipAddress=123+MAIN&ShipCity=Dyer&ShipState=AR&ShipZip=72935&

Shipping Part / consignee
ConsName=ABC+Corp&ConsAddress=321+Elm&ConsCity=LAWRENCE&ConsState=KS&ConsZip=66044&

Commodity / line 1
HN1=100&HT1=PLT&WT1=1000&CL1=65&NMFC1=123456&SUB1=78&CB1=321&Desc1=MISC+AUTO+PARTS&

ShipmentSpecifics
ShipDate=05/31/2024&

ReferenceNumbers
Bol=123BOL45&PO1=1231235435&POPiece1=100&POWeight1=1000&CRN1=1234567890&Acc_ARR=Y&

DocLabelInfo
FileFormat=A
"""

if __name__ == '__main__':
    requestor = Requestor(
            payment_terms=PayTerms.PREPAID,
            requestor_type=RequestorTypes.CONSIGNEE,
            name='John Black',
            email='WqkzQ@example.com',
            phone='5555555555',
    )
    shipper = ShippingParty(
            name='XYZ Corp',
            street_address='123 Main St',
            city='Dyer',
            state='AR',
            zip_code='72935',
    )
    consignee = ShippingParty(
            name='ABC Corp',
            street_address='321 Elm St',
            city='Lawrence',
            state='KS',
            zip_code='66044',
    )
    commodity = Commodity(
            line_number=1,
            number_of_handling_units=100,
            height=PackageType.PLT,
            total_weight=1000,
            shipment_class=ShipmentClasses.CLASS_65,
            nmfc_number=123456,
            nmfc_sub_number=78,
            cube=321,
            description='Misc. Auto Parts',
    )
    ref_nums = ReferenceNumbers(
            bol_number='123BOL45',
            po_index=1,
            actual_po_number='1231235435',
            po_pieces=100,
            po_weight=1000,
            customer_reference_number='1234567890',
    )

    doc_label = DocLabelInfo(file_format=FileFormats.A)

    shipment_specs = ShipmentSpecifics(ship_date=date(2024, 5, 31))

    bol = get_bol(
            requestor=requestor,
            shipping_party=shipper,
            consignee=consignee,
            commodity_lines=[commodity],
            shipment_specifics=shipment_specs,
            doc_label_info=doc_label,
            reference_numbers=[ref_nums]
    )

    print(bol)
