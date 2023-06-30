pyinstaller --noconfirm --onefile --console --icon %cd%\icon.ico %cd%\scrb.py
del "scrb.spec"
rmdir /s /q build
move %cd%\dist\scrb.exe %cd%
rmdir /s /q dist