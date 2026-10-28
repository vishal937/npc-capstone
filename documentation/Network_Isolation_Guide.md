# Network Isolation & Traffic Containment Guide

**Course:** NPC Capstone Project  
**Student Name:** Vishal Katyare  
**PRN:** 2125UCSM1034  
**Department:** Computer Science Engineering (Cyber Security)  
**University:** Sanjivani University, Kopargaon  

---

## 1. Principles of Network Containment in Malware Sandboxes

Dynamic analysis involves observing untrusted code during live execution. If the sandboxed virtual machine retains an active path to external networks, two severe consequences can occur:
1. **Malicious Outbound Egress:** Malware can join a botnet, participate in distributed denial-of-service (DDoS) attacks, exfiltrate stolen host telemetry, or download destructive second-stage payloads (e.g., ransomware cryptors).
2. **Threat Actor Infiltration & Notification:** Attackers monitoring their C2 listener dashboards will observe the IP address of the university or researcher, alerting them that their binary is under active reverse engineering and compromising threat intelligence operations.

Therefore, an airtight **network isolation protocol** is an absolute prerequisite.

---

## 2. Loopback Architecture vs. External Egress

In computer networking, the loopback device (`lo`, IPv4 `127.0.0.1/8`, IPv6 `::1`) is a purely software-implemented network interface managed directly within the Linux kernel networking stack:
- Packets routed to `127.0.0.1` are never translated into Ethernet frames by a physical or virtual Network Interface Card (NIC).
- Loopback packets never traverse the hypervisor's software bridge, virtual switch, or host physical adapter.
- In contrast, external interfaces (e.g., `eth0`, `enp0s3`) pass frames through hypervisor drivers (`vboxnetflt`, `vmnet`) directly to the host operating system.

By configuring our safe simulation listener to bind **exclusively to `127.0.0.1`**, communication remains entirely self-contained within the guest kernel's memory space.

---

## 3. Pre-Execution Isolation Verification Protocol

Before running any script or shell simulation in the laboratory virtual machine, the student must execute and document the following four-step verification suite:

### Test 1: Interface Inspection
Confirm the status of network interfaces:
```bash
ip addr show
```
*Expected Output:*
- `lo`: State `UNKNOWN` or `UP`, address `127.0.0.1/8`.
- `enp0s3` / `eth0`: Either absent, `DOWN`, or configured with a private host-only address without a default gateway.

### Test 2: Routing Table Verification
Ensure no default gateway is present to route packets outside the local subnet:
```bash
ip route show
```
*Expected Output:*
- No entry starting with `default via ...`.
- Only local subnet routes (e.g., `127.0.0.0/8 dev lo proto kernel scope link src 127.0.0.1`).

### Test 3: ICMP Egress Test (Direct IP)
Verify that outbound packets cannot reach public IPv4 addresses:
```bash
ping -c 3 -W 2 8.8.8.8
```
*Expected Output:*
```text
ping: connect: Network is unreachable
# OR
3 packets transmitted, 0 received, 100% packet loss
```

### Test 4: DNS Resolution & HTTP Egress Test
Verify that domain name lookups and outbound web requests fail immediately:
```bash
ping -c 3 google.com
```
*Expected Output:*
```text
ping: google.com: Temporary failure in name resolution
```

```bash
curl --connect-timeout 3 http://example.com
```
*Expected Output:*
```text
curl: (6) Could not resolve host: example.com
# OR
curl: (7) Failed to connect to example.com port 80: Network is unreachable
```

---

## 4. Live Packet Capture Methodology (Loopback Interface)

To observe and prove the socket behavior of the safe bind-shell simulation, packet capture is conducted directly on the loopback interface using `tcpdump`.

### Step 1: Launch Packet Capture in Background / Separate Terminal
Before starting the shell simulation, initiate packet capture on interface `lo`:
```bash
sudo tcpdump -i lo -nnvv -X -s 0 -w evidence/packet_captures/loopback_shell.pcap port 54321
```
*Explanation of flags:*
- `-i lo`: Capture exclusively on the loopback device.
- `-nn`: Do not resolve hostnames or port numbers (preserves raw numeric IP and port data).
- `-vv`: Verbose protocol decoding (TTL, identification flags, TCP options).
- `-X`: Display packet contents in both hex and ASCII formats.
- `-s 0`: Capture full packet payload without truncation.
- `-w <path>`: Write raw packets to standard PCAP format for Wireshark inspection.
- `port 54321`: Restrict capture strictly to the simulation port.

### Step 2: Trigger Traffic
1. In another terminal, start `python3 lab/safe_shell_simulation/server.py`.
2. In a third terminal, run `python3 lab/safe_shell_simulation/client.py`.
3. Issue commands: `STATUS`, `HELP`, `whoami` (to trigger rejection), and `EXIT`.

### Step 3: Stop Packet Capture & Inspect
Press `Ctrl+C` in the `tcpdump` terminal to stop logging.

Inspect the captured file directly in the console:
```bash
tcpdump -r evidence/packet_captures/loopback_shell.pcap -nn -X
```

### Step 4: Wireshark Packet Dissection
Open `loopback_shell.pcap` in Wireshark:
1. Observe the **TCP Three-Way Handshake**:
   - `Frame 1: 127.0.0.1:client_port -> 127.0.0.1:54321 [SYN] Seq=0`
   - `Frame 2: 127.0.0.1:54321 -> 127.0.0.1:client_port [SYN, ACK] Seq=0 Ack=1`
   - `Frame 3: 127.0.0.1:client_port -> 127.0.0.1:54321 [ACK] Seq=1 Ack=1`
2. Follow TCP Stream (`Analyze` -> `Follow` -> `TCP Stream`):
   - Blue text displays client requests (`STATUS\n`, `HELP\n`, etc.).
   - Red text displays server responses (student details, status report, rejection notices).
3. Observe the **TCP Four-Way Teardown**:
   - `[FIN, ACK]` and `[ACK]` exchanges verifying clean session termination.

---

## 5. Summary of Egress Prevention Controls

| Layer | Control Implemented | Verification Mechanism |
|---|---|---|
| **Layer 1 / Physical** | Virtual NIC detached or cable disconnected | Hypervisor VM Settings GUI |
| **Layer 3 / Network** | No default gateway configured in guest kernel | `ip route show` returns no default route |
| **Layer 4 / Transport** | Server strictly bound to `127.0.0.1` | `ss -tulpn` verifies `127.0.0.1:54321` |
| **Layer 7 / Application** | Predefined commands only; no arbitrary shell execution | Source code audit of `server.py` |
