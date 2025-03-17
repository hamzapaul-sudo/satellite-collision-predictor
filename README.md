# 🛰️ Satellite Collision Predictor  
**Real-time Satellite Tracking & Collision Detection using FastAPI, Streamlit, and Orekit**  

## 🚀 Project Overview  
This project tracks active satellites in orbit, predicts future positions, and detects potential **collisions** using **FastAPI, Orekit, and Streamlit**.

### 🔹 **Features**:  
- 🛰️ Fetch **live TLE data** from NORAD
- 📈 **Orbit Propagation** using Orekit  
- 🌍 **3D Visualization** of satellite orbits  
- ⚠️ **Collision Detection** with threshold-based warnings  
- 🎨 **Streamlit Dashboard** for interactive UI  

---

## 🛠️ **Installation**
### ✅ 1. **Run Locally with Docker**
```bash
git clone https://github.com/hamzapaul-sudo/satellite-collision-predictor.git
cd satellite-collision-predictor
docker build -t satellite-tracker .
docker run -p 8501:8501 satellite-tracker
```
🔹 Open **Streamlit UI**: [http://localhost:8501](http://localhost:8501)  

---

### ✅ 2. **Run Locally Without Docker**
```bash
git clone https://github.com/hamzapaul-sudo/satellite-collision-predictor.git
cd satellite-collision-predictor
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

#### Start **Streamlit Dashboard**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🚀 **Live Demo (Render)**
🔹 **Streamlit UI**: [https://satellite-collision-predictor.onrender.com](https://satellite-collision-predictor.onrender.com)

---

## 🛠️ **Technologies Used**
- 🐍 **Python 3.11**  
- 🎨 **Streamlit** (Dashboard UI)  
- 🌍 **Orekit** (Orbit Propagation)  
- 📦 **Docker** (Deployment)  
- ☁️ **Render** (Cloud Hosting)  

---

## 🎯 **Future Improvements**
- [ ] 🛰 **More accurate orbit predictions**  
- [ ] 🌍 **3D visualization with Cesium.js**  
- [ ] 📡 **Add real-time satellite tracking**  

---

## 🤝 **Contributing**
Contributions are welcome! Fork the repo and submit a **Pull Request**.

---

## 📧 **Contact**
📌 **GitHub:** [Hamza Paul](https://github.com/hamzapaul-sudo)  
📌 **LinkedIn:** [Hamza Paul](https://www.linkedin.com/in/pa-u-271654269)  

🚀 **Happy Coding!** 🛰️

