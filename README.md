# GuardiánClima ITBA

Aplicación de consola en Python que consulta el clima en tiempo real, guarda historial personal, muestra estadísticas globales y genera consejos de vestimenta usando inteligencia artificial (Google Gemini).

## Requisitos

- Python 3.10+
- Cuenta en [OpenWeatherMap](https://openweathermap.org/api) (API gratuita)
- Cuenta en [Google AI Studio](https://aistudio.google.com/) para la API de Gemini

## Instalación

```bash
pip install requests python-dotenv google-generativeai
```

## Configuración

1. Copiá el archivo de ejemplo y completá tus claves:

```bash
cp .env.example .env
```

2. Editá `.env` con tus claves reales:

```
OPENWEATHERMAP_API_KEY=tu_clave_openweathermap
GEMINI_API_KEY=tu_clave_gemini
```

## Ejecución

```bash
python main.py
```

## Estructura del proyecto

```
guardianclimaITBA/
├── main.py                 # Punto de entrada y menús
├── auth.py                 # Registro e inicio de sesión
├── clima.py                # Consulta a la API de OpenWeatherMap
├── ia.py                   # Consejos de vestimenta con Google Gemini
├── historial.py            # Lectura/escritura/estadísticas del historial
├── utils.py                # Helpers compartidos (pantalla, banner, inputs)
├── .env                    # Variables de entorno (no subir a git)
├── .env.example            # Plantilla de variables de entorno
├── usuarios_simulados.csv  # Base de datos de usuarios
└── historial_global.csv    # Historial de consultas climáticas
```

## Funcionalidades

| Función | Descripción |
|---|---|
| Registro | Crea usuario con validación estricta de contraseña |
| Login | Autenticación por CSV |
| Clima | Temperatura, sensación térmica, humedad, viento y condición |
| Historial | Filtra consultas por usuario y ciudad, ordenadas por fecha |
| Estadísticas | Ciudad más consultada, total de consultas, temperatura promedio |
| Consejo IA | Sugerencia de vestimenta personalizada según el clima actual |

## Validación de contraseña

Las contraseñas deben cumplir **todos** estos requisitos:
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número
- Al menos un carácter especial (`!@#$%^&*...`)

## Notas

- Los archivos CSV se crean automáticamente si no existen.
- El consejo de IA usa el clima de la última consulta realizada en la sesión actual.
- La API de OpenWeatherMap retorna el viento en m/s; la app lo convierte a km/h.
