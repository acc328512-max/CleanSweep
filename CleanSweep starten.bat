@echo off
REM Startet die CleanSweep-Oberflaeche per Doppelklick.
REM pythonw.exe = Python ohne schwarzes Konsolenfenster.
start "" "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" "%~dp0src\gui.py"
