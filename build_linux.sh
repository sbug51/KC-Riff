#!/bin/bash
echo "Building KC-Riff for Linux..."

# Create output directory
mkdir -p build

# Build the shared library
echo "Building shared library..."
go build -buildmode=c-shared -o build/libkcriff.so kcriff_shared_lib.go

if [ $? -ne 0 ]; then
    echo "Failed to build shared library"
    exit 1
fi

# Build the minimal server
echo "Building minimal server..."
go build -o build/kcriff-server minimal_server.go

if [ $? -ne 0 ]; then
    echo "Failed to build minimal server"
    exit 1
fi

# Copy Python integration files
echo "Copying Python files..."
cp kcriff_integration.py build/
cp run_desktop_app.py build/
mkdir -p build/pyqt_interface
cp pyqt_interface/*.py build/pyqt_interface/

echo "Build completed successfully."
echo "Output is in the build directory."

# Make scripts executable
chmod +x build/kcriff-server