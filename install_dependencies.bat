@echo off
echo Installing SEBI Safe Space Dependencies...
echo.

echo Installing core dependencies...
pip install streamlit requests pandas openpyxl

echo.
echo Installing fraud detection dependencies...
pip install opencv-python werkzeug numpy flask flask-cors

echo.
echo Installation complete!
echo.
echo To run the application:
echo   streamlit run sebi_safe_space.py --server.port 8505
echo.
echo For full functionality (with deepfake detection):
echo   1. Terminal 1: python deepfake_api.py
echo   2. Terminal 2: streamlit run sebi_safe_space.py --server.port 8505
echo.
pause