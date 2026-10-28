# 16-Point Laboratory Screenshot Capture Checklist

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Academic Year:** 2026–2027  

---

## 1. Overview for Student Submission

To verify your practical execution of this assignment in the university laboratory, take screenshots corresponding to the **16 designated figures** listed below. Each figure documents a specific milestone in hypervisor provisioning, network isolation, baseline snapshotting, safe shell execution, dynamic monitoring, packet capture, threat intelligence lookup, and snapshot-based disaster recovery.

Save captured image files in PNG format in the `evidence/screenshots/` directory using the standard file naming convention: `Figure_XX_<Description>.png`.

---

## 2. Master Screenshot Checklist (Figures 01 to 16)

| Figure # | Target Milestone | Description & Caption | CLI Capture Command / Visual Target | Status |
|---|---|---|---|---|
| **Figure 01** | **Hypervisor Hardware Configuration** | Virtual machine hardware settings in VirtualBox / VMware showing 2 vCPUs, 4 GB RAM, 30 GB disk, and VMSVGA display controller. | Hypervisor GUI -> VM Settings -> *System / Hardware Overview* | [ ] Pending VM Run |
| **Figure 02** | **Hypervisor Network Adapter Isolation** | Network settings window showing Adapter 1 configured as Host-Only or Cable Disconnected (zero Internet access). | Hypervisor GUI -> VM Settings -> *Network Adapter Settings* | [ ] Pending VM Run |
| **Figure 03** | **Network Isolation Verification (ICMP Ping)** | Terminal showing execution of `ping -c 3 8.8.8.8` returning "Network is unreachable" or 100% packet loss. | `ping -c 3 8.8.8.8` | [ ] Pending VM Run |
| **Figure 04** | **DNS & Web Egress Isolation Verification** | Terminal showing execution of `ping google.com` and `curl http://example.com` failing due to complete lack of routing. | `ping -c 3 google.com && curl --connect-timeout 3 http://example.com` | [ ] Pending VM Run |
| **Figure 05** | **Pre-Execution Baseline (Sockets & Processes)** | Terminal showing `ss -tulpn` and `ps aux` confirming zero custom listeners or simulation processes running. | `sudo ss -tulpn && ps aux \| grep -E "python\|server"` | [ ] Pending VM Run |
| **Figure 06** | **Clean Baseline Snapshot Creation** | Hypervisor Snapshots Manager showing the newly created snapshot named **`NPC_Capstone_Clean_State`**. | Hypervisor GUI -> *Snapshots / Snapshot Manager* | [ ] Pending VM Run |
| **Figure 07** | **Simulation Server Startup (`server.py`)** | Terminal 1 showing `python3 server.py` starting, displaying student name (Vishal Katyare), PRN (2125UCSM1034), and PID. | `python3 lab/safe_shell_simulation/server.py` | [ ] Pending VM Run |
| **Figure 08** | **Active Listener Verification (`ss -tulpn`)** | Terminal 2 showing `ss -tulpn` confirming TCP port 54321 in `LISTEN` state bound strictly to `127.0.0.1`. | `sudo ss -tulpn \| grep 54321` | [ ] Pending VM Run |
| **Figure 09** | **Process Table & Open File Descriptors** | Terminal showing `ps aux` and `lsof -i :54321` confirming the Python process and open socket descriptor. | `ps aux \| grep server.py && sudo lsof -i :54321` | [ ] Pending VM Run |
| **Figure 10** | **Simulation Client Connection (`client.py`)** | Terminal 2 showing `python3 client.py` connecting to 127.0.0.1:54321 and receiving the initial interactive banner. | `python3 lab/safe_shell_simulation/client.py` | [ ] Pending VM Run |
| **Figure 11** | **Command Execution: `STATUS` & `HELP`** | Interactive client session executing `STATUS` (displaying student PRN and server uptime) and `HELP`. | `STATUS` and `HELP` in `client.py` | [ ] Pending VM Run |
| **Figure 12** | **Security Control: Arbitrary Command Rejection** | Client session attempting unauthorized command (e.g., `whoami` or `cat /etc/passwd`) and receiving security rejection. | `whoami` in `client.py` | [ ] Pending VM Run |
| **Figure 13** | **Loopback Packet Capture (`tcpdump`)** | Terminal showing `tcpdump` capturing ASCII commands and responses on interface `lo` over TCP port 54321. | `sudo tcpdump -i lo -nnvv -X port 54321` | [ ] Pending VM Run |
| **Figure 14** | **Cryptographic Hash Verification** | Terminal displaying `sha256sum`, `sha1sum`, and `md5sum` hashes for `server.py` and `client.py`. | `sha256sum lab/safe_shell_simulation/*.py` | [ ] Pending VM Run |
| **Figure 15** | **VirusTotal Hash-Based Lookup** | Web browser showing VirusTotal search result for SHA-256 hash returning "No results found" (clean/unindexed). | Browser window at `virustotal.com/gui/search/<SHA256>` | [ ] Pending VM Run |
| **Figure 16** | **Post-Recovery Audit Verification** | Terminal after restoring `NPC_Capstone_Clean_State` showing `ss -tulpn` and `ps aux` confirming port 54321 is closed. | `sudo ss -tulpn \| grep 54321 && ps aux \| grep server` | [ ] Pending VM Run |

---

## 3. Image Formatting & PDF Compilation Notes

- **Format:** High-resolution PNG (`.png`) images.
- **Resolution:** Recommended minimum 1280x720 or 1920x1080 for sharp text legibility.
- **Placement:** Store raw files in `evidence/screenshots/`.
- Once captured, running `python generate_pdf.py` will automatically embed the real images in place of the bounding box placeholders in Appendix A of the final academic PDF report.
