:: File: install.bat
:: Description: Install the required dependencies for the program.
:: NOTE:        NEED TO RUN THIS AS AN ADMIN.
:: Created at: 161222
:: Modified at:161222
:: By: Res260

@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
	pip install opencv-python
	pip install pyaudio
) else (
	echo Run the program as an admin.
)
pause
