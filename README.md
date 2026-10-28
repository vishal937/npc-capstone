# NPC Capstone Project: Malware Analysis Sandbox Using VirtualBox or VMware

[![Sanbox Type](https://img.shields.io/badge/Sandbox-Type--2%20Hypervisor-blue.svg)](#)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)](#)
[![Security Policy](https://img.shields.io/badge/Security-Safe%20Loopback%20Simulation-success.svg)](#)
[![Academic Status](https://img.shields.io/badge/Course-NPC%20Capstone%20Project-navy.svg)](#)

A comprehensive, academically rigorous, and security-hardened implementation of a **Dynamic Malware Analysis Sandbox** using Type-2 hypervisors (Oracle VM VirtualBox and VMware Workstation Pro / Player). 

This project demonstrates hypervisor security hardening, strict host-only / loopback network containment, copy-on-write snapshot engineering (`NPC_Capstone_Clean_State`), real-time socket and process telemetry monitoring, NIST-standard cryptographic verification, responsible threat intelligence querying via VirusTotal, and snapshot-based disaster recovery.

---

## Academic & Student Credentials

| Parameter | Details |
|---|---|
| **Student Name** | **Vishal Katyare** |
| **PRN Number** | **2125UCSM1034** |
| **Course / Program** | Bachelor of Technology (B.Tech) |
| **Department** | Computer Science Engineering |
| **Specialization** | Cyber Security |
| **Institution** | Sanjivani University, Kopargaon |
| **Academic Year** | 2026–2027 |
| **Subject** | NPC (Capstone Project) |
| **Project Repository** | [https://github.com/vishal937/npc-capstone.git](https://github.com/vishal937/npc-capstone.git) |
| **Final PDF Report** | [NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf) |

---

## Executive Summary & Architecture

Dynamic malware analysis is essential for identifying runtime behaviors, C2 communication protocols, and evasion techniques that evade static detection. However, detonating untrusted code demands airtight isolation.

```text
+-----------------------------------------------------------------------------------+
| PHYSICAL HOST SYSTEM (Hardware / OS)                                              |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | HYPERVISOR LAYER (Oracle VM VirtualBox / VMware Workstation)                |  |
|  | Hardening: 3D Accel OFF | Shared Clipboard OFF | Shared Folders REMOVED     |  |
|  |                                                                             |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | ISOLATED GUEST LINUX VIRTUAL MACHINE (Ubuntu 24.04 LTS / Debian 12)    |  |  |
|  |  | 2 vCPUs | 4096 MB RAM | 30 GB Disk                                      |  |  |
|  |  | Base Snapshot: NPC_Capstone_Clean_State (Copy-on-Write Delta Disk)      |  |  |
|  |  |                                                                       |  |  |
|  |  |  +---------------------------+       +----------------------------+   |  |  |
|  |  |  | Safe Server (server.py)   |<======| Safe Client (client.py)    |   |  |  |
|  |  |  | Bound: 127.0.0.1:54321    | (TCP) | Connects: 127.0.0.1:54321  |   |  |  |
|  |  |  | Allowed: STATUS/HELP/EXIT |       | Interactive Diagnostic CLI |   |  |  |
|  |  |  +-------------+-------------+       +----------------------------+   |  |  |
|  |  |                |                                                       |  |  |
|  |  |  +-------------v---------------------------------------------------+   |  |  |
|  |  |  | KERNEL TELEMETRY MONITORING & PACKET CAPTURE                     |   |  |  |
|  |  |  | Socket State: ss -tulpn | Process Table: ps aux / pstree       |   |  |  |
|  |  |  | Descriptors: lsof -i :54321 | Loopback Capture: tcpdump -i lo    |   |  |  |
|  |  |  +------------------------------------------------------------------+   |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## Laboratory Safety & Compliance Manifesto

In strict adherence to educational cybersecurity laboratory guidelines:
- **Zero Arbitrary Command Execution:** The simulation server rejects all OS shell commands (`ls`, `whoami`, `cat`, etc.) and does not spawn any subprocess (`os.system`, `subprocess`).
- **Loopback-Only Confinement:** The listener binds exclusively to IPv4 `127.0.0.1` on port `54321`. External interfaces are never bound.
- **Network Air-Gapping:** The virtual machine network adapter is disconnected from physical gateways, ensuring 100% egress prevention.
- **OPSEC Threat Intelligence:** VirusTotal queries are conducted solely via SHA-256 cryptographic hashes; local files are never uploaded.

---

## Repository Directory Layout

```text
npc-capstone/
|-- README.md                                 # Master project blueprint & instructions
|-- .gitignore                                # Excludes VM disks (*.vmdk, *.vdi), dumps, logs
|-- generate_pdf.py                           # Python ReportLab academic PDF generator
|
|-- report/
|   |-- NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf  # Final compiled PDF report (<10 MB)
|   |-- report_source.md                      # Comprehensive markdown report source
|
|-- documentation/
|   |-- Lab_Setup_Guide.md                    # VM specs, VirtualBox & VMware setup, network modes
|   |-- Network_Isolation_Guide.md            # Loopback vs WAN, ping/curl verification, tcpdump
|   |-- Snapshot_Recovery_Guide.md            # CoW deltas, baseline snapshot, post-recovery audit
|   |-- Monitoring_Guide.md                   # ps, top, ss, lsof, stat, journalctl monitoring
|   |-- VirusTotal_Analysis_Guide.md          # Multi-engine threat intel, hash-based OPSEC lookup
|   |-- Results_and_Observations.md           # 16-point empirical vs theoretical results matrix
|   |-- Screenshot_Checklist.md               # 16-point screenshot checklist & CLI commands
|
|-- lab/
|   |-- README.md                             # Lab exercises overview and safety protocols
|   |-- safe_shell_simulation/
|       |-- README.md                         # Architecture, safety comparison, and verification
|       |-- server.py                         # Safe loopback bind-shell simulation server
|       |-- client.py                         # Interactive local test client
|
|-- evidence/
|   |-- README.md                             # Evidence collection guidelines
|   |-- screenshots/                          # PNG captures for Figures 01 to 16
|   |-- logs/                                 # Raw terminal logs (isolation, socket, process)
|   |-- packet_captures/                      # Loopback pcap files (tcpdump traces)
|
|-- analysis/
|   |-- File_Identification.md                # Static analysis, file type, stat metadata
|   |-- Hash_Results.md                       # Genuine MD5, SHA-1, SHA-256 cryptographic digests
|   |-- VirusTotal_Findings.md                # Multi-engine lookup report and status statement
|
|-- references/
|   |-- References.md                         # IEEE & academic citations (NIST, MITRE, RFCs)
|
|-- vm/
|   |-- README.md                             # VM hardware manifest, OS specs, and hardening
```

---

## Cryptographic Hash Registry

Cryptographic digests calculated for the primary simulation scripts:

| File Name | File Size | MD5 Digest | SHA-1 Digest | SHA-256 Digest |
|---|---|---|---|---|
| `server.py` | 10,337 bytes | `363fb4b6141fd879188ab86742f5e78b` | `0d0c8b3f0ea0956a061aaa850f56c5c4b8c716c6` | `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa` |
| `client.py` | 4,759 bytes | `132c47a87200232d07ff7be0c4b74d81` | `eabb5aeb3238f69b3b2b9b48b1a20b5128602cb1` | `d5d37de3e4b02a148ba382809ebcea844f213a8498510e772838ba269c15598a` |

### VirusTotal Query Finding
- **Query Target:** `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa`
- **Result:** `No results found (0/70+ engines)`
- **Official Finding Statement:** *"No existing VirusTotal report was available for the investigated file at the time of analysis."*

---

## Step-by-Step Laboratory Execution Instructions

### Step 1: Provision the VM & Verify Network Isolation
1. Create a Linux VM (Ubuntu 24.04 LTS / Debian 12) with 2 vCPUs, 4 GB RAM, and 30 GB disk in VirtualBox or VMware.
2. In VM Settings, set Network Adapter 1 to **Host-Only** or uncheck **Cable Connected**.
3. Inside the VM terminal, verify network isolation:
   ```bash
   # Check interfaces
   ip addr show
   
   # Confirm no default gateway
   ip route show
   
   # Verify outbound ICMP fails (Network unreachable / 100% loss)
   ping -c 3 8.8.8.8
   
   # Verify DNS resolution fails
   ping -c 3 google.com
   ```

### Step 2: Establish Clean Baseline Snapshot
1. Power off the VM:
   ```bash
   sudo shutdown -h now
   ```
2. In the hypervisor GUI, open **Snapshots** and take a new snapshot:
   - **Name:** `NPC_Capstone_Clean_State`
   - **Description:** `Baseline clean state of Linux VM with zero active listeners. Student: Vishal Katyare (PRN: 2125UCSM1034).`
3. Power the VM back on.

### Step 3: Run the Safe Bind-Shell Simulation
1. **Terminal 1 — Start the Server:**
   ```bash
   python3 lab/safe_shell_simulation/server.py
   ```
2. **Terminal 2 — Start Packet Capture:**
   ```bash
   sudo tcpdump -i lo -nnvv -s 0 -w evidence/packet_captures/loopback_shell.pcap port 54321
   ```
3. **Terminal 3 — Connect the Safe Client:**
   ```bash
   python3 lab/safe_shell_simulation/client.py
   ```
4. **Execute Commands:**
   - Type `STATUS` -> Displays process metadata, student PRN, and uptime.
   - Type `HELP` -> Displays safe command usage and security policy.
   - Type `whoami` -> Demonstrates security rejection: `[SECURITY REJECTION] Command 'WHOAMI' is NOT permitted.`
   - Type `EXIT` -> Closes session cleanly.

### Step 4: Monitor System Telemetry
In another terminal, inspect process and socket status:
```bash
# Check listening socket
sudo ss -tulpn | grep 54321

# Check running process
ps aux | grep server.py

# Check open file descriptors
sudo lsof -i :54321
```

### Step 5: Restore Clean Snapshot & Audit Eradication
1. Power off the VM.
2. In the hypervisor, select `NPC_Capstone_Clean_State` and click **Restore / Revert**.
3. Power on the VM and execute the post-recovery audit:
   ```bash
   # Verify port 54321 is closed (must return empty)
   sudo ss -tulpn | grep 54321
   
   # Verify server process is gone (must return empty)
   ps aux | grep server.py
   ```

---

## Compiling the Academic PDF Report

The repository includes a dedicated ReportLab compiler (`generate_pdf.py`) that generates the university-grade submission PDF:

```bash
python generate_pdf.py
```

The script compiles:
- Formal cover page with student details (Vishal Katyare, PRN: 2125UCSM1034)
- Two-pass `NumberedCanvas` dynamic page numbering ("Page X of Y"), running headers, and footers
- Comprehensive research sections (1.0 to 16.0)
- Master Results Matrix and IEEE References
- Appendix A: 16-point screenshot plates (embeds genuine PNGs from `evidence/screenshots/` or renders professional placeholder frames)
- Output location: [report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf](report/NPC_Capstone_Malware_Analysis_Sandbox_Report.pdf) (< 10 MB).

---

## License & Academic Disclaimer

This project is created strictly for academic and educational purposes under the **Bachelor of Technology (B.Tech)** curriculum at **Sanjivani University, Kopargaon**. All scripts and documentation are engineered to prevent harm, enforce network isolation, and adhere to responsible cybersecurity laboratory practices.
