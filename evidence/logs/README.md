# System Logs & Terminal Audit Records

This directory contains raw text logs recorded during the live laboratory execution.

### Standard Log Files to Generate:
1. `isolation_verification.log`: Output of `ip addr`, `ip route`, `ping -c 3 8.8.8.8`, and `curl`.
2. `server_runtime.log`: Full console output of `server.py` during execution.
3. `socket_audit.log`: Snapshot of `ss -tulpn` and `ss -tan` during active connection.
4. `process_audit.log`: Snapshot of `ps aux | grep server.py` and `lsof -i :54321`.
5. `post_recovery_audit.log`: Proof of clean state following snapshot reversion.
