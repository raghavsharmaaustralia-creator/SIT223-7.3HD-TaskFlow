import re
import subprocess
import sys

PYLINT_MIN_SCORE = 8.0
MAX_COMPLEXITY = 10


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True
    )
    return result.stdout + result.stderr


print("=" * 50)
print("TASKFLOW CODE QUALITY GATE")
print("=" * 50)

# ---------------- PYLINT QUALITY GATE ----------------

print("\nRunning Pylint analysis...")

pylint_output = run_command(
    f'"{sys.executable}" -m pylint app tests'
)

print(pylint_output)

score_match = re.search(
    r"rated at (-?\d+(?:\.\d+)?)/10",
    pylint_output
)

if not score_match:
    print("QUALITY GATE FAILED: Could not determine Pylint score.")
    sys.exit(1)

pylint_score = float(score_match.group(1))

print(f"Pylint score: {pylint_score}/10")
print(f"Required Pylint score: {PYLINT_MIN_SCORE}/10")

if pylint_score < PYLINT_MIN_SCORE:
    print("QUALITY GATE FAILED: Pylint score is below threshold.")
    sys.exit(1)

print("Pylint quality gate PASSED.")


# ---------------- COMPLEXITY QUALITY GATE ----------------

print("\nRunning Radon complexity analysis...")

radon_output = run_command(
    f'"{sys.executable}" -m radon cc app -a -s'
)

print(radon_output)

complexities = [
    int(value)
    for value in re.findall(r"\(([0-9]+)\)", radon_output)
]

if not complexities:
    print("QUALITY GATE FAILED: Could not determine complexity.")
    sys.exit(1)

highest_complexity = max(complexities)

print(f"Highest cyclomatic complexity: {highest_complexity}")
print(f"Maximum permitted complexity: {MAX_COMPLEXITY}")

if highest_complexity > MAX_COMPLEXITY:
    print("QUALITY GATE FAILED: Complexity threshold exceeded.")
    sys.exit(1)

print("Complexity quality gate PASSED.")

print("\n" + "=" * 50)
print("ALL CODE QUALITY GATES PASSED")
print("=" * 50)

sys.exit(0)