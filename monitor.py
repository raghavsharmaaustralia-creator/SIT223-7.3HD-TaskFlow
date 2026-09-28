import csv
import os
import urllib.error
import urllib.request
from datetime import datetime

APP_NAME = "TaskFlow"
PRODUCTION_HOST = "127.0.0.1"
PRODUCTION_PORT = "5060"
HEALTH_URL = f"http://{PRODUCTION_HOST}:{PRODUCTION_PORT}/health"
MONITORING_FILE = "monitoring_history.csv"

# Used only when testing the monitoring and alerting system
SIMULATE_FAILURE = os.environ.get(
    "SIMULATE_MONITORING_FAILURE", "false"
).lower() == "true"


def save_monitoring_record(timestamp, status, alert):
    file_exists = os.path.exists(MONITORING_FILE)

    with open(
        MONITORING_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Application",
                "Health URL",
                "Status",
                "Alert"
            ])

        writer.writerow([
            timestamp,
            APP_NAME,
            HEALTH_URL,
            status,
            alert
        ])

    print("\nMonitoring record saved.")
    print(f"Monitoring history: {MONITORING_FILE}")


def check_production_health():
    print("=" * 60)
    print("TASKFLOW PRODUCTION MONITORING")
    print("=" * 60)

    print(f"Application: {APP_NAME}")
    print(f"Monitoring endpoint: {HEALTH_URL}")
    print("Checking production health...")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Controlled incident simulation for testing the alert system
    if SIMULATE_FAILURE:
        status = "UNHEALTHY"
        alert = "ALERT"

        print("\nSIMULATED INCIDENT: Production service failure detected.")
        print("Monitoring status: UNHEALTHY")
        print("ALERT: Production service is unavailable.")

        save_monitoring_record(
            timestamp,
            status,
            alert
        )

        print("\n" + "=" * 60)
        print("MONITORING GATE FAILED")
        print("=" * 60)

        raise SystemExit(1)

    try:
        with urllib.request.urlopen(
            HEALTH_URL,
            timeout=5
        ) as response:

            body = response.read().decode("utf-8")
            clean_body = body.replace(" ", "")

            healthy = (
                response.status == 200
                and '"status":"healthy"' in clean_body
                and '"service":"TaskFlow"' in clean_body
            )

            if healthy:
                status = "HEALTHY"
                alert = "NO ALERT"

                print("\nMonitoring status: HEALTHY")
                print(f"HTTP status: {response.status}")
                print(f"Response: {body}")
                print("Alert status: NO ALERT")

            else:
                status = "UNHEALTHY"
                alert = "ALERT"

                print("\nMonitoring status: UNHEALTHY")
                print(f"HTTP status: {response.status}")
                print(f"Response: {body}")
                print("ALERT: Production health check failed.")

    except (
        urllib.error.URLError,
        TimeoutError
    ) as error:

        status = "UNHEALTHY"
        alert = "ALERT"

        print("\nMonitoring status: UNHEALTHY")
        print("ALERT: Production service is unavailable.")
        print(f"Details: {error}")

    save_monitoring_record(
        timestamp,
        status,
        alert
    )

    print("\n" + "=" * 60)

    if status != "HEALTHY":
        print("MONITORING GATE FAILED")
        print("=" * 60)
        raise SystemExit(1)

    print("MONITORING GATE PASSED")
    print("=" * 60)


if __name__ == "__main__":
    check_production_health()