from enum import Enum
from utils import bool_to_str
from shared_enums import PackageType, ShipmentClasses


class HazMatCompatibilities(Enum):
    CLASS_1_4 = ["B", "C", "D", "E", "F", "G", "S"]
    CLASS_1_5 = ["D"]
    CLASS_1_6 = ["N"]


class HazMatZones(Enum):
    CLASS_2_3 = ["A", "B", "C", "D"]
    CLASS_6_1 = ["A", "B"]


class Commodity:
    def __init__(self,
                 line_number: int,
                 number_of_handling_units: int | None,
                 handling_unit_type: PackageType | None,
                 length: float | None,
                 width: float | None,
                 height: float | None,
                 number_of_packages: int | None,
                 package_type: PackageType | None,
                 total_weight: float | None,
                 shipment_class: ShipmentClasses | None,
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
                 hazmat_product_name: str | None,
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
        self.shipment_class = shipment_class
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
        self.hazmat_product_name = hazmat_product_name
        self.hazmat_sub_hazard1 = hazmat_sub_hazard1
        self.hazmat_sub_hazard2 = hazmat_sub_hazard2
        self.hazmat_packaging_group = hazmat_packaging_group
        self.hazmat_additional_info = hazmat_additional_info
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
            f'HN{self.line_number}': self.number_of_handling_units,
            f'HT{self.line_number}': self.handling_unit_type.value if self.handling_unit_type else None,
            f'FrtLng{self.line_number}': self.length,
            f'FrtWdth{self.line_number}': self.width,
            f'FrtHght{self.line_number}': self.height,
            f'PN{self.line_number}': self.number_of_packages,
            f'PT{self.line_number}': self.package_type.value if self.package_type else None,
            f'WT{self.line_number}': self.total_weight,
            f'CL{self.line_number}': self.shipment_class.value if self.shipment_class else None,
            f'NMFC{self.line_number}': self.nmfc_number,
            f'SUB{self.line_number}': self.nmfc_sub_number,
            f'CB{self.line_number}': self.cube,
            f'Desc{self.line_number}': self.description,
            f'HZ{self.line_number}': bool_to_str(self.hazmat),
            f'HZCL{self.line_number}': self.hazmat_class,
            f'HZUN{self.line_number}': self.un_ua_number,
            f'HZContact{self.line_number}': self.hazmat_contact_name,
            f'HZPH{self.line_number}': self.hazmat_contact_phone,
            f'HZExt{self.line_number}': self.hazmat_contact_phone_ext,
            f'HZPropName{self.line_number}': self.hazmat_proper_shipping_name,
            f'HZTechName{self.line_number}': self.hazmat_technical_name,
            f'HZProdName{self.line_number}': self.hazmat_product_name,
            f'HZSubHaz1{self.line_number}': self.hazmat_sub_hazard1,
            f'HZSubHaz2{self.line_number}': self.hazmat_sub_hazard2,
            f'HZPackGrp{self.line_number}': self.hazmat_packaging_group,
            f'HZAddlInfo{self.line_number}': self.hazmat_additional_info,
            f'HZDOTEx{self.line_number}': self.hazmat_dot_exemption,
            f'HZSpecPerm{self.line_number}': self.hazmat_special_permit,
            f'HZRQ{self.line_number}': bool_to_str(self.hazmat_reportable_quantity),
            f'LtdQty{self.line_number}': bool_to_str(self.hazmat_limited_quantity),
            f'HZPIH{self.line_number}': bool_to_str(self.hazmat_poison_inhalation_hazard),
            f'HZBulk{self.line_number}': bool_to_str(self.hazmat_bulk_package),
            f'HZMarine{self.line_number}': bool_to_str(self.hazmat_marine_pollutant),
            f'HZResidue{self.line_number}': bool_to_str(self.hazmat_residue_last_contained),
            f'Compat{self.line_number}': self.hazmat_compatibility.value if self.hazmat_compatibility else None,
            f'HZZone{self.line_number}': self.hazmat_material_zone.value if self.hazmat_material_zone else None,
            f'HZFlashPointTemp{self.line_number}': self.hazmat_flash_point_temp,
            f'HZNetExplosiveMass{self.line_number}': self.hazmat_net_explosive_mass,
        }.items() if value is not None}

