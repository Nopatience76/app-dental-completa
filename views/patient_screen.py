from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from views.styles import Colors, FontSizes, Metrics

class PatientScreen(Screen):
    def __init__(self, db=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.build_ui()
        self.load_patients()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=Metrics.PADDING, spacing=Metrics.SPACING)
        
        # Encabezado
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        back_btn = Button(
            text='←',
            font_size=FontSizes.SUBTITLE,
            size_hint=(0.1, 1),
            background_color=Colors.PRIMARY,
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        title = Label(
            text='Gestión de Pacientes',
            font_size=FontSizes.SUBTITLE,
            bold=True,
            size_hint=(0.8, 1)
        )
        
        add_btn = Button(
            text='➕',
            font_size=FontSizes.SUBTITLE,
            size_hint=(0.1, 1),
            background_color=Colors.SECONDARY,
            background_normal=''
        )
        add_btn.bind(on_press=self.show_add_patient_popup)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(add_btn)
        
        layout.add_widget(header)
        
        # Búsqueda
        search_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        
        self.search_input = TextInput(
            hint_text='Buscar paciente...',
            multiline=False,
            size_hint=(0.8, 1)
        )
        
        search_btn = Button(
            text='🔍',
            size_hint=(0.2, 1),
            background_color=Colors.PRIMARY,
            background_normal=''
        )
        search_btn.bind(on_press=self.search_patients)
        
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        layout.add_widget(search_box)
        
        # Lista de pacientes
        scroll = ScrollView(size_hint=(1, 0.82))
        self.patients_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.patients_layout.bind(minimum_height=self.patients_layout.setter('height'))
        scroll.add_widget(self.patients_layout)
        
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_patients(self):
        if self.db:
            patients = self.db.get_all_patients()
            self.display_patients(patients)
    
    def display_patients(self, patients):
        self.patients_layout.clear_widgets()
        
        for patient in patients:
            patient_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10)
            
            # Información del paciente
            info_box = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
            
            name_label = Label(
                text=patient[1],  # name
                font_size=FontSizes.BODY,
                bold=True,
                size_hint=(1, 0.5)
            )
            
            phone_label = Label(
                text=patient[2],  # phone
                font_size=FontSizes.SMALL,
                color=Colors.TEXT_LIGHT,
                size_hint=(1, 0.5)
            )
            
            info_box.add_widget(name_label)
            info_box.add_widget(phone_label)
            
            # Botones de acción
            action_box = BoxLayout(orientation='horizontal', size_hint=(0.3, 1), spacing=5)
            
            edit_btn = Button(
                text='✏️',
                font_size=FontSizes.SMALL,
                size_hint=(0.5, 1),
                background_color=Colors.PRIMARY_LIGHT,
                background_normal=''
            )
            edit_btn.bind(on_press=lambda x, p=patient: self.show_edit_patient_popup(p))
            
            delete_btn = Button(
                text='🗑️',
                font_size=FontSizes.SMALL,
                size_hint=(0.5, 1),
                background_color=Colors.ACCENT,
                background_normal=''
            )
            delete_btn.bind(on_press=lambda x, p=patient: self.delete_patient(p[0]))
            
            action_box.add_widget(edit_btn)
            action_box.add_widget(delete_btn)
            
            patient_box.add_widget(info_box)
            patient_box.add_widget(action_box)
            
            self.patients_layout.add_widget(patient_box)
    
    def search_patients(self, instance):
        if self.db and self.search_input.text:
            patients = self.db.search_patients(self.search_input.text)
            self.display_patients(patients)
        else:
            self.load_patients()
    
    def show_add_patient_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Campos del formulario
        fields = [
            ('Nombre completo:', 'text'),
            ('Teléfono:', 'text'),
            ('Email:', 'text'),
            ('Dirección:', 'text'),
            ('Fecha nacimiento:', 'text'),
            ('Tipo sangre:', 'text'),
            ('Alergias:', 'text'),
            ('Notas médicas:', 'text')
        ]
        
        self.inputs = {}
        for label, input_type in fields:
            field_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
            field_box.add_widget(Label(text=label, size_hint=(0.4, 1)))
            
            inp = TextInput(multiline=False, size_hint=(0.6, 1))
            self.inputs[label] = inp
            field_box.add_widget(inp)
            
            content.add_widget(field_box)
        
        # Botones
        button_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        
        cancel_btn = Button(text='Cancelar', background_color=Colors.DARK_GRAY)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        save_btn = Button(text='Guardar', background_color=Colors.SECONDARY)
        save_btn.bind(on_press=self.save_patient)
        
        button_box.add_widget(cancel_btn)
        button_box.add_widget(save_btn)
        
        content.add_widget(button_box)
        
        popup = Popup(
            title='Nuevo Paciente',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        self.current_popup = popup
        popup.open()
    
    def save_patient(self, instance):
        if self.db:
            patient_id = self.db.add_patient(
                name=self.inputs['Nombre completo:'].text,
                phone=self.inputs['Teléfono:'].text,
                email=self.inputs['Email:'].text,
                address=self.inputs['Dirección:'].text,
                birth_date=self.inputs['Fecha nacimiento:'].text,
                blood_type=self.inputs['Tipo sangre:'].text,
                allergies=self.inputs['Alergias:'].text,
                medical_notes=self.inputs['Notas médicas:'].text
            )
            
            if patient_id:
                self.current_popup.dismiss()
                self.load_patients()
    
    def show_edit_patient_popup(self, patient):
        # Similar a show_add_patient_popup pero prellenando datos
        pass
    
    def delete_patient(self, patient_id):
        if self.db:
            if self.db.delete_patient(patient_id):
                self.load_patients()