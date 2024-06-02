import re
from enum import Enum
from datetime import date
from enumerations import PackageType, HazMatCompatibilities, HazMatZones, UnitsOfMeasurement, LimitedAccessOptions
from email_validator import validate_email, EmailNotValidError

bool_to_str = lambda x: 'Y' if x else 'N'

class RequestorTypes(Enum):
    CONSIGNEE = 1
    SHIPPER = 2
    THIRD_PARTY = 3


class PayTerms(Enum):
    PREPAID = 'P'
    COLLECT = 'C'


class Requestor:
    def __init__(self, name: str | None,
                 email: str | None,
                 phone: str | None,
                 phone_ext: str | None,
                 fax: str | None):
        self.name = name
        self.email = email
        self.phone = phone
        self.phone_ext = phone_ext
        self.fax = fax

    def as_dict(self):
        return {key: value for key, value in {
            'RequestorName': self.name,
            'RequestorEmail': self.email,
            'RequestorPhone': self.phone,
            'RequestorPhoneExt': self.phone_ext,
            'RequestorFax': self.fax
        }.items() if value is not None}


class ShippingParty:
    def __init__(self, name: str | None,
                 name_plus: str | None,
                 street_address: str | None,
                 city: str | None,
                 state: str | None,
                 zip: str | None,
                 country: str | None,
                 phone: str | None,
                 phone_ext: str | None,
                 fax: str | None,
                 email: str | None):
        self.name = name
        self.name_plus = name_plus
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.phone = phone
        self.phone_ext = phone_ext
        self.fax = fax
        self.email = email

    def as_shipper_dict(self):
        return {key: value for key, value in {
            'ShipName': self.name,
            'ShipNamePlus': self.name_plus,
            'ShipAddr': self.street_address,
            'ShipCity': self.city,
            'ShipState': self.state,
            'ShipZip': self.zip,
            'ShipCountry': self.country,
            'ShipPhone': self.phone,
            'ShipPhoneExt': self.phone_ext,
            'ShipFax': self.fax,
            'ShipEmail': self.email,
        }.items() if value is not None}

    def as_consignees_dict(self):
        return {key: value for key, value in {
            'ConsName': self.name,
            'ConsNamePlus': self.name_plus,
            'ConsAddr': self.street_address,
            'ConsCity': self.city,
            'ConsState': self.state,
            'ConsZip': self.zip,
            'ConsCountry': self.country,
            'ConsPhone': self.phone,
            'ConsPhoneExt': self.phone_ext,
            'ConsFax': self.fax,
            'ConsEmail': self.email,
        }.items() if value is not None}

    def as_third_party_dict(self):
        return {key: value for key, value in {
            'TPBName': self.name,
            'TPBNamePlus': self.name_plus,
            'TPBAddr': self.street_address,
            'TPBCity': self.city,
            'TPBState': self.state,
            'TPBZip': self.zip,
            'TPBCountry': self.country,
            'TPBPhone': self.phone,
            'TPBPhoneExt': self.phone_ext,
            'TPBFax': self.fax,
            'TPBEmail': self.email,
        }.items() if value is not None}


