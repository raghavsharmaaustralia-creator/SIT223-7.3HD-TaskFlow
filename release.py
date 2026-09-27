import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

APP_NAME = "TaskFlow"

STAGING_DIR = "deploy"
PRODUCTION_DIR = "production"
PRODUCTION_BACKUP_DIR = "production_backup"

PRODUCTION_HOST = "127.0.0.1"
PRODUCTION_PORT = "5060"
HEALTH_URL = (
    f"http://{PRODUCTION_HOST}:{PRODUCTION_PORT}/health"
)


def rollback():
    print("Rolling back production release...")

    if os.path.exists(PRODUCTION_DIR):
        shutil.rmtree(PRODUCTION_DIR)

    if os.path.exists(PRODUCTION_BACKUP_DIR):
        shutil.copytree(
            PRODUCTION_BACKUP_DIR,
            PRODUCTION_DIR
        )
        print("Production rollback completed successfully.")
    else:
        print("No previous production release backup was available.")


def verify_release_files():
    required_files = [
        os.path.join(PRODUCTION_DIR, "app"),
        os.path.join(PRODUCTION_DIR, "run.py"),
        os.path.join(PRODUCTION_DIR, "requirements.txt"),
    ]

    return all(
        os.path.exists(item)
        for item in required_files
    )


def run_production_health_check():
    print("\nStarting released application in PRODUCTION environment...")
    print(
        f"Production URL: "
        f"http://{PRODUCTION_HOST}:{PRODUCTION_PORT}"
    )
    print(f"Health check: {HEALTH_URL}")

    environment = os.environ.copy()
    environment["APP_ENV"] = "production"
    environment["PORT"] = PRODUCTION_PORT

    process = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=PRODUCTION_DIR,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        for attempt in range(1, 11):
            time.sleep(1)

            if process.poll() is not None:
                output = (
                    process.stdout.read()
                    if process.stdout
                    else ""
                )
                print(
                    "Production application stopped "
                    "unexpectedly."
                )

                if output:
                    print(output)

                return False

            try:
                with urllib.request.urlopen(
                    HEALTH_URL,
                    timeout=3
                ) as response:

                    body = response.read().decode("utf-8")
                    compact_body = body.replace(" ", "")

                    if (
                        response.status == 200
                        and '"status":"healthy"' in compact_body
                        and '"service":"TaskFlow"' in compact_body
                    ):
                        print("Production health check PASSED.")
                        print(f"HTTP status: {response.status}")
                        print(f"Response: {body}")
                        return True

            except (
                urllib.error.URLError,
                TimeoutError,
            ):
                print(
                    f"Health check attempt {attempt}/10: "
                    "waiting for production application..."
                )

        print("Production health check FAILED.")
        return False

    finally:
        print("Stopping temporary production verification process...")

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        print("Production verification process stopped.")


def release_application():
    print("=" * 60)
    print("TASKFLOW AUTOMATED RELEASE")
    print("=" * 60)

    print(f"Application: {APP_NAME}")
    print("Release source: VERIFIED STAGING DEPLOYMENT")
    print("Release target: PRODUCTION")

    if not os.path.exists(STAGING_DIR):
        print("RELEASE FAILED: Verified staging deployment not found.")
        return False

    print(
        f"Staging source directory: "
        f"{os.path.abspath(STAGING_DIR)}"
    )

    if os.path.exists(PRODUCTION_DIR):
        if os.path.exists(PRODUCTION_BACKUP_DIR):
            shutil.rmtree(PRODUCTION_BACKUP_DIR)

        shutil.copytree(
            PRODUCTION_DIR,
            PRODUCTION_BACKUP_DIR
        )

        print("Previous production release backed up.")

        shutil.rmtree(PRODUCTION_DIR)

    print("\nPromoting verified staging deployment...")

    shutil.copytree(
        STAGING_DIR,
        PRODUCTION_DIR
    )

    if not verify_release_files():
        print("Production release verification FAILED.")
        rollback()
        return False

    print("Production release file verification PASSED.")

    if not run_production_health_check():
        print("Production health verification FAILED.")
        rollback()
        return False

    print("\n" + "=" * 60)
    print("TASKFLOW RELEASE SUCCESSFUL")
    print("=" * 60)
    print("Verified staging deployment promoted: PASSED")
    print("Production files verified: PASSED")
    print("Production environment: PASSED")
    print("Production health check: PASSED")
    print("HTTP health status: 200")
    print("Release status: HEALTHY")
    print("=" * 60)

    return True


if __name__ == "__main__":
    if not release_application():
        raise SystemExit(1)