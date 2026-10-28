# Virtual Machine Laboratory Setup & Hardening Guide

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  
**Academic Year:** 2026–2027  

---

## 1. Laboratory Overview & Hardware Specifications

Dynamic malware analysis necessitates a resilient, isolated virtualization sandbox that prevents any accidental guest-to-host or guest-to-LAN communication while providing granular visibility into process, socket, and memory behaviors.

This guide provides exhaustive provisioning procedures for both **Oracle VM VirtualBox** and **VMware Workstation Pro / Player**, including hardware resource allocations, guest OS configuration, hypervisor security hardening, and snapshot creation.

### Recommended Virtual Machine Hardware Profile

| Hardware Parameter | Minimum Requirement | Recommended Specification | Rationale in Sandbox Analysis |
|---|---|---|---|
| **Guest OS** | Ubuntu 22.04 LTS (64-bit) | Ubuntu 24.04 LTS / Debian 12 (64-bit) | Modern Linux kernel with full `eBPF`, `systemd`, `iproute2`, and `auditd` support |
| **Virtual CPUs (vCPUs)** | 1 Core | 2 Cores | Ensures fluid multiprocess scheduling and avoids artificial CPU starvation during live monitoring |
| **RAM (Memory)** | 2048 MB (2 GB) | 4096 MB (4 GB) | Accommodates in-memory packet buffering (`tcpdump`), kernel buffers, and terminal logging |
| **Virtual Storage** | 20 GB (Dynamically Allocated) | 30 GB (Dynamically Allocated VDI/VMDK) | Provides sufficient headroom for OS packages, debugging tools, and copy-on-write delta snapshots |
| **Graphics Controller** | Default (VMSVGA) | VMSVGA (3D Acceleration Disabled) | Mitigates potential hypervisor GPU driver escape vulnerabilities (CVE-2019-15693, etc.) |
| **Network Adapter** | Disabled or Host-Only | Host-Only / Isolated Loopback | Prevents unauthorized egress traffic to the physical local area network or the Internet |

---

## 2. Hypervisor Network Isolation Modes: Comparative Analysis

Configuring the virtual network adapter correctly is the most critical operational security decision in sandbox design. A single misconfiguration (e.g., leaving an interface in Bridged mode) can result in live malware propagating onto corporate subnets, triggering IDS/IPS alerts, or communicating with active threat actor infrastructure.

### Table 1: Comprehensive Comparison of Hypervisor Networking Modes

| Network Mode | VM-to-Host Comm. | VM-to-LAN Comm. | VM-to-Internet Access | Risk Level in Malware Sandbox | Recommended Use in This Lab |
|---|---|---|---|---|---|
| **Bridged Adapter** | Yes (Direct LAN peer) | **Yes (Full access)** | **Yes (Direct routing)** | **CRITICAL / EXTREME DANGER**<br>Guest acts as a physical node on LAN. Malware can scan, exploit, and infect LAN devices. | **STRICTLY PROHIBITED** |
| **NAT (Network Address Translation)** | Host inaccessible directly | No (Masked behind host IP) | **Yes (Outbound egress allowed)** | **HIGH RISK**<br>VM can initiate outbound TCP/UDP connections to external C2 servers and download secondary payloads. | **STRICTLY PROHIBITED** |
| **NAT Network** | Isolated from LAN | No | **Yes (Outbound egress allowed)** | **HIGH RISK**<br>Similar to NAT; enables multi-VM communication but allows external Internet access. | **STRICTLY PROHIBITED** |
| **Host-Only Adapter** | Yes (Via private virtual subnet) | No | **No (Isolated from WAN)** | **LOW TO MODERATE**<br>Traffic restricted to host virtual adapter. Host OS services must be protected against probing. | **PERMITTED (Controlled)** |
| **Internal Network** (VirtualBox) / **LAN Segment** (VMware) | No | No | **No (Completely isolated)** | **LOW / SECURE**<br>Traffic strictly contained within hypervisor software switch. No host IP assigned. | **RECOMMENDED FOR MULTI-VM** |
| **Disconnected (Cable Unplugged / No Adapter)** | **None** | **None** | **None** | **ZERO RISK (Air-Gapped Equivalent)**<br>Virtual NIC disabled or cable unplugged. Only internal `lo` (127.0.0.1) operates. | **STRONGLY RECOMMENDED** |

> [!IMPORTANT]
> For this laboratory assignment, the virtual machine must be configured in either **Host-Only Networking** (with default gateway removed) or **Disconnected / Cable Unplugged Mode**. The safe bind-shell simulation operates exclusively over the Linux kernel loopback interface (`lo` - `127.0.0.1`), ensuring zero external packet egress.

