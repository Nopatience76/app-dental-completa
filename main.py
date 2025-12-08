from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from views.main_screen import MainScreen
from views.patient_screen import PatientScreen
from views.appointment_screen import AppointmentScreen
from views.search_screen import SearchScreen
from models.database import Database

class DentalApp(App):
    def build(self):
        # Configurar tamaño de ventana para móvil
        Window.size = (360, 640)
        
        # Inicializar base de datos
        self.db = Database()
        
        # Configurar ScreenManager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', db=self.db))
        sm.add_widget(PatientScreen(name='patients', db=self.db))
        sm.add_widget(AppointmentScreen(name='appointments', db=self.db))
        sm.add_widget(SearchScreen(name='search', db=self.db))
        
        return sm

if __name__ == '__main__':
    DentalApp().run()