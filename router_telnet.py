import asyncio
import msvcrt
import sys
import telnetlib3

HOST = "192.168.1.1"
PORT = 23
USER = "gepon"
PASS = "gepon"

RECONNECT_DELAY = 2


async def monitor_output(reader: telnetlib3.TelnetReader):
    """Continuously print router output without blocking."""
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("\n[!] Router closed the connection.")
                break
            print(data, end="", flush=True)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"\n[!] Reader error: {e}")


async def login(writer: telnetlib3.TelnetWriter):
    """Send login credentials and wake up the CLI."""
    writer.write(USER + "\n")
    await asyncio.sleep(0.3)
    writer.write(PASS + "\n")
    await asyncio.sleep(1.0)
    writer.write("\n")
    await asyncio.sleep(0.5)


async def keyboard_input(writer: telnetlib3.TelnetWriter):
    """
    Read keyboard input character by character using msvcrt (Windows-native).
    This never blocks the event loop.
    """
    line = ""
    while True:
        # Yield control to event loop so monitor_output can run
        await asyncio.sleep(0.05)

        while msvcrt.kbhit():
            ch = msvcrt.getwch()

            if ch == "\r":               # Enter key
                print()                  # move to next line
                writer.write(line + "\n")
                line = ""

            elif ch == "\x03":           # Ctrl-C
                print("\n[*] Ctrl-C pressed. Exiting.")
                sys.exit(0)

            elif ch == "\x08" or ch == "\x7f":  # Backspace
                if line:
                    line = line[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()

            elif ch == "\x00" or ch == "\xe0":  # Special keys (arrows etc)
                msvcrt.getwch()          # consume the second byte, ignore

            else:
                line += ch
                sys.stdout.write(ch)
                sys.stdout.flush()


async def session(reader, writer):
    """Handle one connected session."""
    output_task = asyncio.create_task(monitor_output(reader))
    input_task = asyncio.create_task(keyboard_input(writer))

    try:
        await login(writer)
        print("[+] Logged in. You are now at User> prompt.\n")
        await asyncio.gather(output_task, input_task)
    except asyncio.CancelledError:
        pass
    except SystemExit:
        raise
    finally:
        output_task.cancel()
        input_task.cancel()
        await asyncio.gather(output_task, input_task, return_exceptions=True)
        try:
            writer.close()
        except Exception:
            pass


async def main():
    attempt = 0
    while True:
        attempt += 1
        print(f"[*] Connecting to {HOST}:{PORT} (attempt {attempt})...")
        try:
            reader, writer = await telnetlib3.open_connection(HOST, PORT)
            print("[+] Connected!")
            await session(reader, writer)
            break
        except SystemExit:
            raise
        except KeyboardInterrupt:
            print("\n[*] Interrupted. Exiting.")
            break
        except OSError as e:
            print(f"[-] Connection failed: {e}. Retrying in {RECONNECT_DELAY}s...")
            await asyncio.sleep(RECONNECT_DELAY)
        except Exception as e:
            print(f"[!] Unexpected error: {e}. Retrying in {RECONNECT_DELAY}s...")
            await asyncio.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Exiting.")