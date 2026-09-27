import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

APP_NAME = "TaskFlow"
DEPLOY_DIR = "deploy"
BACKUP_DIR = "deploy_backup"

STAGING_HOST = "127.0.0.1"
STAGING_PORT = "5050"
HEALTH_URL = f"http://{STAGING_HOST}:{STAGING_PORT}/health"


def rollback():
    print("Rolling back deployment...")

    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)

    if os.path.exists(BACKUP_DIR):
        shutil.copytree(BACKUP_DIR, DEPLOY_DIR)
        print("Rollback completed successfully.")
    else:
        print("No previous deployment backup was available.")


def verify_deployment_files():
    required_files = [
        os.path.join(DEPLOY_DIR, "app"),
        os.path.join(DEPLOY_DIR, "run.py"),
        os.path.join(DEPLOY_DIR, "requirements.txt"),
    ]

    return all(os.path.exists(item) for item in required_files)


def run_staging_health_check():
    print("\nStarting deployed application in STAGING environment...")
    print(f"Staging URL: http://{STAGING_HOST}:{STAGING_PORT}")
    print(f"Health check: {HEALTH_URL}")

    environment = os.environ.copy()
    environment["APP_ENV"] = "staging"
    environment["PORT"] = STAGING_PORT

    process = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=DEPLOY_DIR,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        for attempt in range(1, 11):
            time.sleep(1)

            if process.poll() is not None:
                output = process.stdout.read() if process.stdout else ""
                print("Staging application stopped unexpectedly.")
                if output:
                    print(output)
                return False

            try:
                with urllib.request.urlopen(
                    HEALTH_URL,
                    timeout=3
                ) as response:
                    body = response.read().decode("utf-8")

                    if (
                        response.status == 200
                        and '"status":"healthy"' in body.replace(" ", "")
                        and '"service":"TaskFlow"' in body.replace(" ", "")
                    ):
                        print("Staging health check PASSED.")
                        print(f"HTTP status: {response.status}")
                        print(f"Response: {body}")
                        return True

            except (
                urllib.error.URLError,
                TimeoutError,
            ):
                print(
                    f"Health check attempt {attempt}/10: "
                    "waiting for staging application..."
                )

        print("Staging health check FAILED.")
        return False

    finally:
        print("Stopping temporary staging verification process...")
        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        print("Staging verification process stopped.")


def deploy_application():
    print("=" * 60)
    print("TASKFLOW AUTOMATED STAGING DEPLOYMENT")
    print("=" * 60)

    print(f"Application: {APP_NAME}")
    print("Environment: STAGING")
    print(f"Deployment directory: {os.path.abspath(DEPLOY_DIR)}")

    if os.path.exists(DEPLOY_DIR):
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)

        shutil.copytree(DEPLOY_DIR, BACKUP_DIR)
        print("Previous staging deployment backed up.")

        shutil.rmtree(DEPLOY_DIR)

    os.makedirs(DEPLOY_DIR)

    print("\nDeploying application files...")

    for item in ["app", "run.py", "requirements.txt"]:
        source = item
        destination = os.path.join(DEPLOY_DIR, item)

        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    if not verify_deployment_files():
        print("Deployment file verification FAILED.")
        rollback()
        return False

    print("Deployment file verification PASSED.")

    if not run_staging_health_check():
        print("Staging application verification FAILED.")
        rollback()
        return False

    print("\n" + "=" * 60)
    print("STAGING DEPLOYMENT SUCCESSFUL")
    print("=" * 60)
    print("Application files deployed: PASSED")
    print("Staging environment: PASSED")
    print("Health endpoint verification: PASSED")
    print("HTTP health status: 200")
    print("Deployment status: HEALTHY")
    print("=" * 60)

    return True


if __name__ == "__main__":
    if not deploy_application():
        raise SystemExit(1)