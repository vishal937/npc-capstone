#!/usr/bin/env python3
"""
==============================================================================
NPC Capstone Project — Malware Analysis Sandbox
Safe Local Bind-Shell Simulation Client (Educational Demonstration)
==============================================================================
Student Name   : Vishal Katyare
PRN Number     : 2125UCSM1034
Department     : Computer Science Engineering (Cyber Security)
University     : Sanjivani University, Kopargaon
Subject        : NPC Capstone Project
==============================================================================

PURPOSE:
Interactive client script designed to connect exclusively to the local safe
bind-shell simulation (127.0.0.1:54321). Used to verify process responsiveness,
protocol compliance, and demonstrate isolation in the sandboxed environment.
==============================================================================
"""

import sys
import socket
import select

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 54321
BUFFER_SIZE = 2048


def print_banner():
    """Prints the educational client banner."""
    print("=" * 64)
    print(" NPC CAPSTONE: SAFE SHELL SIMULATION TEST CLIENT")
    print(" Student Name : Vishal Katyare")
    print(" PRN Number   : 2125UCSM1034")
    print(" Institution  : Sanjivani University, Kopargaon")
    print(f" Target       : {TARGET_HOST}:{TARGET_PORT} (Loopback Interface)")
    print(" Commands     : STATUS, HELP, EXIT")
    print("=" * 64)


def main():
    print_banner()

    # Safety check: enforce local loopback target only
    if TARGET_HOST != "127.0.0.1":
        print("[FATAL SECURITY ERROR] Target host must be 127.0.0.1. Aborting.")
        sys.exit(1)

    print(f"[*] Attempting connection to {TARGET_HOST}:{TARGET_PORT}...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)

    try:
        sock.connect((TARGET_HOST, TARGET_PORT))
        print(f"[+] Successfully connected to {TARGET_HOST}:{TARGET_PORT}.")
        print("[*] Ready for command interaction.\n")
    except ConnectionRefusedError:
        print(f"[-] Connection refused on {TARGET_HOST}:{TARGET_PORT}.")
        print("    Ensure that server.py is running in a separate terminal:")
        print("    Command: python3 lab/safe_shell_simulation/server.py")
        sys.exit(1)
    except socket.timeout:
        print(f"[-] Connection attempt timed out to {TARGET_HOST}:{TARGET_PORT}.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Connection error: {e}")
        sys.exit(1)

    sock.settimeout(None)

    try:
        # Read initial banner from server
        initial_data = sock.recv(BUFFER_SIZE)
        if initial_data:
            sys.stdout.write(initial_data.decode("utf-8", errors="replace"))
            sys.stdout.flush()

        while True:
            # Read user input from terminal
            try:
                user_cmd = input()
            except EOFError:
                break

            # Send command to server
            sock.sendall((user_cmd + "\n").encode("utf-8"))

            if user_cmd.strip().upper() == "EXIT":
                # Receive farewell message before closing
                try:
                    farewell = sock.recv(BUFFER_SIZE)
                    if farewell:
                        sys.stdout.write(farewell.decode("utf-8", errors="replace"))
                except Exception:
                    pass
                print("\n[*] Session concluded. Disconnecting client.")
                break

            # Receive and display response from server
            response_chunks = []
            while True:
                # Use select to check if more socket data is immediately available
                ready_to_read, _, _ = select.select([sock], [], [], 0.3)
                if not ready_to_read:
                    break
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    break
                response_chunks.append(data.decode("utf-8", errors="replace"))
                # Stop reading once the prompt is displayed at the end
                if "".join(response_chunks).endswith("NPC_SHELL> "):
                    break

            response = "".join(response_chunks)
            if not response:
                print("[-] Server disconnected.")
                break

            sys.stdout.write(response)
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n[*] User interrupted session with Ctrl+C. Closing client socket.")
        try:
            sock.sendall(b"EXIT\n")
        except Exception:
            pass
    finally:
        sock.close()
        print("[*] Connection closed cleanly.")


if __name__ == "__main__":
    main()
