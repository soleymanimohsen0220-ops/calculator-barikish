[app]

# (str) Title of your application
title = Calculator Barikish

# (str) Package name
package.name = calculatorbarikish

# (str) Package domain (needed for android/ios packaging)
package.domain = org.barikish

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,otf

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) fullscreen mode on the android app
fullscreen = 1

# (list) Permissions
android.permissions =

# (int) Target Android API
android.api = 34

# (int) Minimum API required (Android 5.0 = 21)
android.minapi = 21

# (bool) Accept Android SDK license automatically
android.accept_sdk_license = True

# (bool) Skip checking for Android SDK updates
android.skip_update = True

# (str) Path to Android SDK (uses GitHub Actions pre-installed SDK)
android.sdk_path = /usr/local/lib/android/sdk

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Copy the libraries instead of making a link (faster startup)
android.copy_libs = 1

# (str) Logcat filter
android.logcat_filters = *:S python:D

# (int) Specifies the number of make jobs to run in parallel
make.jobs = 4

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = android:Theme.Material.NoActionBar

# (bool) Skip android update
# android.skip_update = False

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Application versioning (method 2)
# version.regex = __version__ = ['\"](.*)['\"]\n# version.filename = %(source.dir)s/main.py

# (list) List of service to declare
# services = Name:Name, ...

# (str) Custom additions to the buildozer command line
# android.add_compile_options = ...

# (str) p4a source directory
# p4a.source_dir = ...

# (str) Directory for p4a fork
# p4a.branch = master

# (str) Git URL for python-for-android
# p4a.git_url = https://github.com/kivy/python-for-android

# (str) Bootstrap to use
# p4a.bootstrap = sdl2

# (str) Local recipes directory
# p4a.local_recipes =

# (str) Build directory
# p4a.build_dir = ./.buildozer/android/platform/python-for-android

# (str) Path to a custom whitelist file
# android.whitelist =

# (bool) Show build warnings
android.debug = 1

# (bool) Force services to start on boot
# android.wakelock = False

# (str) The Android NDK version to use
android.ndk = 25b

# (bool) Use the PyPI package instead of git
# p4a.fork = kivy

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warnings
warn_on_root = 1

# (str) Path to the buildozer config file
# buildozer.config =

# (str) Path to the buildozer state file
# state = .buildozer/state

# (str) Path to the buildozer log directory
# log_dir = logs
