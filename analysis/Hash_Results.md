# Cryptographic Hash Results & Integrity Verification

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Academic Year:** 2026–2027  

---

## 1. Overview & Forensic Significance of Hashing

In malware analysis and forensic investigations, cryptographic hashing generates fixed-length mathematical digests from arbitrary input data. Cryptographic hashes serve three fundamental operational functions:
1. **Sample Identification:** Enabling unique indexing across malware repositories and threat intelligence platforms without revealing proprietary content.
2. **Chain of Custody & Integrity Assurance:** Proving conclusively that an evidence file or laboratory script has not been altered, corrupted, or tampered with throughout the analysis lifecycle.
3. **Threat Intelligence Correlation:** Allowing analysts to query multi-engine scanners (such as VirusTotal, AlienVault OTX, and MISP) using non-sensitive hashes rather than uploading confidential binaries.

---

## 2. Calculated Cryptographic Hashes

The files investigated in this project were hashed using the standard NIST-approved hashing algorithms: MD5 (RFC 1321), SHA-1 (FIPS PUB 180-4), and SHA-256 (FIPS PUB 180-4).

### Table 1: Primary Laboratory Artifacts Hash Registry

| Parameter | Laboratory Target 1 (`server.py`) | Laboratory Target 2 (`client.py`) |
|---|---|---|
| **File Name** | `server.py` | `client.py` |
| **Relative Path** | `lab/safe_shell_simulation/server.py` | `lab/safe_shell_simulation/client.py` |
| **File Description** | Safe Loopback Bind-Shell Server | Interactive Local Test Client |
| **File Size (Bytes)** | 10,337 bytes | 4,759 bytes |
| **MIME Type** | `text/x-python` (UTF-8 source text) | `text/x-python` (UTF-8 source text) |
| **MD5 Digest** | `363fb4b6141fd879188ab86742f5e78b` | `132c47a87200232d07ff7be0c4b74d81` |
| **SHA-1 Digest** | `0d0c8b3f0ea0956a061aaa850f56c5c4b8c716c6` | `eabb5aeb3238f69b3b2b9b48b1a20b5128602cb1` |
| **SHA-256 Digest** | `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa` | `d5d37de3e4b02a148ba382809ebcea844f213a8498510e772838ba269c15598a` |

---

## 3. Hash Generation Commands (Linux VM & Host Verification)

To independently verify these cryptographic hashes inside the Linux guest or on any POSIX-compliant host, execute the following commands:

### SHA-256 Verification:
```bash
sha256sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
```
*Expected Linux Standard Output:*
```text
a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa  lab/safe_shell_simulation/server.py
d5d37de3e4b02a148ba382809ebcea844f213a8498510e772838ba269c15598a  lab/safe_shell_simulation/client.py
```

### SHA-1 Verification:
```bash
sha1sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
```
*Expected Linux Standard Output:*
```text
0d0c8b3f0ea0956a061aaa850f56c5c4b8c716c6  lab/safe_shell_simulation/server.py
eabb5aeb3238f69b3b2b9b48b1a20b5128602cb1  lab/safe_shell_simulation/client.py
```

### MD5 Verification:
```bash
md5sum lab/safe_shell_simulation/server.py lab/safe_shell_simulation/client.py
```
*Expected Linux Standard Output:*
```text
363fb4b6141fd879188ab86742f5e78b  lab/safe_shell_simulation/server.py
132c47a87200232d07ff7be0c4b74d81  lab/safe_shell_simulation/client.py
```

---

## 4. Integrity Assertion

The SHA-256 digest `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa` uniquely identifies the safe server demonstration created specifically for Vishal Katyare (PRN: 2125UCSM1034). Any byte-level modification to comments, logic, or formatting will produce a completely different SHA-256 digest due to the cryptographic avalanche effect.
