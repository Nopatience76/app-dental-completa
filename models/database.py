import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('dental_clinic.db', check_same_thread=False)
        self.create_tables()
        self.insert_sample_data()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabla de pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                birth_date TEXT,
                blood_type TEXT,
                allergies TEXT,
                medical_notes TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                procedure_type TEXT NOT NULL,
                status TEXT DEFAULT 'Programada',
                notes TEXT,
                cost REAL DEFAULT 0.0,
                paid REAL DEFAULT 0.0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        # Tabla de tratamientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                treatment_date TEXT NOT NULL,
                treatment_type TEXT NOT NULL,
                description TEXT,
                cost REAL DEFAULT 0.0,
                next_appointment TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        self.conn.commit()
    
    def insert_sample_data(self):
        cursor = self.conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM patients")
        if cursor.fetchone()[0] == 0:
            # Insertar pacientes de ejemplo
            sample_patients = [
                ('María González', '555-1234', 'maria@email.com', 'Calle Principal 123', '1985-03-15', 'O+', 'Penicilina', 'Control anual'),
                ('Carlos López', '555-5678', 'carlos@email.com', 'Avenida Central 456', '1990-07-22', 'A-', 'Ninguna', 'Ortodoncia'),
                ('Ana Martínez', '555-9012', 'ana@email.com', 'Plaza Mayor 789', '1978-11-30', 'B+', 'Aspirina', 'Implantes'),
                ('Juan Pérez', '555-3456', 'juan@email.com', 'Boulevard Norte 321', '1995-05-10', 'AB-', 'Latex', 'Limpieza dental'),
                ('Laura Sánchez', '555-7890', 'laura@email.com', 'Calle Sur 654', '1988-09-05', 'O-', 'Ninguna', 'Blanqueamiento')
            ]
            
            cursor.executemany('''
                INSERT INTO patients (name, phone, email, address, birth_date, blood_type, allergies, medical_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_patients)
            
            # Insertar citas de ejemplo
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT INTO appointments (patient_id, date, time, procedure_type, status, notes, cost, paid)
                VALUES (1, ?, '09:00', 'Limpieza dental', 'Programada', 'Primera visita', 500.00, 0.0)
            ''', (tomorrow,))
            
            cursor.execute('''
                INSERT INTO appointments (patient_id, date, time, procedure_type, status, notes, cost, paid)
                VALUES (2, ?, '11:30', 'Ortodoncia', 'Programada', 'Ajuste de brackets', 800.00, 400.0)
            ''', (tomorrow,))
            
            self.conn.commit()
    
    # ===== MÉTODOS PARA PACIENTES =====
    
    def add_patient(self, name, phone, email="", address="", birth_date="", blood_type="", allergies="", medical_notes=""):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO patients (name, phone, email, address, birth_date, blood_type, allergies, medical_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, phone, email, address, birth_date, blood_type, allergies, medical_notes))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar paciente: {e}")
            return None
    
    def get_all_patients(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM patients ORDER BY name')
        return cursor.fetchall()
    
    def search_patients(self, search_term):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM patients 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return cursor.fetchall()
    
    def get_patient_by_id(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        return cursor.fetchone()
    
    def update_patient(self, patient_id, name, phone, email="", address="", birth_date="", blood_type="", allergies="", medical_notes=""):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE patients 
                SET name=?, phone=?, email=?, address=?, birth_date=?, blood_type=?, allergies=?, medical_notes=?
                WHERE id=?
            ''', (name, phone, email, address, birth_date, blood_type, allergies, medical_notes, patient_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            return False
    
    def delete_patient(self, patient_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar paciente: {e}")
            return False
    
    # ===== MÉTODOS PARA CITAS =====
    
    def add_appointment(self, patient_id, date, time, procedure_type, status="Programada", notes="", cost=0.0, paid=0.0):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO appointments (patient_id, date, time, procedure_type, status, notes, cost, paid)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, date, time, procedure_type, status, notes, cost, paid))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar cita: {e}")
            return None
    
    def get_appointments_by_date(self, date):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name 
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.id 
            WHERE a.date = ? 
            ORDER BY a.time
        ''', (date,))
        return cursor.fetchall()
    
    def get_all_appointments(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT a.*, p.name 
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.id 
            ORDER BY a.date DESC, a.time DESC
        ''')
        return cursor.fetchall()
    
    def update_appointment_status(self, appointment_id, status):
        cursor = self.conn.cursor()
        try:
            cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', (status, appointment_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar estado de cita: {e}")
            return False
    
    def delete_appointment(self, appointment_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar cita: {e}")
            return False
    
    # ===== MÉTODOS PARA TRATAMIENTOS =====
    
    def add_treatment(self, patient_id, treatment_date, treatment_type, description="", cost=0.0, next_appointment=""):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO treatments (patient_id, treatment_date, treatment_type, description, cost, next_appointment)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, treatment_date, treatment_type, description, cost, next_appointment))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar tratamiento: {e}")
            return None
    
    def get_treatments_by_patient(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM treatments 
            WHERE patient_id = ? 
            ORDER BY treatment_date DESC
        ''', (patient_id,))
        return cursor.fetchall()
    
    # ===== ESTADÍSTICAS =====
    
    def get_stats(self):
        cursor = self.conn.cursor()
        
        # Total pacientes
        cursor.execute('SELECT COUNT(*) FROM patients')
        total_patients = cursor.fetchone()[0]
        
        # Citas hoy
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM appointments WHERE date = ?', (today,))
        appointments_today = cursor.fetchone()[0]
        
        # Citas pendientes
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Programada'")
        pending_appointments = cursor.fetchone()[0]
        
        # Ingresos del mes
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute("SELECT SUM(paid) FROM appointments WHERE strftime('%Y-%m', date) = ?", (current_month,))
        monthly_income = cursor.fetchone()[0] or 0
        
        return {
            'total_patients': total_patients,
            'appointments_today': appointments_today,
            'pending_appointments': pending_appointments,
            'monthly_income': monthly_income
        }