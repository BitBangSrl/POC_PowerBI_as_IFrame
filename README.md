# POC_PowerBI_as_IFrame

## 📌 Overview

Questo progetto rappresenta una Proof of Concept (PoC) per l'integrazione di report Power BI all'interno di una web application custom, supportando due diversi modelli di accesso ai dati:

- **App owns data [Work in progress]**
- **User owns data**

L'obiettivo della PoC è validare i flussi di autenticazione, il controllo degli accessi ai dati e l'integrazione della Row-Level Security (RLS) in un'architettura cloud moderna.

---

## 🧱 Struttura del progetto

Il repository è organizzato come monorepo e contiene sia il frontend che il backend:

---

## ⚙️ Tecnologie utilizzate

### Frontend
- HTML / JavaScript
- Power BI JavaScript SDK

### Backend
- Python (FastAPI)
- API REST
- Integrazione con Azure Entra ID

### Cloud & Servizi
- GitHub Pages
- Power BI / Fabric

---

## 🔐 Autenticazione e Autorizzazione

L'applicazione supporta due modelli distinti:

---

### 🔹 App owns data (WIP)

- Il backend si autentica tramite **service principal**
- L'accesso a Power BI avviene tramite **Embed Token**
- La RLS è implementata tramite `CustomData()`

---

### 🔹 User owns data

- L’utente effettua login tramite **Microsoft Entra ID**
- Il backend utilizza il **flusso On-Behalf-Of (OBO)**
- Power BI applica la RLS con `USERPRINCIPALNAME()`
- Non viene generato un embed token: viene usato direttamente il token utente

---

## 🔄 Architettura (high level)

L'applicazione è composta da tre livelli principali:

- **Frontend**
  - Gestione interazione utente e embedding del report
- **Backend**
  - Gestione autenticazione, scambio token e chiamate API
- **Power BI**
  - Hosting report, dataset e logica RLS

👉 I dettagli architetturali sono documentati separatamente.

---

## 🚀 Deploy

### Frontend

- Ospitato su **GitHub Pages**
- Deploy automatico a ogni push sul branch configurato

---

### Backend

WIP

---

## 🔧 Configurazione

### Backend

La configurazione è gestita tramite variabili di ambiente:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `POWERBI_WORKSPACE_ID`
- `POWERBI_REPORT_ID`
- `POWERBI_DATASET_ID`

> È presente un file `.env.example` a scopo illustrativo.

---

### Frontend

- Configurazione MSAL (Client ID, Tenant ID)
- URL del backend configurabile in base all’ambiente

---

## 🧪 Scopo della PoC

Questo progetto nasce per:

- Validare i modelli di embedding Power BI
- Confrontare App owns data vs User owns data
- Testare l’integrazione della RLS
- Fornire una base riutilizzabile per sviluppi futuri

---

## 📚 Documentazione

La documentazione dettagliata (diagrammi, flussi OBO, RLS, ecc.) è mantenuta separatamente.

---

## ⚠️ Note

- Questa è una Proof of Concept, non una soluzione production-ready
- Le informazioni sensibili non sono incluse nel repository
- Per uso in produzione è necessario applicare ulteriori misure di sicurezza

---