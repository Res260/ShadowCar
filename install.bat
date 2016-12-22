REM File: install.bat
REM Description: Install the required dependencies for the program.
REM NOTE:        NEED TO RUN THIS AS AN ADMIN.
REM Created at: 161222
REM Modified at:161222
REM By: Res260

@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
	pip install opencv-python
	pip install pyaudio
) else (
	echo Run the program as an admin.
)
