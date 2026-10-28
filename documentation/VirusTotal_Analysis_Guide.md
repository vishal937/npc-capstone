# VirusTotal & Threat Intelligence Analysis Guide

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Role of Multiscanners in Threat Intelligence

In modern security operations centers (SOCs) and computer incident response teams (CIRTs), multiscanners like **VirusTotal** (a subsidiary of Google Chronicle) aggregate over 70 leading antivirus engines, dynamic behavioral sandboxes, and crowdsourced YARA rule engines.

When an analyst encounters a suspicious file or binary during an incident, querying a multiscanner provides:
1. **Consensus Threat Verdict:** Eliminating individual engine false positives and false negatives by evaluating detections across CrowdStrike, Microsoft Defender, Kaspersky, Sophos, ESET, and dozens of others.
2. **First-Seen / Last-Seen Chronology:** Establishing when a specific malware campaign was first observed globally.
3. **Associated Indicators of Compromise (IoCs):** Correlating cryptographic hashes with command-and-control (C2) domains, IP addresses, mutexes, and registry artifacts.

---

## 2. OPSEC: Hash-Based Lookup vs. Raw Sample Upload

A critical competency for cybersecurity students is understanding **Operational Security (OPSEC)** when interacting with public threat intelligence platforms.

### The Dangers of Uploading Raw Samples:
1. **Exposure of Proprietary / Confidential Data:**  
   When a file is uploaded to VirusTotal, it is distributed to hundreds of premium intelligence subscribers (including security researchers, vendors, enterprise SOCs, and government agencies). If the file contains proprietary business logic, hardcoded API tokens, student credentials, or personal identification data (such as a student's PRN), that information becomes permanently accessible worldwide.
2. **Tipping Off the Adversary:**  
   Advanced threat actors (APTs) actively monitor public multiscanner feeds. If a custom implant used in a targeted intrusion is uploaded, the threat actor receives immediate notification that their operation is compromised, prompting them to change C2 infrastructure, wipe evidence, or activate anti-forensic triggers before investigators complete their analysis.
3. **Repository Pollution:**  
   Submitting benign student programming assignments clutters threat repositories with non-threat specimens.

### The Professional Protocol: Hash-Based Lookups
Security engineers **always calculate the cryptographic hash (SHA-256) locally first**, and query VirusTotal exclusively by that hash digest:
- **API / Web Hash Query:** Transmits only the 64-character hexadecimal digest.
- **Privacy Guarantee:** The internal code, strings, credentials, and structural data are never transmitted to external servers.
- **Verdict Availability:** If the sample has been analyzed previously by anyone globally, the full intelligence report is retrieved immediately. If the sample is unknown, the platform simply reports "No matches found".

---

## 3. Threat Intelligence Search Workflow

### Step 1: Calculate Local SHA-256 Digest
On the host or inside the VM:
```bash
sha256sum lab/safe_shell_simulation/server.py
```
*Calculated Digest:*
`a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa`

### Step 2: Query Public Threat Intelligence
1. Open a secure browser on the host machine.
2. Navigate to `https://www.virustotal.com/gui/home/search`.
3. Paste the SHA-256 digest into the search bar and press **Enter**.
4. Observe the result screen.

### Step 3: Interpreting the Result
For `server.py`, VirusTotal returns:
> **"No results found for a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa"**

As required by academic integrity and laboratory guidelines, the student accurately documents:
> **"No existing VirusTotal report was available for the investigated file at the time of analysis."**

---

## 4. Analysis of Detection Engine Methodologies

Understanding how antivirus engines categorize files when a sample *is* scanned:

| Engine Detection Category | Analysis Technique | Mechanism |
|---|---|---|
| **Signature-Based Detection** | Static Pattern Matching | Matches byte sequences, MD5/SHA-256 hashes against known malware databases |
| **Heuristic Detection** | Static Rule Heuristics | Analyzes structural anomalies, suspicious imported APIs (`VirtualAllocEx`, `WriteProcessMemory`), and section entropy |
| **Machine Learning / AI** | Feature Vector Classification | Compares binary characteristics against neural network models trained on benign and malicious corpora |
| **YARA Rule Matching** | Pattern & Condition Sets | Scans for specific textual strings, regular expressions, or cryptographic constants |
| **Dynamic Sandbox Analysis** | Emulated / Bare-Metal Execution | Monitors runtime API calls, process injection, network beaconing, and registry modifications |

Because our laboratory artifact is a benign, newly authored Python script containing no malicious APIs or known malware signatures, it naturally exhibits zero detections across all analysis modalities.
