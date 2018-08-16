@echo off
set DIR=%~dp0
set PYTHONPATH=%DIR%lib;%DIR%plugins;%PYTHONPATH%
start python "%DIR%launcher.py"


