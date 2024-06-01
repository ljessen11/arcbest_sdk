from enum import Enum
from datetime import date
from enumerations import PackageType, HazMatCompatibilities, HazMatZones, UnitsOfMeasurement

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
    def __init__(self, shipDate: date | None = None,
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

