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
