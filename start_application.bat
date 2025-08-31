@echo off
echo Starting SEBI Safe Space Application...
echo.
echo This will start the main application on http://localhost:8505
echo.
echo For deepfake detection, start deepfake_api.py in a separate terminal first.
echo.
streamlit run sebi_safe_space.py --server.port 8505