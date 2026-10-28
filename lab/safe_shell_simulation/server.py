#!/usr/bin/env python3
"""
==============================================================================
NPC Capstone Project — Malware Analysis Sandbox
Safe Local Bind-Shell Simulation Server (Educational Demonstration)
==============================================================================
Student Name   : Vishal Katyare
PRN Number     : 2125UCSM1034
Department     : Computer Science Engineering (Cyber Security)
University     : Sanjivani University, Kopargaon
Subject        : NPC Capstone Project
==============================================================================

SAFETY & ISOLATION POLICY:
1. This script is strictly an educational laboratory demonstration.
2. It binds EXCLUSIVELY to loopback IPv4 address 127.0.0.1 on port 54321.
3. It CANNOT bind to 0.0.0.0, external interfaces, or bridged networks.
4. It accepts ONLY predefined harmless test commands: STATUS, HELP, EXIT.
5. All arbitrary system commands (e.g. ls, whoami, sh, bash) are REJECTED.
6. Absolutely NO subprocess execution, os.system(), eval(), or exec() calls.
7. Shuts down cleanly on SIGINT (Ctrl+C) or SIGTERM, closing all sockets.
==============================================================================
"""

import sys
import os
import socket
import select
import signal
import time
from datetime import datetime

# Mandatory Local-Only Binding Configuration
BIND_HOST = "127.0.0.1"
BIND_PORT = 54321
BUFFER_SIZE = 1024
SERVER_START_TIME = time.time()

# Safety assertion: prevent accidental binding to external addresses
if BIND_HOST != "127.0.0.1":
    sys.stderr.write("[FATAL SECURITY ERROR] Bind address MUST be 127.0.0.1! Aborting execution.\n")
    sys.exit(1)


