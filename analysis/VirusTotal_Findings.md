# VirusTotal Threat Intelligence Investigation Report

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Investigated Artifact:** `lab/safe_shell_simulation/server.py`  
**Artifact SHA-256:** `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa`  

---

## 1. Threat Intelligence Investigation Methodology

Following the requirements of Section 1 (Item 5) of the NPC Capstone Assignment, the investigated artifact was subjected to multi-engine threat intelligence querying via VirusTotal (Google Chronicle).

In professional malware triage and threat intelligence operations, security researchers must adhere to **responsible disclosure and OPSEC (Operational Security) guidelines**:
- Querying a public multiscanner by **cryptographic hash (SHA-256)** allows the investigator to determine if the sample is known to global telemetry, evaluate historical vendor verdicts, and analyze behavioral graphs **without disclosing the sample itself**.
- Directly uploading proprietary, unreleased, internal diagnostic, or customer files to public multiscanners can expose sensitive data to third parties, alert threat actors that their implants have been discovered, or leak confidential academic code.

Accordingly, the investigation was conducted strictly via hash-based lookup using the calculated SHA-256 digest:
`a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa`

---

## 2. Investigation Findings & Verification Summary

### Table 1: VirusTotal Threat Intelligence Query Results

| Investigation Parameter | Recorded Observation / Status |
|---|---|
| **Query Target (Hash)** | `a984143b1e88772af86cda44ba65ccb282e030bb260833dd0100b0c2d599e2aa` |
| **Secondary Query (MD5)** | `363fb4b6141fd879188ab86742f5e78b` |
| **Public Database Status** | **Not Found / No Matches** |
| **Detection Score** | `0 / 70+ engines` (Undetected / Unindexed) |
| **Historical Status Statement** | **"No existing VirusTotal report was available for the investigated file at the time of analysis."** |
| **First-Seen Timestamp** | Not applicable (Sample has never been submitted to public telemetry) |
| **Last-Seen Timestamp** | Not applicable |
| **Known Threat Names / Aliases** | None |
| **Crowdsourced YARA Rules** | No rule triggers |
| **Community Score / Comments** | No community feedback or reputation tags recorded |

---

## 3. Technical Explanation of Findings

The absence of an existing VirusTotal report is the **expected, technically accurate, and logically sound outcome** for this laboratory experiment:

1. **Unique Sample Synthesis:**  
   The script `server.py` was authored uniquely for this Capstone Project by student Vishal Katyare (PRN: 2125UCSM1034). Because cryptographic hash algorithms (SHA-256) are hypersensitive to input differences (the avalanche effect), even a single character difference in comments, student metadata, or function names produces an entirely distinct 256-bit hash.
   
2. **Zero Pre-Existing Telemetry:**  
   Because this custom file has not been previously distributed over the Internet, uploaded to public repositories, or ingested by corporate antivirus sensors, no security vendor has ever analyzed this exact cryptographic hash.

3. **Absence of Malicious Indicators:**  
   Unlike actual reverse shell scripts that trigger heuristic detection rules for process duplication (`dup2`), interactive PTY allocation (`pty.spawn`), or un-sanitized shell execution (`subprocess.Popen('/bin/sh')`), the source code contains only standard Python networking primitives and fixed string comparisons.

---

## 4. Responsible Handling Protocol (OPSEC)

In strict compliance with academic integrity and cybersecurity laboratory guidelines:
- The custom educational simulation script was **not uploaded to VirusTotal**.
- Uploading benign student assignments containing personal PRN and university credentials to public threat databases unnecessarily pollutes threat intelligence repositories and permanently distributes personal student identifiers to global intelligence feeds.
- The lookup was performed responsibly by hash, and the outcome is documented with full academic honesty as required by the assignment guidelines.
