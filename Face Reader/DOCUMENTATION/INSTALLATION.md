# FaceVault Installation Guide

This guide will walk you through setting up FaceVault on your system.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Troubleshooting](#troubleshooting)
4. [Verification](#verification)

## System Requirements

### Operating System
- Linux (Ubuntu 18.04+, Debian 10+, etc.)
- macOS (10.14+)
- Windows 10/11

### Software Requirements
- Python 3.8 or higher
- pip (Python package installer)
- cmake 3.15 or higher
- C++ compiler (GCC, Clang, or MSVC)
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

### Hardware Requirements
- CPU: Dual-core processor or better
- Optional: GPU with CUDA support for faster processing
- Webcam (optional, for live recognition)

## Step-by-Step Installation

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-python-dev
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake
brew install python@3.11
```

#### Windows
1. Download and install Python from [python.org](https://www.python.org/downloads/)
   - ✓ Check "Add Python to PATH" during installation
2. Download and install CMake from [cmake.org](https://cmake.org/download/)
   - Choose "Add CMake to system PATH"
3. Install Visual Studio Build Tools:
   - Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/downloads/)
   - Select "Desktop development with C++" workload

### 2. Clone or Download FaceVault

```bash
# Option 1: If you have git
git clone <repository-url>
cd face-recognition-system

# Option 2: Extract the downloaded ZIP file
unzip face-recognition-system.zip
cd face-recognition-system
```

### 3. Set Up Python Environment

#### Using Virtual Environment (Recommended)

**Linux/macOS:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

### 4. Install Python Dependencies

This step may take 10-20 minutes as it builds dlib from source.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Progress indicators:**
- Installing cmake...
- Installing dlib... (this takes the longest)
- Installing face_recognition...
- Installing other dependencies...

### 5. Verify Installation

Run the test script:

```bash
cd ..
python test.py
```

You should see:
```
✓ Flask installed
✓ face_recognition installed
✓ numpy installed
✓ Pillow installed
✓ sqlite3 available
✓ All tests passed!
```

### 6. Start FaceVault

**Linux/macOS:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

Or manually:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
# Open index.html in your browser
```

## Troubleshooting

### Issue: "cmake not found"

**Solution:**
- Verify cmake is installed: `cmake --version`
- On Linux/Mac: `sudo apt-get install cmake` or `brew install cmake`
- On Windows: Reinstall CMake and ensure "Add to PATH" is checked

### Issue: "dlib installation failed"

**Linux/Mac Solution:**
```bash
# Install additional dependencies
sudo apt-get install libboost-all-dev  # Ubuntu/Debian
brew install boost  # macOS
```

**Windows Solution:**
1. Ensure Visual Studio Build Tools are installed
2. Try installing the wheel directly:
```cmd
pip install dlib-19.24.2-cp311-cp311-win_amd64.whl
```

### Issue: "No module named 'face_recognition'"

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall
pip install face_recognition --break-system-packages
```

### Issue: "Could not build wheels for dlib"

**Solution:**
```bash
# Install dlib dependencies
pip install cmake
pip install dlib --verbose

# If still failing, try pre-built wheel:
pip install dlib-binary
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill the process or change port in backend/app.py:
app.run(debug=True, port=5001)  # Use different port
```

### Issue: "CORS error in browser"

**Solution:**
1. Verify backend is running: visit `http://localhost:5000/api/stats`
2. Check browser console for specific error
3. Ensure `flask-cors` is installed: `pip install flask-cors`

### Issue: "Face detection is very slow"

**Solutions:**
1. Use smaller images (800-1200px width recommended)
2. Ensure you're using HOG model (not CNN):
   ```python
   face_locations = face_recognition.face_locations(image, model="hog")
   ```
3. Consider using GPU acceleration (requires CUDA)

### Issue: "Database locked" error

**Solution:**
```bash
# Close any other processes accessing the database
# Delete the lock file
rm database/faces.db-journal

# Restart the backend
```

## Verification Checklist

After installation, verify these work:

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Can upload an image
- [ ] Face registration works
- [ ] Face recognition works
- [ ] Database stores faces persistently
- [ ] Can delete registered faces
- [ ] Stats update correctly

## Performance Optimization

### For Faster Recognition

1. **Use HOG model** (default, faster):
```python
model="hog"
```

2. **Reduce image size** before processing:
```python
max_width = 1200
if image.width > max_width:
    ratio = max_width / image.width
    image = image.resize((max_width, int(image.height * ratio)))
```

3. **Adjust tolerance** for speed vs accuracy:
```python
tolerance=0.6  # Default (balanced)
tolerance=0.5  # Stricter (slower, more accurate)
tolerance=0.7  # Looser (faster, less accurate)
```

### For Better Accuracy

1. **Use CNN model** (slower but more accurate):
```python
face_locations = face_recognition.face_locations(image, model="cnn")
```

2. **Use higher resolution images** for registration

3. **Ensure good lighting** in photos

4. **Use front-facing photos** without obstructions

## Next Steps

Once installed:

1. Read the [Usage Guide](USAGE.md) to learn how to use FaceVault
2. Check the [API Documentation](API.md) for integration
3. Review [Best Practices](BEST_PRACTICES.md) for optimal results
4. Explore [Advanced Configuration](ADVANCED.md) for customization

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Run `python test.py` to diagnose problems
3. Review logs in `backend/facevault.log`
4. Check GitHub issues for similar problems
5. Create a new issue with:
   - Operating system and version
   - Python version: `python --version`
   - Error messages
   - Steps to reproduce

## Uninstallation

To remove FaceVault:

```bash
# Remove virtual environment
rm -rf backend/venv

# Remove database
rm -rf database/

# Remove the entire project
cd ..
rm -rf face-recognition-system
```

---

**Installation complete!** 🎉

Your FaceVault system is ready to use. Run `./start.sh` to begin.
