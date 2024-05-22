REM Download and install the required dependencies for the project on Windows

echo Install espeak-ng...
curl -L "https://github.com/espeak-ng/espeak-ng/releases/download/1.51/espeak-ng-X64.msi" --output "espeak-ng-X64.msi"
espeak-ng-X64.msi
del espeak-ng-X64.msi

python3.10 -m venv venv
call .\venv\Scripts\activate
pip install -r requirements.txt

echo Done!