class CommodityLine():
    def __init__(self,
                 line_number: int,
                 number_of_handling_units: int | None,
                 handling_unit_type: PackageType | None,
                 length: float | None,
                 width:float | None,
                 height: float | None,
                 number_of_packages: int | None,
                 package_type: PackageType | None,
                 total_weight: float | None,
                 commodity_class: int | None,
                 nmfc_number: int | None,
                 nmfc_sub_number: int | None,
                 cube: float | None,
                 description: str | None,
                 hazmat: bool | None,
                 hazmat_class: int | None,
                 un_ua_number: int | None,
                 hazmat_contact_name: str | None,
                 hazmat_contact_phone: str | None,
                 hazmat_contact_phone_ext: str | None,
                 hazmat_proper_shipping_name: str | None,
                 hazmat_technical_name: str | None,
                 hazmat_sub_hazard1: str | None,
                 hazmat_sub_hazard2: str | None,
                 hazmat_packaging_group: str | None,
                 hazmat_additional_info: str | None,
                 hazmat_dot_exemption: str | None,
                 hazmat_special_permit: str | None,
                 hazmat_reportable_quantity: bool | None,
                 hazmat_limited_quantity: bool | None,
                 hazmat_poison_inhalation_hazard: bool | None,
                 hazmat_bulk_package: bool | None,
                 hazmat_marine_pollutant: bool | None,
                 hazmat_residue_last_contained: bool | None,
                 hazmat_compatibility: HazMatCompatibilities | None,
                 hazmat_material_zone: HazMatZones | None,
                 hazmat_flash_point_temp: float | None,
                 hazmat_net_explosive_mass: float | None):

        self.line_number = line_number
        self.number_of_handling_units = number_of_handling_units
        self.handling_unit_type = handling_unit_type
        self.length = length
        self.width = width
        self.height = height
        self.number_of_packages = number_of_packages
        self.package_type = package_type
        self.total_weight = total_weight
        self.commodity_class = commodity_class
        self.nmfc_number = nmfc_number
        self.nmfc_sub_number = nmfc_sub_number
        self.cube = cube
        self.description = description
        self.hazmat = hazmat
        self.hazmat_class = hazmat_class
        self.un_ua_number = un_ua_number
        self.hazmat_contact_name = hazmat_contact_name
        self.hazmat_contact_phone = hazmat_contact_phone
        self.hazmat_contact_phone_ext = hazmat_contact_phone_ext
        self.hazmat_proper_shipping_name = hazmat_proper_shipping_name
        self.hazmat_technical_name = hazmat_technical_name
        self.hazmat_sub_hazard1 = hazmat_sub_hazard1
        self.hazmat_sub_hazard2 = hazmat_sub_hazard2
        self.hazmat_packaging_group = hazmat_packaging_group
        self.additional_info = hazmat_additional_info
        self.hazmat_dot_exemption = hazmat_dot_exemption
        self.hazmat_special_permit = hazmat_special_permit
        self.hazmat_reportable_quantity = hazmat_reportable_quantity
        self.hazmat_limited_quantity = hazmat_limited_quantity
        self.hazmat_poison_inhalation_hazard = hazmat_poison_inhalation_hazard
        self.hazmat_bulk_package = hazmat_bulk_package
        self.hazmat_marine_pollutant = hazmat_marine_pollutant
        self.hazmat_residue_last_contained = hazmat_residue_last_contained
        self.hazmat_compatibility = hazmat_compatibility
        self.hazmat_material_zone = hazmat_material_zone
        self.hazmat_flash_point_temp = hazmat_flash_point_temp
        self.hazmat_net_explosive_mass = hazmat_net_explosive_mass

    def as_dict(self):
        return {key: value for key, value in {
            'line_number': self.line_number,
            'number_of_handling_units': self.number_of_handling_units,
            'handling_unit_type': self.handling_unit_type.value if self.handling_unit_type else None,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'number_of_packages': self.number_of_packages,
            'package_type': self.package_type.value if self.package_type else None,
            'total_weight': self.total_weight,
            'commodity_class': self.commodity_class,
            'nmfc_number': self.nmfc_number,
            'nmfc_sub_number': self.nmfc_sub_number,
            'cube': self.cube,
            'description': self.description,
            'hazmat': bool_to_str(self.hazmat),
            'hazmat_class': self.hazmat_class,
            'un_ua_number': self.un_ua_number,
            'hazmat_contact_name': self.hazmat_contact_name,
            'hazmat_contact_phone': self.hazmat_contact_phone,
            'hazmat_contact_phone_ext': self.hazmat_contact_phone_ext,
            'hazmat_proper_shipping_name': self.hazmat_proper_shipping_name,
            'hazmat_technical_name': self.hazmat_technical_name,
            'hazmat_sub_hazard1': self.hazmat_sub_hazard1,
            'hazmat_sub_hazard2': self.hazmat_sub_hazard2,
            'hazmat_packaging_group': self.hazmat_packaging_group,
            'additional_info': self.hazmat_additional_info,
            'hazmat_dot_exemption': self.hazmat_dot_exemption,
            'hazmat_special_permit': self.hazmat_special_permit,
            'hazmat_reportable_quantity': bool_to_str(self.hazmat_reportable_quantity),
            'hazmat_limited_quantity': bool_to_str(self.hazmat_limited_quantity),
            'hazmat_poison_inhalation_hazard': bool_to_str(self.hazmat_poison_inhalation_hazard),
            'hazmat_bulk_package': bool_to_str(self.hazmat_bulk_package),
            'hazmat_marine_pollutant': bool_to_str(self.hazmat_marine_pollutant),
            'hazmat_residue_last_contained': bool_to_str(self.hazmat_residue_last_contained),
            'hazmat_compatibility': self.hazmat_compatibility.value if self.hazmat_compatibility else None,
            'hazmat_material_zone': self.hazmat_material_zone.value if self.hazmat_material_zone else None,
            'hazmat_flash_point_temp': self.hazmat_flash_point_temp,
            'hazmat_net_explosive_mass': self.hazmat_net_explosive_mass,
        }.items() if value is not None}


