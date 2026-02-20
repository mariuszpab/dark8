@echo off
title DARK8 – Interaktywna Konsola

REM --- Wymuszenie UTF-8 w konsoli Windows ---
chcp 65001 >nul

REM --- Przejście do katalogu projektu ---
cd /d %~dp0

:loop
cls
echo ============================================
echo        DARK8 MARK01 – INTERAKTYWNA KONSOLE
echo ============================================
echo.
set /p usercmd="Wpisz polecenie: "

if "%usercmd%"=="wyjdz" exit

REM --- Uruchom interpreter poleceń DARK8 ---
py -3.10 dark8_interpreter.py "%usercmd%"

echo.
pause
goto loop
