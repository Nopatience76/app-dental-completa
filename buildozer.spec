[app]

# Título de la aplicación
title = Clínica Dental

# Nombre del paquete
package.name = clinicadental

# Dominio (reverso de tu organización)
package.domain = com.dental

# Configuración de código fuente
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json,db,sqlite3
source.exclude_exts = spec

# Versión
version = 1.0

# Requerimientos - SOLO ESPECIFICA KIVY
requirements = python3,kivy==2.3.0

# Permisos
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Configuración de Android
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25c  # IMPORTANTE: Usar 25c en lugar de 25b

# Arquitectura
android.arch = arm64-v8a

# Versión de Gradle
android.gradle_dependencies = 

# Aceptar licencias
android.accept_sdk_license = True

# Log level para debugging
log_level = 2

# Fullscreen (opcional)
fullscreen = 0

# Orientación
orientation = portrait

# Ícono (debe existir en tu proyecto)
#icon.filename = icon.png

# Paquetes a incluir
#android.add_packaging_options = --use-library

[buildozer]

# Configuración de buildozer
log_level = 2
warn_on_root = 1

# Directorio de trabajo
build_dir = ./.buildozer

# Cache para builds más rápidos
update_cache = 1
cache_dir = ./.buildozer/cache

# Directorio de bins
bin_dir = ./bin

# Tiempo de espera
# timeout = 600
