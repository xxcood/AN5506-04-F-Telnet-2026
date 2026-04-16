see full video 
[AN5506-04-FA](https://youtu.be/A4qx5TDCzoo)
# AN5506-04-F-Telnet-2026
AN5506-04-F  Telnet 2026 administrator PASS
AN5506-04-F  Telnet 2026 
A real-time interactive Telnet client forAN5506-04-F routers (tested on `192.168.1.1`, User: `gepon`).  

---
Requirements
Windows (uses `msvcrt` for non-blocking keyboard input)
Python 3.8+
`telnetlib3` library
Install the dependency:
```bash
pip install telnetlib3
```
---
Setup
Clone or download this repo
Open `router_telnet.py` and set your router's credentials at the top:
```python
HOST = "192.168.1.1"   # Your router's IP
PORT = 23               # Telnet port (default 23)
USER = "gepon"          # Telnet username
PASS = "gepon"          # Telnet password
```
Run with PowerShell (recommended) or CMD:
```powershell
python router_telnet.py
```
> **Note:** Run PowerShell as Administrator if you get permission errors.
---
Usage
Once connected you will see the `User>` prompt. The script handles login automatically.
Step-by-step during a router reboot
This is the main use case — monitoring and interacting with the router while it reboots:
1. Start the script before or during reboot
```
python router_telnet.py
```
The script will keep retrying the connection every 2 seconds until the router comes back online. You do not need to restart it.
```
[*] Connecting to 192.168.1.1:23 (attempt 1)...
[-] Connection failed: ... Retrying in 2s...
[*] Connecting to 192.168.1.1:23 (attempt 2)...
...
[+] Connected!
[+] Logged in. You are now at User> prompt.
```
2. Elevate to privileged mode
Type at the prompt:
```
enable
```
Donate paypal.me/XTechNet
