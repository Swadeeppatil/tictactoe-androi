[app]

# (str) Title of your application
title = Tic Tac Toe Pro

# (str) Package name
package.name = tictactoepro

# (str) Package domain (needed for android/ios packaging)
package.domain = org.swade

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3,wav

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,numpy

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,VIBRATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android archs to build for
android.archs = arm64-v8a

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) p4a branch to use
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
