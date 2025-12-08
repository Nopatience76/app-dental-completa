[app]
title = Clínica Dental
package.name = clinicadental
package.domain = org.dental

source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json,db

version = 1.0
requirements = python3,kivy==2.3.0,sqlite3

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Configuración optimizada
android.accept_sdk_license = True
android.api = 33
android.minapi = 21

# Usar solo una arquitectura para builds más rápidos
android.arch = arm64-v8a

# Orientación vertical
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0