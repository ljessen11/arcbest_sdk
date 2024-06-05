class ShippingParty:
    def __init__(self, name: str | None,
                 name_plus: str | None,
                 street_address: str | None,
                 city: str | None,
                 state: str | None,
                 zip_code: str | None,
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
        self.zip = zip_code
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
