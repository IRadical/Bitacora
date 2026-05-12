# 🐎 RADICAL - Log Automator Pro
> **Intelligent automation for emergency power plant maintenance logs.**

![Branding](https://img.shields.io/badge/Brand-RADICAL-D4A373?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/UI-Flet-00d2ff?style=for-the-badge)

## 🎯 The Problem
In the industrial sector, creating maintenance logs is often a tedious manual process: transferring photos, resizing them manually in Word, and repeatedly typing technical data. This workflow used to take between 20 to 30 minutes per power plant.

## 🚀 The Solution (RADICAL Log Automator)
I developed a standalone desktop application that reduces this process to **under 2 minutes**. The software handles photographic evidence, maintains technical data persistence (JSON), and generates a professional `.docx` report ready for submission.

### ✨ Key Features:
* **Premium Visual Identity:** Custom dark-mode UI (Japandi/Modern Cowboy aesthetic) optimized for industrial environments.
* **Automated Image Processing:** Automatically resizes and injects photos into a master template while maintaining aspect ratios.
* **Data Persistence:** Tracks total engine hours and starts using a local JSON storage layer.
* **Dynamic Configuration:** Enables users to swap the Word template directly through the UI without modifying code.
* **Portable Execution:** Packaged as a standalone `.exe`—no Python installation required for end-users.

## 🛠️ Tech Stack
* **Python 3.10** (Core logic)
* **Flet** (UI framework powered by Flutter)
* **docxtpl & python-docx** (Office Open XML template manipulation)
* **Pillow** (Image processing)
* **PyInstaller** (Binary packaging)

## 📁 Project Structure
```text
├── core/               # Image processing and resizing logic
├── data/               # JSON persistence (Hours/Starts tracking)
├── fotos/              # Temporary directories for evidence categories
├── reportes_finales/   # Output directory for generated .docx files
├── main.py             # Application entry point
└── plantilla_maestra.docx # Official corporate report template
