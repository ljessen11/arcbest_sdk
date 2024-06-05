



class CommodityLine:
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