class ShipmentSpecifics:
    def __init__(self,
                 shipDate: date | None = None,
                 other_carrier: str | None = None,
                 pro_number: int | None = None,
                 pro_number_check_digit: int | None = None,
                 auto_assign_pro_number: bool | None= None,
                 quote_id: str | None = None,
                 instructions: str | None = None,
                 total_cube: float | None = None,
                 cube_unit_of_measurement: UnitsOfMeasurement | None = None):


        self.shipDate = shipDate
        self.formatted_ship_date = shipDate.strftime("%m/%d/%y")
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
            'ShipDate': self.formatted_ship_date,
            'OtherCarrier': self.other_carrier,
            'ProNumber': self.pro_number,
            'CheckDigit': self.pro_number_check_digit,
            'ProAutoAssign': self.auto_assign_pro_number,
            'QuoteID': self.quote_id,
            'Instructions': self.instructions,
            'TotalCube': self.total_cube,
            'LWHType': self.cube_unit_of_measurement.value if self.cube_unit_of_measurement else None,
        }.items() if value is not None}

class DeliveryDateTypes(Enum):
    BY: 'by'
    ON: 'on'
    BETWEEN: 'between'

class DeliveryTimeTypes(Enum):
    BY: 'by'
    BETWEEN: 'between'


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
                 isTimeCritical: bool | None = True,
                 DeliveryDateType: DeliveryDateTypes | None = None,
                 DeliveryDateMin: date | None = None,
                 DeliveryDateMax: date | None = None,
                 DeliveryTimeType: DeliveryTimeTypes | None = None,
                 DeliveryTime: str | None = None,
                 DeliveryTimeMin: str | None = None,
                 DeliveryTimeMax: str | None = None):

        if DeliveryTimeMin is None:
            raise ValueError('DeliveryTimeMin is required to be in the format for all delivery time fields:'
                             ' hh:MM in military format (24-hour) in fifteen-minute increments'
                             ' between 9:00 and 17:00')
        if DeliveryTimeMax is None:
            raise ValueError('DeliveryTimeMax is required to be in the format for all delivery time fields:'
                             ' hh:MM in military format (24-hour) in fifteen-minute increments'
                             ' between 9:00 and 17:00')

        self.isTimeCritical = isTimeCritical
        self.DeliveryDateType = DeliveryDateType
        self.DeliveryDateMin = DeliveryDateMin
        self.DeliveryDateMax = DeliveryDateMax
        self.DeliveryTimeType = DeliveryTimeType
        self.DeliveryTime = DeliveryTime
        self.DeliveryTimeMin = DeliveryTimeMin
        self.DeliveryTimeMax = DeliveryTimeMax

    def as_dict(self):
        return {key: value for key, value in {
            'TimeKeeper': bool_to_str(self.isTimeCritical),
            'DeliveryDateType': self.DeliveryDateType.value if self.DeliveryDateType else None,
            'DeliveryDateMin': self.DeliveryDateMin.strftime("%m/%d/%y") if self.DeliveryDateMin else None,
            'DeliveryDateMax': self.DeliveryDateMax.strftime("%m/%d/%y") if self.DeliveryDateMax else None,
            'DeliveryTimeType': self.DeliveryTimeType.value if self.DeliveryTimeType else None,
            'DeliveryTime': self.DeliveryTime,
            'DeliveryTimeMin': self.DeliveryTimeMin,
            'DeliveryTimeMax': self.DeliveryTimeMax,
        }.items() if value is not None}

