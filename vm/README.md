# Virtual Machine Configuration & Deployment Manifest

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Academic Year:** 2026–2027  

---

## 1. Virtual Machine Profile

This directory contains specifications and configuration guides for deploying the Linux dynamic malware analysis sandbox:

| Attribute | Deployment Specification |
|---|---|
| **VM Identifier** | `NPC_Capstone_Malware_Sandbox` |
| **Target Hypervisor** | Oracle VM VirtualBox (v7.0+) or VMware Workstation Pro/Player (v17+) |
| **Guest Operating System** | Ubuntu 24.04 LTS (Noble Numbat) 64-bit or Debian 12 (Bookworm) 64-bit |
| **vCPU Allocation** | 2 Processors (Execution Cap 100%) |
| **RAM Allocation** | 4096 MB (4.0 GB) |
| **Storage Controller** | SATA Controller / AHCI |
| **Virtual Disk Size** | 30.00 GB Dynamically Allocated VDI / VMDK |
| **Display Controller** | VMSVGA (3D Acceleration Disabled) |
| **Network Adapter 1** | Host-Only (`vboxnet0` / `VMnet1`) with Cable Disconnected |
| **Clean Snapshot Name** | `NPC_Capstone_Clean_State` |

---

## 2. Hardening Protocols for Malware Analysis

To prevent sandbox evasion and host leakage:
1. **Disable Shared Clipboard:** Ensure Host-to-Guest and Guest-to-Host clipboard sharing is Disabled.
2. **Disable Drag and Drop:** Ensure file transfer drag-and-drop is Disabled.
3. **No Shared Folders:** Remove all host shared directories.
4. **Isolate Network:** Ensure no Bridged or NAT adapter is attached during malware execution.
5. **Freeze Baseline:** Take snapshot `NPC_Capstone_Clean_State` immediately after installing diagnostic tools.
