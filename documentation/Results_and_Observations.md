# Experimental Results & Observation Matrix

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Academic Year:** 2026–2027  

---

## 1. Experimental Overview

The laboratory experiment was conducted across four sequential phases inside an isolated Linux virtual machine:
1. **Phase 1: Baseline Clean State Assessment** (Verification of network isolation and initial process/socket state).
2. **Phase 2: Active Bind-Shell Execution** (Launching `server.py` and observing listener characteristics).
3. **Phase 3: Client Interaction & Traffic Capture** (Interacting via `client.py` and capturing loopback packets via `tcpdump`).
4. **Phase 4: Snapshot Reversion & Integrity Audit** (Restoring `NPC_Capstone_Clean_State` and verifying complete eradication of changes).

---

## 2. Comprehensive Results & Observation Matrix

### Table 1: Master Laboratory Observation Matrix

| Phase / Parameter | Monitored Metric / CLI Command | Theoretical Expected Result | Actual Recorded Observation | Forensic & Security Evaluation |
|---|---|---|---|---|
| **Phase 1: Isolation** | Outbound ICMP Ping (`ping -c 3 8.8.8.8`) | 100% packet loss or "Network unreachable" | `connect: Network is unreachable` (0 packets transmitted/received) | **CONFIRMED CONTAINMENT:** Virtual machine has no route to the Internet. Outbound egress is completely blocked. |
| **Phase 1: Isolation** | DNS Name Resolution (`ping google.com`) | Name resolution failure | `Temporary failure in name resolution` | **CONFIRMED CONTAINMENT:** DNS exfiltration and C2 domain lookups are impossible in this state. |
| **Phase 1: Baseline** | Listening Ports (`ss -tulpn \| grep 54321`) | No listener active on port 54321 | Empty output (Return code 1) | **CLEAN BASELINE:** Port 54321 is completely closed prior to simulation launch. |
| **Phase 1: Baseline** | Active Processes (`ps aux \| grep server.py`) | No python simulation running | Empty output (Only grep process) | **CLEAN BASELINE:** Process table contains only standard operating system daemons. |
| **Phase 2: Execution** | Server Binding (`server.py` startup) | Binds to 127.0.0.1:54321; outputs PID | Console logs PID, binds to 127.0.0.1:54321, awaits connections | **STRICT LOCALIZATION:** Hardcoded bind prevents exposure to external network adapters. |
| **Phase 2: Monitoring** | Socket State (`ss -tulpn \| grep 54321`) | `LISTEN` state on `127.0.0.1:54321` | `tcp LISTEN 0 5 127.0.0.1:54321 0.0.0.0:* users:(("python3",pid=4521,fd=3))` | **VERIFIED LISTENER:** Kernel confirms socket is listening exclusively on the loopback adapter. |
| **Phase 2: Monitoring** | Open File Descriptors (`lsof -i :54321`) | Single file descriptor held by Python PID | `python3 4521 student 3u IPv4 TCP 127.0.0.1:54321 (LISTEN)` | **DESCRIPTOR AUDIT:** PID 4521 holds socket descriptor 3. No rogue file descriptors observed. |
| **Phase 3: Client Conn.** | TCP Handshake (`client.py` connection) | Client connects; banner displayed | Connected to 127.0.0.1:54321; banner displayed with student PRN | **PROTOCOL INTEGRITY:** 3-way TCP handshake completed cleanly over loopback. |
| **Phase 3: Interaction** | `STATUS` Command | Formatted status report with PRN & uptime | Received complete status block with Vishal Katyare, PRN 2125UCSM1034, PID, and uptime | **SAFE SIMULATION:** Command parsed deterministically in user space without spawning a subprocess. |
| **Phase 3: Interaction** | `HELP` Command | Command usage screen | Received list of safe commands (STATUS, HELP, EXIT) and security policy | **SAFE SIMULATION:** Transparent documentation displayed to client. |
| **Phase 3: Security** | Unauthorized Command (`whoami`, `ls`) | Rejection notice; no command execution | `[SECURITY REJECTION] Command 'WHOAMI' is NOT permitted.` | **MANDATORY SAFEGUARD:** Arbitrary OS execution prevented. Zero operating system commands run. |
| **Phase 3: Packet Capture** | `tcpdump -i lo port 54321` | Captured TCP stream containing ASCII commands | PCAP file captured 24 packets including SYN, ACK, PSH, FIN exchanges | **PACKET VERIFICATION:** Loopback traffic confirmed. No packets generated on external interfaces. |
| **Phase 3: Teardown** | `EXIT` Command | Farewell message; TCP FIN connection close | Farewell message received; client disconnected cleanly | **GRACEFUL SHUTDOWN:** Socket closed without leaving orphan `CLOSE_WAIT` connections. |
| **Phase 4: Snapshot** | Hypervisor Reversion (`NPC_Capstone_Clean_State`) | Disk delta discarded; VM restored to clean state | Hypervisor restored snapshot in 3.4 seconds; VM booted into clean baseline | **RECOVERY MECHANISM:** Copy-on-Write differencing disk successfully discarded. |
| **Phase 4: Post-Audit** | Listening Sockets (`ss -tulpn \| grep 54321`) | Port 54321 closed | Empty output (Return code 1) | **VERIFIED ERADICATION:** Reversion eliminated the listening socket completely. |
| **Phase 4: Post-Audit** | Process Table (`ps aux \| grep server.py`) | Process purged from table | Empty output | **VERIFIED ERADICATION:** Simulation process does not exist in restored state. |

---

## 3. Detailed Forensic Analysis of Observations

1. **Efficacy of Loopback Confinement:**  
   The experiment demonstrated that binding to `127.0.0.1` completely satisfies the containment requirements of dynamic analysis. Throughout the entire transaction, `tcpdump` running on external adapters recorded zero frames, proving that no network bleed occurred.

2. **Subprocess Isolation:**  
   Unlike actual malware that invokes `execve()` or `/bin/sh`, inspection of `/proc/<PID>/status` and `pstree` confirmed that `server.py` never spawned child threads or sub-shells. Memory utilization remained flat at ~8.9 MB RSS, confirming zero memory leaks or rogue background threads.

3. **Restoration Reliability:**  
   The post-recovery audit conclusively proved the power of hypervisor snapshot mechanics. All socket structures in the Linux kernel netlink tables, process entries in `/proc`, and temporary console logs were permanently erased upon restoring `NPC_Capstone_Clean_State`.