class ReferenceNumbers():
    def __init__(self,
                 bol_number: str | None = None,
                 PO_number: int | None = None,
                 actual_po_number: str | None = None,
                 PO_pieces: int | None = None,
                 PO_weight: float | None = None,
                 PO_department: str | None = None,
                 customer_reference_number: str | None = None):

        if PO_number is not None and (PO_number == 0 or PO_number > 10):
            raise ValueError('If PO_number is provided, it must be between 1 and 10')
        self.bol_number = bol_number
        self.PO_number = PO_number
        self.actual_po_number = actual_po_number
        self.PO_pieces = PO_pieces
        self.PO_weight = PO_weight
        self.PO_department = PO_department
        self.customer_reference_number = customer_reference_number

    def as_dict(self):
        return {key: value for key, value in {
            'Bol': self.bol_number,
            f'PO{self.PO_number}': self.actual_po_number,
            f'POPiece{self.PO_number}': self.PO_pieces,
            f'POWeight{self.PO_number}': self.PO_weight,
            f'PODept{self.PO_number}': self.PO_department,
            f'CRN{self.PO_number}': self.customer_reference_number
        }.items() if value is not None}


class CopyConfirmation:
    def __init__(self, bol_to_shipper: bool | None = None,
                 bol_to_consignee: bool | None = None,
                 bol_to_third_party: bool | None = None,
                 bol_to_emails: [str] | None = None,
                 shipping_lables_to_shipper: bool | None = None,
                 shipping_labels_to_consignee: bool | None = None,
                 shipping_labels_to_third_party: bool | None = None,
                 shipping_labels_to_emails: [str] | None = None):

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
            'BolCopyShip': bool_to_str(self.bol_to_shipper),
            'BolCopyCons': bool_to_str(self.bol_to_consignee),
            'BolCopyTPB': bool_to_str(self.bol_to_third_party),
            'BolCopyAdd': ','.join(self.bol_to_emails) if self.bol_to_emails else None,
            'BolCopyLabelShip': bool_to_str(self.shipping_lables_to_shipper),
            'BolCopyLabelCons': bool_to_str(self.shipping_labels_to_consignee),
            'BolCopyLabelTPB': bool_to_str(self.shipping_labels_to_third_party),
            'BolCopyLabelAdd': ','.join(self.shipping_labels_to_emails) if self.shipping_labels_to_emails else None
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
            'Acc_IPU': bool_to_str(self.inside),
            'Acc_LAP': bool_to_str(self.limited_access),
            'LAPType': self.limited_access_type.value if self.limited_access_type else None,
            'Acc_RPU': bool_to_str(self.residential_pickup),
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
            'Acc_CSD': bool_to_str(self.construction_site),
            'Acc_DELON': bool_to_str(self.on_date),
            'Acc_GRD_DEL': bool_to_str(self.liftgate),
            'Acc_IDEL': bool_to_str(self.inside),
            'Acc_LAD': bool_to_str(self.limited_access),
            'LADType': self.limited_access_type.value if self.limited_access_type else None,
            'Acc_RDEL': bool_to_str(self.residential_delivery),
            'Acc_FLATBD': bool_to_str(self.flatbed),
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
            'Acc_AR': self.arrival_notification,
            'Acc_CAP': self.capacity_load,
            'Acc_BOND': self.customs_or_in_bond_freight,
            'Acc_ELC': self.excess_liability_coverage,
            'DeclaredValue': self.declared_value,
            'Acc_OD': self.over_dimension,
            'ODLongestSide': self.longest_dimension,
            'Acc_SS': self.single_shipment,
            'Acc_SEG': self.sort_and_segregate,
            'SegPieces': self.number_of_pieces_to_sort_and_segregate,
            'Acc_TRPACK': self.truck_pack_shipment,
            'TPBoxes': self.number_truck_pack_boxes,
            'Acc_BLKH': self.secure_shipment_divider,
            'Acc_FRE': self.freeze_protection
        }.items() if value is not None}


class FileFormats(Enum):
    A = "A" # Adobe acrobat
    H = "H" # HTML


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
            'FileFormat': self.file_format.value if self.file_format else None,
            'InkJetPrinter': bool_to_str(self.using_inject_printer),
            'LabelFormat': self.label_format.value if self.label_format else None,
            'LableNum': self.number_shipping_labels_to_create,
            'StartPositionAvery5264': self.start_position_avery_5264,
            'ProLabelNum': self.number_pro_labels,
            'ProLabelStart': self.starting_page_avery_5160
        }.items() if value is not None}
