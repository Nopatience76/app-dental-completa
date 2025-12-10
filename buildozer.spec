[app]
title = Clínica Dental
package.name = clinicadental
package.domain = com.dental

source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json,db
version = 1.0
requirements = python3,kivy==2.3.0

android.permissions = INTERNET

# CONFIGURACIÓN CORREGIDA
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25c  # ¡IMPORTANTE! Usar 25c

# Solo una arquitectura para simplificar
android.arch = arm64-v8a

# Aceptar licencias automáticamente
android.accept_sdk_license = True

# Directorio de salida explícito
android.bin_dir = bin

orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
