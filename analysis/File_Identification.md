# Static File Identification & Artifact Characteristics

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Static Identification Methodology

Static analysis forms the initial triage phase of any malware investigation. Before executing code in a sandboxed virtual machine, an analyst must determine the artifact's file type, target architecture, encoding format, and structural composition without executing a single instruction.

---

## 2. Linux Utility Findings

### 2.1 File Command Output (`file`)
The standard POSIX `file` utility inspects magic bytes and header structures:

```bash
file lab/safe_shell_simulation/server.py
```
*Output:*
```text
lab/safe_shell_simulation/server.py: Python script, Unicode text, UTF-8 text executable, with CRLF line terminators
```

```bash
file lab/safe_shell_simulation/client.py
```
*Output:*
```text
lab/safe_shell_simulation/client.py: Python script, Unicode text, UTF-8 text executable, with CRLF line terminators
```

### 2.2 File System Metadata (`stat`)
Detailed file system inode properties collected on the laboratory system:

#### `server.py`:
- **Size:** 10,337 bytes
- **Blocks:** 24 / IO Block: 4096 bytes
- **File Type:** Regular file
- **Permissions:** `0644` / `rw-r--r--` (or `0755` / `rwxr-xr-x` when marked executable)
- **Programming Language:** Python 3 (interpreted script)

#### `client.py`:
- **Size:** 4,759 bytes
- **Blocks:** 16 / IO Block: 4096 bytes
- **File Type:** Regular file
- **Permissions:** `0644` / `rw-r--r--`
- **Programming Language:** Python 3 (interpreted script)

---

## 3. Heuristic & Static Code Audit

In contrast to commercial malware specimens that utilize packing, encryption, string obfuscation, and anti-disassembly techniques, static examination of `server.py` reveals:

1. **Obfuscation Status:** **None**. The code is completely human-readable UTF-8 source text.
2. **Entropy Evaluation:** Low entropy (~4.8 bits/byte), consistent with standard source code containing English documentation strings and comments (packed or encrypted malware typically exhibits Shannon entropy > 7.2 bits/byte).
3. **Suspicious API References:** **Zero**. Audit confirmed complete absence of dangerous API calls:
   - No `os.system`
   - No `subprocess.Popen` / `subprocess.run` / `subprocess.call`
   - No `eval` or `exec`
   - No `ctypes` or `win32api`
   - No `pty.spawn` or `dup2`
   - No raw socket packet crafting (`SOCK_RAW`)
4. **Network Surface:** Restricted exclusively to `AF_INET` / `SOCK_STREAM` with hardcoded binding to `127.0.0.1:54321`.

---

## 4. Conclusion of Static Analysis

The artifact is definitively identified as an uncompiled, un-obfuscated, educational Python 3 socket script designed solely for local diagnostic observation. It poses zero danger of host compromise, lateral propagation, or external communication.
