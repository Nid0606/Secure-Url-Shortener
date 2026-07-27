# 🛡️ Secure URL Shortener & Redirector

> A "Zero-Trust" URL shortening service built with security at its core—vetting links against malicious APIs, preventing brand impersonation, and providing an unmasking redirect gateway.

🌐 **Live Deployment:** [https://n06.me](https://n06.me)

---

## 📌 About The Project

Traditional URL shorteners blindfold the user: you click a shortened link with no idea where it leads. Cybercriminals heavily exploit this gap to run phishing campaigns, distribute malware, and obscure suspicious domains.

This project solves that exact issue by acting as a **defensive security layer**. Before a URL is shortened, our backend verifies its safety and checks for brand impersonation. When a visitor clicks a generated link, they land on an **informed-consent redirection screen** that unmasks the destination domain, allowing them to verify where they are heading before making the jump.

---

## ✨ Key Features

* 🎲 **Flexible Generation:** Choose between random alphanumeric URL creation with customizable lengths or user-defined custom aliases.
* 🛑 **Anti-Phishing Brand Filter:** Custom regex and blocklist filters reject aliases mimicking major brands (e.g., `google`, `paypal`, `netflix`) to stop impersonation attacks.
* 🛡️ **Automated Threat Detection:** Real-time integration with the **Google Safe Browsing API** together with **ViruTotal Safe Browsing API** scans target links and rejects malicious destinations instantly.
* 🔍 **Unmasking Gateway (Redirection Page):** Visual buffer page displaying the full destination domain, complete with an explicit user permission trigger before navigating away.

---

## 🚀 Architecture & Technical Stack

* **Backend:** Python (Flask), Flask-CORS, REST API
* **Database:** SQLite / Flask-SQLAlchemy
* **External Security APIs:** Google Safe Browsing API, VirusTotal safe Browsing API
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Collaboration & Deployment:** Git, VS Code Live Share, Hosted at [n06.me](https://n06.me)

---

## 🛠️ Development Phases

### Phase 1: Environment Setup & Core Architecture
* Configured virtual environments, dependencies (`Flask`, `flask-cors`, `requests`), and base Flask API boilerplate with CORS handling.
* Established collaborative Git workflow and Live Share workspace setup.

### Phase 2: Database Schema & Base Generation Engine
* Modeled database schema for storing mappings (`short_code`, `long_url`, `report_count`, `is_suspended`).
* Built Base62/random string generator allowing dynamic length configurations.

### Phase 3: Redirection & Unmasking Engine
* Built `GET /api/redirect/<short_code>` route to serve unmasking payloads for frontend gateway rendering.
* Configured conditional logic for handling missing, active, or suspended URLs.

### Phase 4: Defensive Security Shield
* Developed local regex pattern matching to block trademarked domain aliases.
* Integrated Google Safe Browsing API client to perform real-time URL threat verification prior to database insertion.

### Phase 5: Community Flagging Pipeline & Production Deployment
* Engineered `POST /api/report` endpoint to handle user flagging thresholds and auto-suspension triggers.
* Connected frontend to backend endpoints and deployed the live system at **n06.me**.

---

## ⚡ Local Setup & Installation

### Prerequisites
* Python 3.x
* Git

## 🤝 Authors & Credits

* Frontend Lead: Manya Singh/ https://github.com/manya2509
* Backend & Security Lead: Nidhi Chauhan/ https://github.com/Nid0606
