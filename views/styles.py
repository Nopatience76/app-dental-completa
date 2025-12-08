from kivy.utils import get_color_from_hex

class Colors:
    # Paleta dental profesional
    PRIMARY = get_color_from_hex('#4A90E2')  # Azul profesional
    PRIMARY_LIGHT = get_color_from_hex('#7BB4F0')
    SECONDARY = get_color_from_hex('#50C878')  # Verde salud
    SECONDARY_LIGHT = get_color_from_hex('#85E3A1')
    ACCENT = get_color_from_hex('#FF6B6B')  # Rojo para alertas
    SUCCESS = get_color_from_hex('#4CAF50')  # Verde éxito
    WARNING = get_color_from_hex('#FFC107')  # Amarillo advertencia
    WHITE = get_color_from_hex('#FFFFFF')
    LIGHT_GRAY = get_color_from_hex('#F5F5F5')
    MEDIUM_GRAY = get_color_from_hex('#E0E0E0')
    DARK_GRAY = get_color_from_hex('#424242')
    TEXT_DARK = get_color_from_hex('#212121')
    TEXT_LIGHT = get_color_from_hex('#757575')
    
    # Colores de estado de citas
    SCHEDULED = get_color_from_hex('#4A90E2')  # Programada
    CONFIRMED = get_color_from_hex('#50C878')  # Confirmada
    COMPLETED = get_color_from_hex('#9C27B0')  # Completada
    CANCELLED = get_color_from_hex('#FF6B6B')  # Cancelada
    
class FontSizes:
    TITLE = 24
    SUBTITLE = 18
    BODY = 16
    SMALL = 14
    TINY = 12

class Metrics:
    PADDING = 20
    SPACING = 10
    BORDER_RADIUS = 10