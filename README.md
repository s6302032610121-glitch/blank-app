# 🏗️ StructureCAD AI

StructureCAD AI is a professional, high-fidelity structural engineering application built with Streamlit. It combines an AI-powered engineering assistant with specialized tools for structural analysis and design.

## 🚀 Features

- **💬 AI Structural Assistant**: A specialized chatbot powered by OpenAI, expert in structural analysis and design codes (ACI, AISC, EIT).
- **📊 2D Beam Analysis**: Analyze beams with custom spans, multiple support types (Pin, Roller, Fixed), and point/UDL loads. Generates Shear Force (SFD) and Bending Moment (BMD) diagrams.
- **📐 Truss Analysis**: Interactive solver for 2D trusses using the matrix method to calculate axial member forces.
- **🧱 RC Design**: Reinforced concrete beam reinforcement calculator based on factored moments.
- **📚 Steel Sections**: Integrated database for Thai standard H-Beams (TIS).

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/s6302032610121-glitch/structurecad.git
   cd structurecad
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## ⚙️ Requirements

- Python 3.8+
- Streamlit
- OpenAI API Key (for Chatbot features)
- anastruct
- plotly
- pandas

## 📝 License

This project is licensed under the Apache License 2.0.
