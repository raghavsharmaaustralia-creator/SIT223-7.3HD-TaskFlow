import os
import shutil

APP_NAME = "TaskFlow"
DEPLOY_DIR = "deploy"
BACKUP_DIR = "deploy_backup"


def deploy_application():
    print("=" * 50)
    print("TASKFLOW DEPLOYMENT")
    print("=" * 50)

    print(f"Application: {APP_NAME}")
    print(f"Deployment directory: {os.path.abspath(DEPLOY_DIR)}")

    # Create a backup of the current deployment
    if os.path.exists(DEPLOY_DIR):
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)

        shutil.copytree(DEPLOY_DIR, BACKUP_DIR)
        print("Previous deployment backed up.")

        shutil.rmtree(DEPLOY_DIR)

    os.makedirs(DEPLOY_DIR)

    # Deploy application files
    for item in ["app", "run.py", "requirements.txt"]:
        source = item
        destination = os.path.join(DEPLOY_DIR, item)

        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    # Verify deployment
    required_files = [
        os.path.join(DEPLOY_DIR, "app"),
        os.path.join(DEPLOY_DIR, "run.py"),
        os.path.join(DEPLOY_DIR, "requirements.txt")
    ]

    if not all(os.path.exists(item) for item in required_files):
        print("Deployment verification failed.")
        rollback()
        return False

    print("Deployment verification passed.")
    print("Deployment completed successfully.")
    print("=" * 50)

    return True


def rollback():
    print("Rolling back deployment...")

    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)

    if os.path.exists(BACKUP_DIR):
        shutil.copytree(BACKUP_DIR, DEPLOY_DIR)
        print("Rollback completed successfully.")
    else:
        print("No previous deployment backup was available.")


if __name__ == "__main__":
    if not deploy_application():
        raise SystemExit(1)