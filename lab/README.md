# Laboratory Simulation & Experimentation Directory

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## Laboratory Contents

This directory contains the source code, client scripts, and execution manifests for the practical laboratory demonstrations:

- **`safe_shell_simulation/`**: Directory containing the educational bind-shell simulation components:
  - `server.py`: Safe loopback-only bind-shell simulation server binding strictly to `127.0.0.1:54321`. Evaluates predefined harmless commands (`STATUS`, `HELP`, `EXIT`) and rejects all arbitrary OS commands.
  - `client.py`: Interactive local test client for socket verification and protocol testing.
  - `README.md`: Technical architecture, safety protocols, protocol specifications, and execution instructions.

---

## Safety Guidelines Reminder

1. **Host-Only / Disconnected Execution:** Always execute scripts within the isolated virtual machine.
2. **Loopback Only:** Verify that `server.py` remains bound to `127.0.0.1`. Never modify binding to `0.0.0.0`.
3. **No Malicious Payloads:** Do not introduce external malicious scripts into this repository.
