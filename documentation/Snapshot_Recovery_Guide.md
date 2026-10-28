# Snapshot Creation, Restoration & Recovery Verification Guide

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Technical Mechanics of Virtual Machine Snapshots

In computer virtualization, a **snapshot** preserves the exact state of a virtual machine at a specific point in time, including virtual disk storage, virtual hardware configuration, and optionally RAM / CPU execution registers.

### 1.1 Copy-on-Write (CoW) Differencing Disks
When a snapshot is created, the hypervisor freezes the base virtual disk image and marks it read-only:
- **Oracle VM VirtualBox:** Creates a differencing VDI file (e.g., `{UUID}.vdi`) in the `Snapshots/` subfolder. All subsequent guest write operations (file creations, file modifications, OS log entries) are written exclusively to this differencing image.
- **VMware Workstation:** Creates a redo-log delta VMDK file (e.g., `VirtualMachine-000001.vmdk`). Unmodified data blocks continue to be read from the base `VirtualMachine.vmdk`, while modified and new blocks are redirected to the delta file.

### 1.2 Snapshot Reversion Mechanics
When the user restores a snapshot:
1. The hypervisor discards or unlinks the active differencing disk containing experimental changes.
2. The virtual disk pointer is reset back to the frozen base state (or the designated snapshot delta).
3. The guest OS boots into the exact disk state that existed prior to running the experiment, eliminating all malware modifications, rootkits, user accounts, and listening sockets.

---

## 2. Laboratory Snapshot Workflow: `NPC_Capstone_Clean_State`

### Step 1: Pre-Snapshot Cleanliness Verification
Before taking the baseline snapshot, verify that the Linux environment is pristine:
```bash
# Verify no active listening sockets on non-standard ports
sudo ss -tulpn

# Verify no custom background processes are executing
ps aux | grep -E "python|server|client"

# Remove transient package caches and clean bash history
sudo apt-get clean
sudo rm -rf /tmp/* ~/.cache/*
history -c
```

### Step 2: Taking the Snapshot
1. Power down the VM or pause execution:
   ```bash
   sudo shutdown -h now
   ```
2. In **VirtualBox Manager**:
   - Select `NPC_Capstone_Malware_Sandbox`.
   - Click the hamburger menu next to the VM name -> **Snapshots** -> **Take**.
   - **Name:** `NPC_Capstone_Clean_State`
   - **Description:** `Baseline clean installation of Ubuntu Linux 64-bit with diagnostic utilities installed. Zero custom listeners or background processes. Student: Vishal Katyare (PRN: 2125UCSM1034).`
   - Click **OK**.
3. In **VMware Workstation**:
   - Go to **VM** -> **Snapshot** -> **Take Snapshot...**.
   - **Name:** `NPC_Capstone_Clean_State`
   - **Description:** Enter the same formal description.
   - Click **Take Snapshot**.

---

## 3. Post-Experiment Snapshot Restoration Workflow

After executing `server.py`, interacting via `client.py`, and recording all system observations, revert the virtual machine:

### Reversion Procedure in VirtualBox
1. Close the VM window -> Select **Power off the machine** -> Check **Restore current snapshot 'NPC_Capstone_Clean_State'** -> Click **OK**, OR
2. In VirtualBox Manager main window:
   - Select `NPC_Capstone_Malware_Sandbox`.
   - Go to **Snapshots**.
   - Click on `NPC_Capstone_Clean_State`.
   - Click **Restore** (icon with curved back-arrow).
   - Uncheck "Create a snapshot of the current machine state" (to discard experimental changes).
   - Click **Restore**.

### Reversion Procedure in VMware Workstation
1. Go to **VM** -> **Snapshot** -> **Revert to Snapshot: NPC_Capstone_Clean_State**.
2. When prompted "Do you want to revert to the snapshot?", click **Yes**.

---

## 4. Post-Recovery Verification & Integrity Audit

To prove that experimental changes have been completely eliminated and the system has successfully returned to baseline, power on the restored VM and execute the following post-recovery audit commands:

### Audit 1: Verification of Listening Sockets
Ensure that TCP port `54321` is closed and no daemon remains active:
```bash
sudo ss -tulpn | grep 54321
```
*Expected Result:* **Empty output** (return code 1). Demonstrates that no listening socket survived restoration.

### Audit 2: Verification of Running Processes
Ensure that neither `server.py` nor `client.py` is present in the process table:
```bash
ps aux | grep -E "server.py|client.py" | grep -v grep
```
*Expected Result:* **Empty output**. Proves all experimental processes were cleanly purged.

### Audit 3: Open File Descriptor Inspection
Ensure no file descriptors are held open on simulation ports:
```bash
sudo lsof -i :54321
```
*Expected Result:* **Empty output**.

### Audit 4: File System Integrity Check
If any temporary test files (e.g., `/tmp/test_artifact.txt` or `/root/test_drop.bin`) were created during the experiment, verify that they no longer exist:
```bash
ls -la /tmp/test_artifact.txt
```
*Expected Result:* `ls: cannot access '/tmp/test_artifact.txt': No such file or directory`.

---

## 5. Forensic Limitations of Hypervisor Snapshots

While snapshots provide rapid, reliable disk restoration for educational and triage purposes, security researchers must understand their technical limitations in advanced threat scenarios:

1. **Non-Reversion of Shared Folders:**  
   If a hypervisor shared folder (VirtualBox Guest Additions Shared Folder or VMware Host-Guest Filesystem - HGFS) is mounted inside the VM, any files modified or created within that shared folder reside on the **host file system**. Reverting the guest VM snapshot **does not revert changes made to host shared directories**. Threat actors aware of shared folders can write malicious payloads directly to the host machine.
   *Mitigation:* Never attach shared folders to a malware analysis virtual machine.

2. **Hypervisor Host Telemetry & External Logs:**  
   Snapshots revert internal guest disk blocks only. Network captures performed on the host adapter (`vboxnet0` / `vmnet1`), hypervisor event logs (`vbox.log`, `vmware.log`), and external SIEM/IDS alerts remain permanently recorded outside the guest.

3. **Hypervisor Escape Vulnerabilities (Guest-to-Host Breakout):**  
   Advanced nation-state malware or sophisticated threat specimens may contain zero-day hypervisor breakout exploits (e.g., exploiting shared drag-and-drop buffers, SVGA graphics emulation bugs like CVE-2017-4901, or virtual PCI device flaws). If an exploit achieves code execution in the context of the host hypervisor process, snapshot restoration of the guest is completely ineffective at neutralizing the host-level implant.
   *Mitigation:* Keep hypervisor software fully patched, disable 3D acceleration, disable shared clipboards and drag-and-drop, and run the hypervisor with least-privilege host credentials.

4. **Hardware-Assisted VM Detection (Anti-Analysis):**  
   Snapshot differencing introduces minor disk I/O latency shifts, and hypervisor CPUID modifications can be detected by anti-VM malware (using `RDTSC` timing attacks, `CPUID` instruction profiling, or MAC address vendor OUI checks). In high-assurance malware research, bare-metal physical sandbox machines with hardware-based image restoration (e.g., PXE boot reflashing) are utilized.
