@echo off
cd /d "%~dp0"

echo Uruchamianie DARK8...
echo (Jesli pojawi sie blad, okno pozostanie otwarte)

python dark8_gui.py
if %errorlevel% neq 0 (
    echo.
    echo Wystapil blad podczas uruchamiania DARK8.
    echo Sprawdz, czy Python jest zainstalowany i czy dark8_gui.py istnieje.
    echo.
    pause
)
pause
