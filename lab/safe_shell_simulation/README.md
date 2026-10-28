# Safe Shell Simulation — Architecture & Security Blueprint

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Executive Summary & Purpose

In dynamic malware analysis, understanding the runtime network indicators and process characteristics of command-and-control (C2) listeners, bind shells, and reverse shells is essential. However, executing actual malicious backdoors in an educational context introduces severe risks of accidental network propagation, unauthorized remote code execution, host system compromise, and compliance violations.

To fulfill the curriculum requirements of the **NPC Capstone Project** with absolute safety, this component provides a **deterministic, local-only bind-shell simulation** implemented in Python (`server.py` and `client.py`). This implementation allows the student to observe realistic operating system socket behavior, process creation, listening state transitions, packet generation, and snapshot recovery without any capability of executing arbitrary system commands or escaping the laboratory environment.

---

## 2. Technical Comparison: Malicious Shell vs. Safe Simulation

The table below delineates the strict architectural divergence between a dangerous real-world bind shell and this safe educational simulation:

| Architectural Property | Real Malicious Bind/Reverse Shell | NPC Capstone Safe Simulation (`server.py`) |
|---|---|---|
| **Network Interface Binding** | Binds to `0.0.0.0` (all interfaces) or bridges to public WAN | Strictly hardcoded to `127.0.0.1` (loopback only) |
| **Command Execution Mechanism** | Spawns `/bin/sh`, `/bin/bash`, or `cmd.exe` via `execve()` / `CreateProcess()` | **Zero subprocess spawning**. No `os.system()`, `subprocess`, `eval()`, or `exec()` |
| **I/O Redirection** | Duplicates socket file descriptor to `stdin`, `stdout`, `stderr` via `dup2()` | Standard user-space string parsing and formatted reply generation |
| **Permitted Commands** | Arbitrary operating system commands with full privileges | Restricted to **three predefined safe keywords**: `STATUS`, `HELP`, `EXIT` |
| **Arbitrary Input Handling** | Executes malicious instructions directly on the target host | Explicitly rejects unknown commands with an audit warning string |
| **Persistence Mechanisms** | Modifies cron jobs, registry keys, systemd units, bashrc | **Zero persistence**. Ephemeral process terminated immediately upon SIGINT/SIGTERM |
| **Evasion & Stealth** | Hooks APIs, injects into legitimate processes, unlinks binaries | Plain, un-obfuscated script displaying student name and PRN upon connection |
| **Containment Guarantee** | High risk of lateral movement if hypervisor isolation fails | Inherent host-level containment even in the event of hypervisor misconfiguration |

---

## 3. Communication Protocol Specification

The safe simulation implements a structured ASCII text protocol over TCP port `54321`:

### 3.1 Initial Handshake
Upon successful three-way TCP handshake (`SYN` -> `SYN-ACK` -> `ACK`), the server delivers a formal banner identifying the session:

```text
****************************************************
* NPC Capstone: Safe Shell Simulation (127.0.0.1)   *
* Student: Vishal Katyare | PRN: 2125UCSM1034       *
* Department: Computer Science Engineering (CS)     *
* Commands: STATUS, HELP, EXIT                      *
****************************************************
NPC_SHELL> 
```

### 3.2 Supported Commands

1. **`STATUS`**
   - **Request:** `STATUS\n`
   - **Response:** Formatted block providing the Student Name, PRN, University, Server PID, Binding Interface (`127.0.0.1:54321`), Server Uptime, and Confirmation of Safe Simulation Mode.
   - **Connection State:** Remains open.

2. **`HELP`**
   - **Request:** `HELP\n`
   - **Response:** Documentation of authorized commands and educational safety notice.
   - **Connection State:** Remains open.

3. **`EXIT`**
   - **Request:** `EXIT\n`
   - **Response:** Formal termination message followed by graceful TCP FIN disconnection.
   - **Connection State:** Closed.

4. **Arbitrary / Unauthorized Input (e.g., `whoami`, `cat /etc/passwd`, `id`)**
   - **Request:** Any string not matching `STATUS`, `HELP`, or `EXIT`.
   - **Response:** `[SECURITY REJECTION] Command '<INPUT>' is NOT permitted. This simulation strictly prohibits arbitrary command execution.`
   - **Connection State:** Remains open, logging a security alert to the server console.

---

## 4. Laboratory Execution Workflow

### Step 1: Start the Server (Terminal 1)
In the virtual machine terminal, launch the server:
```bash
python3 lab/safe_shell_simulation/server.py
```
*Expected Console Output:*
```text
[2026-10-28 21:50:00] [SAFE_SERVER] NPC Capstone: Safe Bind-Shell Simulation Initialized
[2026-10-28 21:50:00] [SAFE_SERVER] Student: Vishal Katyare | PRN: 2125UCSM1034
[2026-10-28 21:50:00] [SAFE_SERVER] Bound to: 127.0.0.1:54321 (Strict Loopback Only)
[2026-10-28 21:50:00] [SAFE_SERVER] Process PID: 4521
[2026-10-28 21:50:00] [SAFE_SERVER] Awaiting local client connections... (Press Ctrl+C to terminate)
```

### Step 2: Verify Process and Socket Binding (Terminal 2)
Verify that the listener is active exclusively on the loopback adapter:
```bash
# Socket verification
ss -tulpn | grep 54321

# Process verification
ps aux | grep server.py

# File descriptor verification
lsof -i :54321
```

### Step 3: Run the Safe Client (Terminal 2)
Connect to the listener using the provided test client:
```bash
python3 lab/safe_shell_simulation/client.py
```
Interact by typing `STATUS`, `HELP`, testing an unauthorized command like `whoami` to verify security rejection, and concluding with `EXIT`.

### Step 4: Verification via Standard Utility (Alternative)
The simulation can also be verified using the standard netcat utility:
```bash
nc 127.0.0.1 54321
```

---

## 5. Security & Containment Verification Checklist

- [x] Server hardcoded to `127.0.0.1` (`AF_INET`).
- [x] Code audited for zero occurrences of `os.system`, `subprocess.Popen`, `subprocess.run`, `eval`, or `exec`.
- [x] Graceful termination on `SIGINT` (Ctrl+C) and `SIGTERM`.
- [x] No persistent files, registry keys, or scheduled tasks created.
- [x] Comprehensive error handling preventing uncaught exception crashes.
