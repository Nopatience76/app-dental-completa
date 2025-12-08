class Patient:
    def __init__(self, id, name, phone, email="", address="", birth_date="", blood_type="", allergies="", medical_notes=""):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.blood_type = blood_type
        self.allergies = allergies
        self.medical_notes = medical_notes
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'birth_date': self.birth_date,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'medical_notes': self.medical_notes
        }