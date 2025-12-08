class Appointment:
    def __init__(self, id, patient_id, date, time, procedure_type, status="Programada", notes="", cost=0.0, paid=0.0, patient_name=""):
        self.id = id
        self.patient_id = patient_id
        self.date = date
        self.time = time
        self.procedure_type = procedure_type
        self.status = status
        self.notes = notes
        self.cost = cost
        self.paid = paid
        self.patient_name = patient_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'date': self.date,
            'time': self.time,
            'procedure_type': self.procedure_type,
            'status': self.status,
            'notes': self.notes,
            'cost': self.cost,
            'paid': self.paid,
            'patient_name': self.patient_name
        }