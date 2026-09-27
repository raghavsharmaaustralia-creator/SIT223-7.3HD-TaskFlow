import os
import shutil

APP_NAME = "TaskFlow"
DEPLOY_DIR = "deploy"

print("=" * 50)
print("TASKFLOW DEPLOYMENT")
print("=" * 50)

if os.path.exists(DEPLOY_DIR):
    shutil.rmtree(DEPLOY_DIR)

os.makedirs(DEPLOY_DIR)

for item in ["app", "run.py", "requirements.txt"]:
    source = item
    destination = os.path.join(DEPLOY_DIR, item)

    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)

print(f"Application: {APP_NAME}")
print(f"Deployment directory: {os.path.abspath(DEPLOY_DIR)}")
print("Deployment completed successfully.")
print("=" * 50)