[app]

title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ── FIXED: removed opencv-python-headless, removed duplicate kivymd ──
requirements = python3,kivy,kivymd,pyjnius,opencv,pillow

orientation = portrait
fullscreen = 0

# ── FIXED: uncommented and set correct API levels ──
android.api = 33
android.minapi = 21

# ── FIXED: Added all required permissions ──
android.permissions = CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ── FIXED: Enable androidx (needed for modern camera APIs) ──
android.enable_androidx = True

osx.python_version = 3
osx.kivy_version = 1.9.1

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1