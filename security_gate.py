import subprocess
import sys

print("=" * 50)
print("TASKFLOW SECURITY GATE")
print("=" * 50)

print("\nRunning dependency vulnerability scan...")
print("Tool: pip-audit")
print("Target: requirements.txt")

result = subprocess.run(
    [
        sys.executable,
        "-m",
        "pip_audit",
        "-r",
        "requirements.txt"
    ],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.stderr:
    print(result.stderr)

if result.returncode != 0:
    print("\nSECURITY GATE FAILED")
    print("Known dependency vulnerabilities were detected or the scan failed.")
    sys.exit(1)

print("\nNo known vulnerabilities found")
print("SECURITY GATE PASSED")
print("=" * 50)