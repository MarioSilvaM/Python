@echo off
:: Script para ejecutar un archivo Python pasando el nombre del programa como parámetro

:: Verificar si se pasó el nombre del script Python como argumento
if "%~1"=="" (
    echo No se proporciono el nombre del script Python.
    goto :EOF
)

:: Obtener la ruta del directorio padre
set "PARENT_DIR=%~dp0.."

:: Verificar si el archivo existe en la carpeta padre
set "PYTHON_SCRIPT=%PARENT_DIR%\%~1"
if exist "%PYTHON_SCRIPT%" (
    goto :RUN_PYTHON
)

:: Verificar si el archivo existe en un subdirectorio de la carpeta padre
set "SUBDIR_SCRIPT=%PARENT_DIR%\BIN\%~1"
if exist "%SUBDIR_SCRIPT%" (
    set "PYTHON_SCRIPT=%SUBDIR_SCRIPT%"
    goto :RUN_PYTHON
)

echo El archivo %~1 no existe en la carpeta padre ni en el subdirectorio.
goto :EOF

:RUN_PYTHON
:: Ejecutar el script Python con la ruta proporcionada y pasar argumentos adicionales
C:/ProgramData/anaconda3/python.exe "%PYTHON_SCRIPT%" %*
