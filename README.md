# 🛡️ Zero Trust SOC Homelab

A containerized **Security Operations Center (SOC) homelab** built to demonstrate Zero Trust access control, centralized security logging, security event detection, and SOC-style monitoring using Docker.

The project integrates **Traefik, Authelia, Grafana Loki, Grafana Alloy, Grafana, and a custom Flask-based SOC dashboard** into an end-to-end security monitoring environment.

---

## 🎯 Project Overview

This project simulates a small enterprise security monitoring environment where application traffic passes through an authenticated reverse proxy, security logs are centrally collected, and security events are analyzed through Grafana and a custom SOC dashboard.

### Architecture

```text
                    ┌──────────────────────┐
                    │      Kali Linux      │
                    │   Security Testing   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Traefik        │
                    │    Reverse Proxy     │
                    │   HTTPS + Access Log │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Authelia        │
                    │ Authentication /     │
                    │   Access Control     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       whoami         │
                    │   Protected Service  │
                    └──────────────────────┘

                               │
                              Logs
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Grafana Alloy     │
                    │    Log Collection    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        Loki          │
                    │ Centralized Logging  │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │     Grafana      │   │  Flask Backend   │
          │ Log Analytics    │   │ Event Processing │
          └──────────────────┘   └────────┬─────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │  Custom SOC      │
                                │    Dashboard     │
                                └──────────────────┘

The main objectives of this project are to:
- Implement Zero Trust-style authentication
- Protect internal services using Authelia
- Use Traefik as a reverse proxy
- Collect security and application logs centrally
- Implement centralized logging using Grafana Loki
- Use Grafana Alloy for log collection
- Build a custom Flask backend for security event processing
- Develop a custom SOC monitoring dashboard
- Detect authentication failures
- Detect unauthorized and forbidden requests
- Detect suspicious HTTP activity
- Perform controlled security testing using Kali Linux
- Visualize security events using Grafana


Zero Trust Architecture
The protected application is accessed through an authentication layer rather than being directly exposed.
User
 │
 ▼
Traefik
 │
 ▼
Authelia Authentication
 │
 ├── Authentication Failed ──► Security Logs
 │
 └── Authentication Successful
                 │
                 ▼
          Protected Service

Traefik acts as the reverse proxy while Authelia provides authentication and access control before requests reach the protected application.
🧰 Technology Stack
Infrastructure
- Docker
- Docker Compose
- Traefik
- Authelia
Security
- Zero Trust principles
- Authentication and access control
- HTTP anomaly detection
- Suspicious request detection
- Security event classification
Logging & Monitoring
- Grafana Loki
- Grafana Alloy
- Grafana
- LogQL
Application
- Python
- Flask
- Requests
- HTML
- CSS
- JavaScript
Security Testing
- Kali Linux
- cURL
- Browser-based testing

Custom SOC Dashboard
A custom SOC dashboard was developed using Flask, HTML, CSS, and JavaScript.
The dashboard provides:
- Total security events
- High-severity events
- Failed authentication attempts
- Unauthorized requests
- Security activity visualization
- Recent security events
- Event source
- Event category
- HTTP status
- Request path
- Severity classification
- Automatic event refresh
- Embedded Grafana analytics
Dashboard Categories
Authentication
Web Traffic
Access
Suspicious Activity
System

🚨 Security Event Detection
The Flask backend queries Loki and transforms raw log entries into structured security events.
Authentication Events
Failed Authentication
Unknown User
Successful Authentication
Authentication Event

HTTP Events
Successful Request
Authentication Redirect
Unauthorized Request
Forbidden Request
Not Found Request
HTTP Request

Suspicious HTTP Activity
The backend detects suspicious requests targeting paths such as:
/.env
/.git
/wp-admin
/wp-login
/phpmyadmin
/admin

Detected suspicious requests are classified as:
Category: Suspicious Activity
Severity: HIGH

The detection logic uses precise path matching to reduce false positives.
📈 Grafana Monitoring
Grafana is integrated into the custom SOC dashboard for deeper security analysis.
The Grafana dashboard contains six monitoring panels:
1. Failed Authentication Attempts
2. Authentication Events
3. Authelia Errors
4. Traefik Web Traffic
5. HTTP Response Status
6. Suspicious HTTP Activity
The project therefore provides two levels of monitoring:
Custom SOC Dashboard
        +
Grafana Analytics
        ↓
Security Monitoring

🔎 Security Testing
The environment was tested using Kali Linux to generate controlled security events.
Testing included:
- Authentication failures
- Unauthorized requests
- Protected service access
- Suspicious HTTP paths
- HTTP response monitoring
- Authentication redirects
- Normal web traffic
Example Detection
A controlled request to:
curl -k -I https://whoami.soc.example.com/.env

generates a Traefik access log that is collected by Alloy and stored in Loki.
The Flask backend processes the event and identifies it as:
Source:    traefik
Category:  Suspicious Activity
Event:     Suspicious HTTP Request
Severity:  HIGH
Path:      /.env

Normal application requests are classified separately as regular web traffic.
🔄 Log Processing Pipeline
HTTP Request
     │
     ▼
  Traefik
     │
     ├──────────────► Access Logs
     │
     ▼
  Authelia
     │
     ├──────────────► Authentication Logs
     │
     ▼
Grafana Alloy
     │
     ▼
   Loki
     │
     ├──────────────────────┐
     ▼                      ▼
  Grafana             Flask Backend
     │                      │
     │                      ▼
     │               Event Classification
     │                      │
     └──────────────┬───────┘
                    ▼
             Custom SOC Dashboard

📁 Project Structure
zero-trust-soc-homelab/
│
├── alloy/
│   └── config.alloy
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   └── app/
│       ├── app.py
│       │
│       ├── static/
│       │   ├── css/
│       │   │   └── style.css
│       │   │
│       │   └── js/
│       │       └── dashboard.js
│       │
│       └── templates/
│           └── dashboard.html
│
├── loki/
│   └── loki-config.yml
│
├── traefik/
│   └── dynamic.yml
│
├── docker-compose.yml
│
└── .gitignore

Sensitive files such as authentication databases, credentials, private keys, certificates, and runtime data are intentionally excluded from the repository.
⚙️ Deployment
Prerequisites
- Docker Desktop
- WSL2 / Ubuntu
- Git
- Kali Linux for security testing
Clone the Repository
git clone git@github.com:Joyeeta-uckoo/zero-trust-soc-homelab.git

cd zero-trust-soc-homelab

Create Docker Network
docker network create zt-net

Start the Environment
docker compose up -d --build

Check Containers
docker compose ps

View Logs
docker compose logs -f

🌐 Local Services
Custom SOC Dashboard
http://localhost:5000

Grafana
http://localhost:3000

Traefik Dashboard
http://localhost:8081

Authentication Service
https://auth.soc.example.com

Protected Application
https://whoami.soc.example.com

The soc.example.com hostnames are intended for the local homelab environment and require appropriate hosts-file configuration.
🛡️ Security Considerations
This project is intended for educational and defensive security testing.
The following are intentionally excluded from GitHub:
Authelia credentials
Authentication databases
Private keys
TLS certificates
Environment secrets
Runtime databases

The .gitignore file prevents these sensitive files from being committed.
Security testing should only be performed against systems and networks where you have authorization.
🚀 Future Improvements
- [ ] MITRE ATT&CK technique mapping
- [ ] Automated alert generation
- [ ] Brute-force detection
- [ ] IP reputation checks
- [ ] Threat intelligence integration
- [ ] GeoIP enrichment
- [ ] Authentication attack-rate detection
- [ ] Security incident timeline
- [ ] Automated security reports
- [ ] Email/Telegram alerts
- [ ] Docker container health monitoring
- [ ] Role-based SOC dashboard access
- [ ] Advanced HTTP anomaly detection
📚 Learning Outcomes
This project provided practical experience with:
- Zero Trust security concepts
- Reverse proxies
- Authentication middleware
- Centralized logging
- Log aggregation
- LogQL
- Security event processing
- HTTP security monitoring
- Web anomaly detection
- Docker networking
- Containerized deployments
- Flask REST APIs
- SOC dashboard development
- Kali Linux security testing
- Git and GitHub workflows
