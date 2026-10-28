# Packet Captures Directory

This directory stores network packet captures (`.pcap`) recorded during the simulation.

### Instructions:
Record loopback traffic using `tcpdump`:
```bash
sudo tcpdump -i lo -nnvv -s 0 -w evidence/packet_captures/loopback_shell.pcap port 54321
```

### Verification:
Inspect the packet capture in Wireshark or via:
```bash
tcpdump -r evidence/packet_captures/loopback_shell.pcap -nn -X
```
Verify that only loopback (`127.0.0.1`) TCP frames are present and confirm the 3-way handshake, data segments, and connection teardown.