def log_message(msg: str):
    """Outputs a timestamped laboratory audit log message."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [SAFE_SERVER] {msg}", flush=True)


def get_uptime_string() -> str:
    """Computes server uptime in seconds."""
    uptime_sec = int(time.time() - SERVER_START_TIME)
    mins, secs = divmod(uptime_sec, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}h:{mins:02d}m:{secs:02d}s"


def handle_command(command_raw: str, client_addr: tuple) -> tuple[str, bool]:
    """
    Parses and evaluates predefined safe commands.
    Returns: (response_string, should_close_connection)
    
    SAFETY RULE: Predefined deterministic string responses only.
    No shell command execution is permitted.
    """
    cmd = command_raw.strip().upper()
    log_message(f"Command received from {client_addr[0]}:{client_addr[1]} -> '{cmd}'")

    if not cmd:
        return ("NPC_SHELL> (Empty command received. Type HELP for available commands)\r\n", False)

    if cmd == "STATUS":
        resp = (
            "====================================================\r\n"
            "NPC CAPSTONE SAFE SHELL SIMULATION — STATUS REPORT\r\n"
            "====================================================\r\n"
            f"Student Name       : Vishal Katyare\r\n"
            f"PRN                : 2125UCSM1034\r\n"
            f"Institution        : Sanjivani University, Kopargaon\r\n"
            f"Specialization     : Cyber Security\r\n"
            f"Server Process ID  : {os.getpid()}\r\n"
            f"Binding Address    : {BIND_HOST}:{BIND_PORT} (Loopback Only)\r\n"
            f"Server Uptime      : {get_uptime_string()}\r\n"
            f"Execution Mode     : Isolated Safe Simulation (No Subprocess)\r\n"
            f"Arbitrary Exec     : STRICTLY DISABLED\r\n"
            "Status             : ONLINE / CONTROLLED LAB EXPERIMENT\r\n"
            "====================================================\r\n"
        )
        return (resp, False)

    elif cmd == "HELP":
        resp = (
            "====================================================\r\n"
            "AVAILABLE SAFE COMMANDS (DETERMINISTIC SIMULATION):\r\n"
            "====================================================\r\n"
            "  STATUS : Displays process metadata, student PRN, and uptime.\r\n"
            "  HELP   : Displays this documentation screen.\r\n"
            "  EXIT   : Terminates the current client connection safely.\r\n"
            "----------------------------------------------------\r\n"
            "SECURITY NOTICE:\r\n"
            "  Arbitrary OS commands (e.g., ls, whoami, cat, rm) are\r\n"
            "  explicitly rejected by design to prevent any guest system\r\n"
            "  tampering or unauthorized interaction.\r\n"
            "====================================================\r\n"
        )
        return (resp, False)

    elif cmd == "EXIT":
        resp = "Closing connection. NPC Capstone safe session ended. Goodbye!\r\n"
        return (resp, True)

    else:
        # Explicit rejection of unauthorized or arbitrary commands
        resp = (
            f"[SECURITY REJECTION] Command '{cmd}' is NOT permitted.\r\n"
            "This simulation strictly prohibits arbitrary command execution.\r\n"
            "Authorized commands: STATUS, HELP, EXIT\r\n"
        )
        log_message(f"SECURITY ALERT: Rejected arbitrary input '{cmd}' from {client_addr[0]}:{client_addr[1]}")
        return (resp, False)


class SafeSimulationServer:
    """Manages the lifecycle of the safe educational socket server."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self):
        """Initializes and runs the loopback listener loop."""
        # Setup signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            log_message("==========================================================")
            log_message("NPC Capstone: Safe Bind-Shell Simulation Initialized")
            log_message(f"Student: Vishal Katyare | PRN: 2125UCSM1034")
            log_message(f"Bound to: {self.host}:{self.port} (Strict Loopback Only)")
            log_message(f"Process PID: {os.getpid()}")
            log_message("Awaiting local client connections... (Press Ctrl+C to terminate)")
            log_message("==========================================================")

            while self.running:
                try:
                    # Non-blocking accept using select with a 1.0 second timeout
                    readable, _, _ = select.select([self.server_socket], [], [], 1.0)
                    if not readable:
                        continue

                    client_sock, client_addr = self.server_socket.accept()
                    log_message(f"Connection accepted from {client_addr[0]}:{client_addr[1]}")
                    self._handle_client(client_sock, client_addr)

                except select.error:
                    break
                except socket.error as e:
                    if self.running:
                        log_message(f"Socket error encountered: {e}")
                    break

        except Exception as e:
            log_message(f"Failed to start server: {e}")
        finally:
            self.stop()

    def _handle_client(self, client_sock: socket.socket, client_addr: tuple):
        """Communicates with the connected local client."""
        client_sock.settimeout(30.0)  # 30-second idle timeout
        try:
            welcome_banner = (
                "****************************************************\r\n"
                "* NPC Capstone: Safe Shell Simulation (127.0.0.1)   *\r\n"
                "* Student: Vishal Katyare | PRN: 2125UCSM1034       *\r\n"
                "* Department: Computer Science Engineering (CS)     *\r\n"
                "* Commands: STATUS, HELP, EXIT                      *\r\n"
                "****************************************************\r\n"
                "NPC_SHELL> "
            )
            client_sock.sendall(welcome_banner.encode("utf-8"))

            while self.running:
                data = client_sock.recv(BUFFER_SIZE)
                if not data:
                    log_message(f"Client {client_addr[0]}:{client_addr[1]} closed connection.")
                    break

                command_str = data.decode("utf-8", errors="replace")
                response, should_close = handle_command(command_str, client_addr)
                
                # Append shell prompt if not closing
                if not should_close:
                    response += "NPC_SHELL> "
                
                client_sock.sendall(response.encode("utf-8"))

                if should_close:
                    log_message(f"Session terminated by client {client_addr[0]}:{client_addr[1]}.")
                    break

        except socket.timeout:
            log_message(f"Client {client_addr[0]}:{client_addr[1]} timed out (idle).")
        except socket.error as e:
            log_message(f"Connection with {client_addr[0]}:{client_addr[1]} ended: {e}")
        finally:
            try:
                client_sock.close()
            except Exception:
                pass
            log_message(f"Socket closed for {client_addr[0]}:{client_addr[1]}")

    def _signal_handler(self, signum, frame):
        """Handles termination signals cleanly."""
        sig_name = "SIGINT (Ctrl+C)" if signum == signal.SIGINT else f"Signal {signum}"
        log_message(f"Received {sig_name}. Initiating safe laboratory shutdown...")
        self.running = False

    def stop(self):
        """Releases the socket and cleans up resources."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None
        log_message("Server socket closed. Safe bind-shell simulation terminated cleanly.")


def main():
    server = SafeSimulationServer(BIND_HOST, BIND_PORT)
    server.start()


if __name__ == "__main__":
    main()
