from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from datetime import datetime
from views.styles import Colors, FontSizes, Metrics

class AppointmentScreen(Screen):
    def __init__(self, db=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.build_ui()
        self.load_appointments()
    
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
            text='Gestión de Citas',
            font_size=FontSizes.SUBTITLE,
            bold=True,
            size_hint=(0.8, 1)
        )
        
        today_btn = Button(
            text='Hoy',
            size_hint=(0.1, 1),
            background_color=Colors.SECONDARY,
            background_normal=''
        )
        today_btn.bind(on_press=self.show_today_appointments)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(today_btn)
        
        layout.add_widget(header)
        
        # Filtro de fecha
        filter_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        
        self.date_input = TextInput(
            hint_text='AAAA-MM-DD',
            text=datetime.now().strftime('%Y-%m-%d'),
            multiline=False,
            size_hint=(0.7, 1)
        )
        
        filter_btn = Button(
            text='Filtrar',
            size_hint=(0.3, 1),
            background_color=Colors.PRIMARY,
            background_normal=''
        )
        filter_btn.bind(on_press=self.filter_appointments)
        
        filter_box.add_widget(self.date_input)
        filter_box.add_widget(filter_btn)
        
        layout.add_widget(filter_box)
        
        # Lista de citas
        scroll = ScrollView(size_hint=(1, 0.82))
        self.appointments_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.appointments_layout.bind(minimum_height=self.appointments_layout.setter('height'))
        scroll.add_widget(self.appointments_layout)
        
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_appointments(self):
        if self.db:
            appointments = self.db.get_all_appointments()
            self.display_appointments(appointments)
    
    def display_appointments(self, appointments):
        self.appointments_layout.clear_widgets()
        
        for appt in appointments:
            appt_box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10)
            
            # Encabezado de la cita
            header_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
            
            date_label = Label(
                text=f"{appt[2]} {appt[3]}",  # date + time
                font_size=FontSizes.SMALL,
                bold=True,
                size_hint=(0.4, 1)
            )
            
            status_label = Label(
                text=appt[5],  # status
                font_size=FontSizes.SMALL,
                color=self.get_status_color(appt[5]),
                size_hint=(0.3, 1)
            )
            
            cost_label = Label(
                text=f"${appt[7]:.2f}",  # cost
                font_size=FontSizes.SMALL,
                size_hint=(0.3, 1)
            )
            
            header_box.add_widget(date_label)
            header_box.add_widget(status_label)
            header_box.add_widget(cost_label)
            
            # Detalles de la cita
            details_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
            
            patient_label = Label(
                text=appt[10],  # patient_name
                font_size=FontSizes.BODY,
                size_hint=(0.5, 1)
            )
            
            procedure_label = Label(
                text=appt[4],  # procedure_type
                font_size=FontSizes.SMALL,
                size_hint=(0.5, 1)
            )
            
            details_box.add_widget(patient_label)
            details_box.add_widget(procedure_label)
            
            # Botones de acción
            action_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=5)
            
            complete_btn = Button(
                text='✓',
                font_size=FontSizes.SMALL,
                size_hint=(0.25, 1),
                background_color=Colors.SUCCESS,
                background_normal=''
            )
            complete_btn.bind(on_press=lambda x, a=appt: self.update_status(a[0], 'Completada'))
            
            cancel_btn = Button(
                text='✗',
                font_size=FontSizes.SMALL,
                size_hint=(0.25, 1),
                background_color=Colors.ACCENT,
                background_normal=''
            )
            cancel_btn.bind(on_press=lambda x, a=appt: self.update_status(a[0], 'Cancelada'))
            
            edit_btn = Button(
                text='✏️',
                font_size=FontSizes.SMALL,
                size_hint=(0.25, 1),
                background_color=Colors.PRIMARY_LIGHT,
                background_normal=''
            )
            
            delete_btn = Button(
                text='🗑️',
                font_size=FontSizes.SMALL,
                size_hint=(0.25, 1),
                background_color=Colors.DARK_GRAY,
                background_normal=''
            )
            delete_btn.bind(on_press=lambda x, a=appt: self.delete_appointment(a[0]))
            
            action_box.add_widget(complete_btn)
            action_box.add_widget(cancel_btn)
            action_box.add_widget(edit_btn)
            action_box.add_widget(delete_btn)
            
            appt_box.add_widget(header_box)
            appt_box.add_widget(details_box)
            appt_box.add_widget(action_box)
            
            self.appointments_layout.add_widget(appt_box)
    
    def get_status_color(self, status):
        from views.styles import Colors
        if status == 'Programada':
            return Colors.SCHEDULED
        elif status == 'Confirmada':
            return Colors.CONFIRMED
        elif status == 'Completada':
            return Colors.COMPLETED
        elif status == 'Cancelada':
            return Colors.CANCELLED
        else:
            return Colors.TEXT_DARK
    
    def filter_appointments(self, instance):
        if self.db and self.date_input.text:
            appointments = self.db.get_appointments_by_date(self.date_input.text)
            self.display_appointments(appointments)
    
    def show_today_appointments(self, instance):
        self.date_input.text = datetime.now().strftime('%Y-%m-%d')
        self.filter_appointments(instance)
    
    def update_status(self, appointment_id, status):
        if self.db:
            if self.db.update_appointment_status(appointment_id, status):
                self.load_appointments()
    
    def delete_appointment(self, appointment_id):
        if self.db:
            if self.db.delete_appointment(appointment_id):
                self.load_appointments()