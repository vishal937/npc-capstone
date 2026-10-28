# Linux System Monitoring & Forensic Triage Guide

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Principles of Live System Monitoring in Malware Sandboxes

Dynamic analysis requires active observation of an operating system across four core forensic dimensions:
1. **Process Activity:** Creation, hierarchy, UID/GID credentials, arguments, and memory consumption.
2. **Network Activity:** Socket creation, protocol bindings, local and foreign IP:port pairs, and connection states (`LISTEN`, `ESTABLISHED`, `TIME_WAIT`).
3. **File System Activity:** Inode creation, file modification timestamps (`mtime`, `ctime`, `atime`), and open file descriptors.
4. **Log & Kernel Events:** Operating system audit records, authentication attempts, and system daemon log outputs.

---

## 2. Process Monitoring Suite

### 2.1 Process Snapshot (`ps aux`)
Inspect all running processes with user attribution:
```bash
ps aux | grep -E "python3|server.py|client.py" | grep -v grep
```
*Sample Output Interpretation:*
```text
student   4521  0.0  0.4  28340  8912 pts/0    S+   21:50   0:00 python3 lab/safe_shell_simulation/server.py
```
- `student`: The unprivileged user account executing the process.
- `4521`: The unique Process ID (PID).
- `0.0 / 0.4`: Percentage of CPU and RAM consumed.
- `pts/0`: Pseudo-terminal slave from which the process was initiated.
- `S+`: Process status (Interruptible sleep, foreground process group).

### 2.2 Process Tree Hierarchy (`pstree -p`)
Visualize the ancestry of the running simulation:
```bash
pstree -p $(pgrep -f "server.py")
```
*Expected Hierarchy:*
```text
bash(4102)───python3(4521)
```
Confirms that the python process is a direct child of the interactive bash shell without any rogue daemonization, double-forking, or orphaned reparenting to `systemd` (PID 1).

### 2.3 Interactive Resource Monitor (`top` / `htop`)
Monitor CPU and memory overhead during client command transactions:
```bash
top -p $(pgrep -f "server.py")
```

---

## 3. Network & Socket Monitoring Suite

### 3.1 Socket Statistics (`ss`)
The modern replacement for `netstat`, querying socket information directly from Linux kernel netlink:
```bash
sudo ss -tulpn | grep 54321
```
*Flags:*
- `-t`: TCP sockets.
- `-u`: UDP sockets.
- `-l`: Sockets in `LISTEN` state.
- `-p`: Show process name and PID owning the socket.
- `-n`: Numeric port and address display.

*Output During Idle Listener State:*
```text
tcp   LISTEN 0      5      127.0.0.1:54321      0.0.0.0:*    users:(("python3",pid=4521,fd=3))
```
- `127.0.0.1:54321`: Binds strictly to loopback interface.
- `users:(("python3",pid=4521,fd=3))`: Confirms PID 4521 holds socket descriptor `3`.

*Output During Active Client Connection:*
```bash
sudo ss -tan | grep 54321
```
```text
LISTEN      0      5          127.0.0.1:54321      0.0.0.0:*
ESTAB       0      0          127.0.0.1:54321      127.0.0.1:49214
ESTAB       0      0          127.0.0.1:49214      127.0.0.1:54321
```
Demonstrates an active bidirectional TCP connection between listener port `54321` and client ephemeral port `49214`.

### 3.2 List Open Files on Network Port (`lsof`)
```bash
sudo lsof -i :54321
```
*Output:*
```text
COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  4521 student    3u  IPv4  38914      0t0  TCP 127.0.0.1:54321 (LISTEN)
python3  4521 student    4u  IPv4  39120      0t0  TCP 127.0.0.1:54321->127.0.0.1:49214 (ESTABLISHED)
python3  4610 student    3u  IPv4  39119      0t0  TCP 127.0.0.1:49214->127.0.0.1:54321 (ESTABLISHED)
```

---

## 4. File System & Integrity Auditing Suite

### 4.1 Inode & Timestamp Audit (`stat`)
Inspect precise access, modification, and metadata change timestamps:
```bash
stat lab/safe_shell_simulation/server.py
```
*Sample Output:*
```text
  File: lab/safe_shell_simulation/server.py
  Size: 10337     	Blocks: 24         IO Block: 4096   regular file
Device: 0801h/2049d	Inode: 1572948     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/ student)   Gid: ( 1000/ student)
Access: 2026-10-28 21:50:15.000000000 +0530
Modify: 2026-10-28 21:51:03.000000000 +0530
Change: 2026-10-28 21:51:03.000000000 +0530
 Birth: 2026-10-28 21:51:03.000000000 +0530
```

### 4.2 Temporary File Discovery (`find`)
Detect any unauthorized files created within the last 15 minutes across system directories:
```bash
sudo find /tmp /var/tmp /dev/shm -mmin -15 -type f
```

### 4.3 Cryptographic Integrity (`sha256sum`)
Verify hash consistency against known baselines:
```bash
sha256sum lab/safe_shell_simulation/server.py
```

---

## 5. System Event & Journal Logging

Inspect system daemon logs for anomalous socket creation or privilege escalation attempts:
```bash
# View recent system messages
sudo journalctl -n 50 --no-pager

# Check authentication and sudo logs
sudo grep -i "sudo" /var/log/auth.log | tail -n 20
```

---

## 6. Live Forensic Triage Checklist

| Phase | Diagnostic Tool | Target Metric | Expected Safe Baseline |
|---|---|---|---|
| **Pre-Execution** | `ss -tulpn` | Listening Ports | Port 54321 is **CLOSED** |
| **Pre-Execution** | `ps aux` | Process Table | Zero simulation processes active |
| **Active Execution** | `ss -tulpn` | Listening Ports | `127.0.0.1:54321` in `LISTEN` state |
| **Active Execution** | `ps aux` | Process Table | Single unprivileged `python3` process |
| **Active Execution** | `tcpdump` | Loopback Traffic | Clean TCP handshake and formatted ASCII exchanges |
| **Post-Restoration** | `ss -tulpn` | Listening Ports | Port 54321 is **CLOSED** |
| **Post-Restoration** | `ps aux` | Process Table | Zero simulation processes active |
