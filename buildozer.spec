[app]

# Application metadata
title = Calculator Barikish
package.name = calculatorbarikish
package.domain = org.barikish

# Source code location
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,otf,kv,atlas,json

# Versioning
version = 1.0.0

# Application requirements
requirements = python3,kivy

# Build configuration
orientation = portrait
fullscreen = 0

# Android-specific settings
android.permissions =
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# Build settings
android.copy_libs = 1
android.logcat_filters = *:S python:D
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = android:Theme.Material.NoActionBar
android.debug = 1

[buildozer]
log_level = 2
warn_on_root = 1
