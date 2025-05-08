@echo off
echo Building KC-Riff for Windows...

REM Create output directory
if not exist build mkdir build

REM Build the shared library DLL
echo Building shared library...
go build -buildmode=c-shared -o build/kcriff.dll kcriff_shared_lib.go

if %ERRORLEVEL% NEQ 0 (
    echo Failed to build shared library
    exit /b %ERRORLEVEL%
)

REM Build the minimal server
echo Building minimal server...
go build -o build/kcriff-server.exe minimal_server.go

if %ERRORLEVEL% NEQ 0 (
    echo Failed to build minimal server
    exit /b %ERRORLEVEL%
)

REM Copy Python integration files
echo Copying Python files...
copy kcriff_integration.py build\
copy run_desktop_app.py build\
mkdir build\pyqt_interface
copy pyqt_interface\*.py build\pyqt_interface\

echo Build completed successfully.
echo Output is in the build directory.