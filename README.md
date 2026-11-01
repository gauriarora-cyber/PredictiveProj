## Run the Project Locally (Windows)

### 1. Download the project
- Open this GitHub repository.
- Click **Code → Download ZIP**.
- Extract the ZIP file.
- Open the extracted `PredictiveProj-main` folder in VS Code.

Alternatively, clone the repository:

```bash
git clone https://github.com/gauriarora-cyber/PredictiveProj.git
cd PredictiveProj
```

### 2. Open the terminal

In VS Code, select **Terminal → New Terminal**.

### 3. Create a virtual environment

```powershell
py -m venv .venv
```

### 4. Activate the virtual environment

For PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Command Prompt (CMD):

```cmd
.venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python web_app.py
```

### 7. Open the application

Open your browser and visit:

http://127.0.0.1:5000

The Flask server must remain running while using the application.

## Requirements

- Python installed on your computer
- Git (if cloning the repository)
- VS Code (recommended)
- Internet connection for installing dependencies