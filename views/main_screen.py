from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from datetime import datetime
from views.styles import Colors, FontSizes, Metrics

class MainScreen(Screen):
    def __init__(self, db=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.build_ui()
        self.update_stats()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=Metrics.PADDING, spacing=Metrics.SPACING)
        
        # Título
        title = Label(
            text='Clínica Dental',
            font_size=FontSizes.TITLE,
            bold=True,
            color=Colors.TEXT_DARK,
            size_hint=(1, 0.1)
        )
        layout.add_widget(title)
        
        # Tarjetas de estadísticas
        stats_container = GridLayout(cols=2, spacing=Metrics.SPACING, size_hint=(1, 0.3))
        
        self.patients_card = self.create_stat_card('👥', 'Pacientes', '0')
        self.appointments_card = self.create_stat_card('📅', 'Citas Hoy', '0')
        self.pending_card = self.create_stat_card('⏰', 'Pendientes', '0')
        self.income_card = self.create_stat_card('💰', 'Ingresos', '$0')
        
        stats_container.add_widget(self.patients_card)
        stats_container.add_widget(self.appointments_card)
        stats_container.add_widget(self.pending_card)
        stats_container.add_widget(self.income_card)
        
        layout.add_widget(stats_container)
        
        # Botones de navegación
        nav_container = GridLayout(cols=2, spacing=Metrics.SPACING, size_hint=(1, 0.4))
        
        buttons = [
            ('👥 Pacientes', self.go_to_patients),
            ('📅 Citas', self.go_to_appointments),
            ('🔍 Buscar', self.go_to_search),
            ('➕ Nueva Cita', self.add_appointment),
            ('📊 Reportes', self.show_reports),
            ('⚙️ Configuración', self.show_settings)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                font_size=FontSizes.BODY,
                background_color=Colors.PRIMARY,
                background_normal='',
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda instance, cb=callback: cb())
            nav_container.add_widget(btn)
        
        layout.add_widget(nav_container)
        
        # Próximas citas
        appointments_label = Label(
            text='Próximas Citas',
            font_size=FontSizes.SUBTITLE,
            bold=True,
            color=Colors.TEXT_DARK,
            size_hint=(1, 0.05)
        )
        layout.add_widget(appointments_label)
        
        # Scroll para citas
        scroll = ScrollView(size_hint=(1, 0.3))
        self.appointments_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.appointments_layout.bind(minimum_height=self.appointments_layout.setter('height'))
        scroll.add_widget(self.appointments_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def create_stat_card(self, icon, title, value):
        card = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        with card.canvas.before:
            Color(*Colors.LIGHT_GRAY)
            card.rect = Rectangle(size=card.size, pos=card.pos)
        
        card.bind(size=self.update_rect, pos=self.update_rect)
        
        icon_label = Label(
            text=icon,
            font_size=30,
            size_hint=(1, 0.4)
        )
        
        title_label = Label(
            text=title,
            font_size=FontSizes.SMALL,
            color=Colors.TEXT_LIGHT,
            size_hint=(1, 0.3)
        )
        
        value_label = Label(
            text=value,
            font_size=FontSizes.SUBTITLE,
            bold=True,
            color=Colors.TEXT_DARK,
            size_hint=(1, 0.3)
        )
        
        card.add_widget(icon_label)
        card.add_widget(title_label)
        card.add_widget(value_label)
        
        return card
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def update_stats(self):
        if self.db:
            stats = self.db.get_stats()
            
            self.patients_card.children[0].text = f"👥\n{stats['total_patients']}"
            self.appointments_card.children[0].text = f"📅\n{stats['appointments_today']}"
            self.pending_card.children[0].text = f"⏰\n{stats['pending_appointments']}"
            self.income_card.children[0].text = f"💰\n${stats['monthly_income']:.2f}"
            
            # Actualizar próximas citas
            today = datetime.now().strftime('%Y-%m-%d')
            appointments = self.db.get_appointments_by_date(today)
            
            self.appointments_layout.clear_widgets()
            
            for appt in appointments[:5]:  # Mostrar solo 5
                appt_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                
                time_label = Label(
                    text=appt[3],  # time
                    font_size=FontSizes.SMALL,
                    size_hint=(0.2, 1)
                )
                
                name_label = Label(
                    text=appt[10],  # patient_name
                    font_size=FontSizes.SMALL,
                    size_hint=(0.5, 1)
                )
                
                procedure_label = Label(
                    text=appt[4],  # procedure_type
                    font_size=FontSizes.SMALL,
                    size_hint=(0.3, 1)
                )
                
                appt_box.add_widget(time_label)
                appt_box.add_widget(name_label)
                appt_box.add_widget(procedure_label)
                
                self.appointments_layout.add_widget(appt_box)
    
    def go_to_patients(self):
        self.manager.current = 'patients'
    
    def go_to_appointments(self):
        self.manager.current = 'appointments'
    
    def go_to_search(self):
        self.manager.current = 'search'
    
    def add_appointment(self):
        # Aquí iría la lógica para agregar una nueva cita
        print("Agregar nueva cita")
    
    def show_reports(self):
        print("Mostrar reportes")
    
    def show_settings(self):
        print("Mostrar configuración")
    
    def on_enter(self):
        self.update_stats()