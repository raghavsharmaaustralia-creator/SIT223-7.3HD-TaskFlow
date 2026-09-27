import subprocess
import sys

print("=" * 60)
print("TASKFLOW SECURITY GATE")
print("=" * 60)

# --------------------------------------------------
# 1. Dependency vulnerability scanning with pip-audit
# --------------------------------------------------

print("\n[1] DEPENDENCY VULNERABILITY SCAN")
print("Tool: pip-audit")
print("Target: requirements.txt")

dependency_scan = subprocess.run(
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

print(dependency_scan.stdout)

if dependency_scan.stderr:
    print(dependency_scan.stderr)

if dependency_scan.returncode != 0:
    print("Dependency security status: FAILED")
    print(
        "Interpretation: Known vulnerable dependencies were detected "
        "or the dependency scan could not complete."
    )
    sys.exit(1)

print("Dependency security status: PASSED")
print("Interpretation: No known vulnerabilities were found in dependencies.")


# --------------------------------------------------
# 2. Source-code security scanning with Bandit
# --------------------------------------------------

print("\n[2] SOURCE CODE SECURITY SCAN")
print("Tool: Bandit")
print("Target: app/")

bandit_scan = subprocess.run(
    [
        sys.executable,
        "-m",
        "bandit",
        "-r",
        "app"
    ],
    capture_output=True,
    text=True
)

print(bandit_scan.stdout)

if bandit_scan.stderr:
    print(bandit_scan.stderr)

if bandit_scan.returncode != 0:
    print("Source-code security status: FAILED")
    print(
        "Interpretation: Bandit identified one or more security "
        "issues requiring review."
    )
    sys.exit(1)

print("Source-code security status: PASSED")
print("Severity summary: Low = 0, Medium = 0, High = 0")
print(
    "Interpretation: Bandit identified no security issues "
    "in the application source code."
)

print("\n" + "=" * 60)
print("SECURITY REVIEW SUMMARY")
print("=" * 60)
print("Dependency vulnerabilities: 0 known vulnerabilities")
print("Source-code issues: Low 0 | Medium 0 | High 0")
print("Remediation status: No security findings currently require remediation.")
print("ALL SECURITY GATES PASSED")
print("=" * 60)

sys.exit(0)