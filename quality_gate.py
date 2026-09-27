import csv
import os
import re
import subprocess
import sys
from datetime import datetime

PYLINT_MIN_SCORE = 8.0
MAX_COMPLEXITY = 10
TREND_FILE = "quality_history.csv"


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


# ---------------- QUALITY TREND MONITORING ----------------

print("\nRecording quality trend...")

build_number = os.environ.get("BUILD_NUMBER", "LOCAL")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

file_exists = os.path.exists(TREND_FILE)

with open(TREND_FILE, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "Build",
            "Timestamp",
            "Pylint Score",
            "Highest Complexity"
        ])

    writer.writerow([
        build_number,
        timestamp,
        f"{pylint_score:.2f}",
        highest_complexity
    ])

print(f"Quality trend recorded in {TREND_FILE}")
print(f"Build: {build_number}")
print(f"Pylint score: {pylint_score:.2f}/10")
print(f"Highest complexity: {highest_complexity}")

print("\n" + "=" * 50)
print("ALL CODE QUALITY GATES PASSED")
print("=" * 50)

sys.exit(0)