---

## 3. Step-by-Step Provisioning: Oracle VM VirtualBox

### 3.1 VM Creation Procedure
1. Launch **Oracle VM VirtualBox Manager**.
2. Click **New** (or press `Ctrl+N`).
3. Set the virtual machine parameters:
   - **Name:** `NPC_Capstone_Malware_Sandbox`
   - **Folder:** Default or dedicated laboratory path (e.g., `D:\VirtualBox_VMs\`)
   - **Type:** `Linux`
   - **Version:** `Ubuntu (64-bit)` or `Debian (64-bit)`
4. Allocate Base Memory: **4096 MB (4 GB)**.
5. Allocate Processors: **2 vCPUs**.
6. Create Virtual Hard Disk:
   - Disk size: **30.00 GB**.
   - Format: **VDI (VirtualBox Disk Image)**.
   - Storage on physical hard disk: **Dynamically allocated**.
7. Click **Finish**.

### 3.2 Hypervisor Security Hardening
Before powering on the VM, configure hypervisor isolation:
1. Open VM **Settings** (`Ctrl+S`).
2. Navigate to **General** -> **Advanced**:
   - **Shared Clipboard:** Set to **Disabled**.
   - **Drag'n'Drop:** Set to **Disabled**.
   *(Disabling these features mitigates VM escape vectors and accidental clipboard leakage).*
3. Navigate to **Display** -> **Screen**:
   - **Enable 3D Acceleration:** Ensure **Unchecked**.
4. Navigate to **Shared Folders**:
   - Verify that **NO shared folders** are configured between the host and guest.
5. Navigate to **Network** -> **Adapter 1**:
   - Option A (Air-gapped): Uncheck **Enable Network Adapter**, OR
   - Option B (Host-Only): Attached to: **Host-only Adapter**; select `VirtualBox Host-Only Ethernet Adapter`; open **Advanced** and uncheck **Cable Connected** during execution.

---

## 4. Step-by-Step Provisioning: VMware Workstation

### 4.1 VM Creation Procedure
1. Launch **VMware Workstation Pro** or **Player**.
2. Select **Create a New Virtual Machine** (`Ctrl+N`).
3. Choose **Typical (recommended)** and click **Next**.
4. Select **Installer disc image file (iso)** and browse to the Ubuntu 24.04 LTS ISO.
5. Enter student credentials (User: `student`, Hostname: `npc-sandbox`).
6. Specify Virtual Machine Name: `NPC_Capstone_Malware_Sandbox`.
7. Set Disk Capacity: **30.0 GB** (Select *Store virtual disk as a single file* or *split*).
8. Click **Customize Hardware**:
   - Memory: **4096 MB**.
   - Processors: **2 cores**.
   - Display: Uncheck **Accelerate 3D graphics**.
9. Configure Network Adapter:
   - Select **Custom: Specific virtual network** -> `VMnet1 (Host-only)`, OR
   - Select **Host-only: A private network shared with the host**, OR
   - Uncheck **Connect at power on**.
10. Click **Finish**.

### 4.2 Guest Isolation Settings
In VMware Workstation:
1. Go to **VM** -> **Settings** -> **Options** tab.
2. Select **Guest Isolation**:
   - Uncheck **Enable drag and drop**.
   - Uncheck **Enable copy and paste**.
3. Select **Shared Folders**:
   - Ensure set to **Disabled**.

---

## 5. Clean State Verification & Snapshot Baseline

Once the Linux operating system is installed and baseline packages (`python3`, `net-tools`, `lsof`, `tcpdump`, `curl`) are installed, take the baseline snapshot:

1. In the guest VM terminal, update packages and clean package caches:
   ```bash
   sudo apt-get clean
   history -c
   ```
2. Shut down the virtual machine cleanly or keep it in a paused/powered-off state:
   ```bash
   sudo shutdown -h now
   ```
3. In VirtualBox / VMware, navigate to the **Snapshots / Snapshots Manager** tab.
4. Click **Take** (or `Ctrl+Shift+T` in VirtualBox).
5. Specify the mandatory snapshot details:
   - **Snapshot Name:** `NPC_Capstone_Clean_State`
   - **Snapshot Description:** `Baseline clean installation of Ubuntu Linux 64-bit with all diagnostic tools installed, zero background listeners active, no network persistence, and networking isolated. Author: Vishal Katyare (PRN: 2125UCSM1034).`
6. Click **OK**.

The clean baseline is now sealed and ready for controlled experiment execution.
