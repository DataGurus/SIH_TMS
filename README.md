# 🛰️ Smart Tourist Safety Monitoring & Incident Response System  

A **real-time safety monitoring platform** designed to enhance tourist safety using **AI, geo-fencing, and blockchain-based digital IDs**.  
The system provides **tourist tracking, incident response, unit management, and safety analytics** — all in a unified admin dashboard.  

---

## 📜 About The Project  

Tourism is a key economic driver in regions like the Northeast of India, but ensuring visitor safety remains a challenge.  
This project introduces a **smart, technology-driven solution** that allows authorities to:  

- Monitor tourists in real-time via digital IDs and geo-fencing.  
- Detect anomalies in tourist movement and respond proactively.  
- Provide tourists with mobile app safety features like panic buttons and alerts.  
- Enable quick law enforcement response with e-FIR generation.  

The goal is **rapid incident response, proactive safety, and secure tourist management**.  

---

## ✨ Key Features  

### 👮‍♂️ Admin Dashboard  
- **Real-Time Map:** Visualize tourist clusters, incidents, and police unit locations.  
- **Incident Management:** Panic alerts, anomaly detection, missing person tracking, automated e-FIR.  
- **Quick KPIs:** Active tourists, tourists in risk zones, average safety score, response times, hotspot alerts.  
- **Unit Management:** Track unit availability, dispatch police resources, monitor coverage gaps.  
- **Analytics:** Incident trends, hotspot forecasting, tourist flow insights.  
- **Audit Logs:** Track actions taken for transparency.  

### 📱 Tourist Mobile App (future scope)  
- Blockchain-based **Digital Tourist ID** (Aadhaar/Passport + itinerary).  
- **Safety Score:** Auto-assigned based on travel patterns and zones visited.  
- **Geo-fencing Alerts:** Notifications when entering high-risk areas.  
- **Panic Button:** Instant location sharing with police + emergency contacts.  
- **Family Tracking (Opt-in):** Real-time tracking for safety reassurance.  

### 🌐 Multilingual Support  
- App and dashboard available in **10+ Indian languages + English**.  
- Voice/text emergency features for elderly and disabled tourists.  

### 🔐 Data Privacy & Security  
- End-to-end encrypted communication.  
- Blockchain-backed tamper-proof ID & travel logs.  
- Compliance with India’s **DPDPA (Digital Personal Data Protection Act)**.  

---

## 🛠️ Tech Stack  

- **Frontend:** React (JavaScript), TailwindCSS, React Router  
- **Maps & Geo:** Leaflet / MapLibre  
- **Data Visualization:** Recharts  
- **Tables:** TanStack Table  
- **Build Tool:** Vite  
- **Backend (future scope):** Flask / Node.js  
- **Database (future scope):** SQL + Pinecone (for vector search in AI modules)  

---

## ⚙️ Getting Started  

Follow these steps to run the project locally.  

### ✅ Prerequisites  
- Node.js **v18+**  
- npm **v9+**  

### 📥 Installation  

## Using Docker (Recommended)
```bash

# Clone repository
git clone https://github.com/your-username/smart-tourist-safety.git

# Navigate to frontend folder
cd frontend

# Build Docker Image
docker build -t tad-dashboard .

# Run Docker Image with Port Mapping 
docker run -it \
-p 8081:80/tcp \
tad-dashboard

```
## Using Npm

```bash
# Clone repository
git clone https://github.com/your-username/smart-tourist-safety.git

# Enter project directory
cd smart-tourist-safety

# Install dependencies
npm install
```  



### ▶️ Running the App  

```bash
npm run dev
```  

This will start the **Vite development server**.  
Open in browser: [http://localhost:5173](http://localhost:5173)  

---

## 📄 License  

Distributed under the MIT License. See `LICENSE` for details.  

---

💡 *Built for hackathons and real-world deployment in collaboration with state tourism and police departments.*  
