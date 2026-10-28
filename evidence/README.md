# Laboratory Forensic Evidence & Telemetry Directory

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## Directory Architecture

This directory houses all empirical evidence collected during laboratory execution:

- **`screenshots/`**: Visual evidence and terminal captures documenting each phase of the laboratory experiment (Figures 01 through 16).
- **`logs/`**: Raw terminal session logs, socket audits (`ss`, `netstat`), process tables (`ps aux`), and file status outputs.
- **`packet_captures/`**: Network traffic capture files (`.pcap`) recorded during socket communication on the loopback adapter (`lo`).

---

## Logging Guidelines for Students

To capture pristine command output logs during VM execution, use the Linux `tee` utility or `script`:
```bash
# Example: Log session output to file while viewing on terminal
python3 lab/safe_shell_simulation/server.py 2>&1 | tee evidence/logs/server_execution.log

# Example: Log socket status
ss -tulpn > evidence/logs/ss_listening_ports.log
```
