from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from views.styles import Colors, FontSizes, Metrics

class SearchScreen(Screen):
    def __init__(self, db=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.build_ui()
    
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
            text='Buscar Pacientes',
            font_size=FontSizes.SUBTITLE,
            bold=True,
            size_hint=(0.9, 1)
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Campo de búsqueda
        search_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        
        self.search_input = TextInput(
            hint_text='Nombre, teléfono o email...',
            multiline=False,
            size_hint=(0.8, 1)
        )
        self.search_input.bind(on_text_validate=self.perform_search)
        
        search_btn = Button(
            text='🔍 Buscar',
            size_hint=(0.2, 1),
            background_color=Colors.PRIMARY,
            background_normal=''
        )
        search_btn.bind(on_press=self.perform_search)
        
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        layout.add_widget(search_box)
        
        # Resultados
        results_label = Label(
            text='Resultados:',
            font_size=FontSizes.BODY,
            bold=True,
            size_hint=(1, 0.05)
        )
        layout.add_widget(results_label)
        
        # Scroll para resultados
        scroll = ScrollView(size_hint=(1, 0.77))
        self.results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def perform_search(self, instance):
        if self.db and self.search_input.text:
            results = self.db.search_patients(self.search_input.text)
            self.display_results(results)
    
    def display_results(self, patients):
        self.results_layout.clear_widgets()
        
        if not patients:
            no_results = Label(
                text='No se encontraron pacientes',
                font_size=FontSizes.BODY,
                color=Colors.TEXT_LIGHT,
                size_hint_y=None,
                height=50
            )
            self.results_layout.add_widget(no_results)
            return
        
        for patient in patients:
            patient_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10)
            
            # Información principal
            main_info = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
            
            name_label = Label(
                text=patient[1],  # name
                font_size=FontSizes.BODY,
                bold=True,
                size_hint=(0.6, 1)
            )
            
            phone_label = Label(
                text=patient[2],  # phone
                font_size=FontSizes.SMALL,
                size_hint=(0.4, 1)
            )
            
            main_info.add_widget(name_label)
            main_info.add_widget(phone_label)
            
            # Información secundaria
            secondary_info = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
            
            if patient[3]:  # email
                email_label = Label(
                    text=f"Email: {patient[3]}",
                    font_size=FontSizes.SMALL,
                    size_hint=(1, 0.5)
                )
                secondary_info.add_widget(email_label)
            
            if patient[8]:  # medical_notes
                notes_label = Label(
                    text=f"Notas: {patient[8][:30]}...",
                    font_size=FontSizes.SMALL,
                    color=Colors.TEXT_LIGHT,
                    size_hint=(1, 0.5)
                )
                secondary_info.add_widget(notes_label)
            
            patient_box.add_widget(main_info)
            patient_box.add_widget(secondary_info)
            
            self.results_layout.add_widget(patient_box)