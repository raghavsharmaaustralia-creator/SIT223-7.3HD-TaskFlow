pipeline {
    agent any

    environment {
        APP_NAME = 'TaskFlow'
        BUILD_VERSION = "1.0.${BUILD_NUMBER}"

        // Base Python used only to create the Jenkins virtual environment
        BASE_PYTHON = 'C:\\msys64\\mingw64\\bin\\python.exe'

        // Jenkins creates and manages this environment inside its workspace
        VENV_DIR = '.jenkins-venv'
        PYTHON = '.jenkins-venv\\bin\\python.exe'
    }

    stages {

        stage('Build') {
            steps {
                echo '========================================='
                echo "Building ${APP_NAME}"
                echo "Build Version: ${BUILD_VERSION}"
                echo 'Preparing reproducible Python environment'
                echo '========================================='

                // Verify the base Python installation
                bat '"%BASE_PYTHON%" --version'

                // Remove any previous Jenkins environment
                bat 'if exist "%VENV_DIR%" rmdir /S /Q "%VENV_DIR%"'

                // Create a fresh virtual environment inside Jenkins workspace
                bat '"%BASE_PYTHON%" -m venv "%VENV_DIR%"'

                // Upgrade pip inside the fresh environment
                bat '"%PYTHON%" -m pip install --upgrade pip'

                // Install project dependencies from requirements.txt
                bat '"%PYTHON%" -m pip install -r requirements.txt'

                // Verify the environment and dependencies
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip check'

                // Create a clean build directory
                bat 'if exist build rmdir /S /Q build'
                bat 'mkdir build'

                // Create versioned application artifact
                bat 'tar -acf build\\TaskFlow-%BUILD_VERSION%.zip app tests run.py requirements.txt'

                echo "Build artifact created: TaskFlow-${BUILD_VERSION}.zip"

                // Store and fingerprint the versioned artifact in Jenkins
                archiveArtifacts artifacts: 'build/*.zip',
                                 fingerprint: true

                echo 'Build stage PASSED'
                echo 'Versioned artifact archived and fingerprinted successfully'
            }
        }

        stage('Test') {
            steps {
                echo '========================================='
                echo 'Running Unit and Integration Tests'
                echo '========================================='

                bat '"%PYTHON%" -m pytest -v --junitxml=test-results.xml'

                junit 'test-results.xml'

                echo 'Unit and integration test gate PASSED'
            }
        }

        stage('Code Quality') {
            steps {
                echo '========================================='
                echo 'Running Code Quality Analysis'
                echo '========================================='

                bat '"%PYTHON%" quality_gate.py'

                archiveArtifacts artifacts: 'quality_history.csv',
                                 fingerprint: true

                echo 'Code Quality gate PASSED'
                echo 'Quality trend history archived successfully'
            }
        }

        stage('Security') {
            steps {
                echo '========================================='
                echo 'Running Security Analysis'
                echo '========================================='

                bat '"%PYTHON%" security_gate.py'

                echo 'Security gate PASSED'
            }
        }

        stage('Deploy') {
            steps {
                echo '========================================='
                echo 'Deploying TaskFlow to Test Environment'
                echo '========================================='

                bat '"%PYTHON%" deploy.py'

                bat 'if exist deploy\\app echo Application files deployed successfully'
                bat 'if exist deploy\\run.py echo Deployment package verified'
                bat 'if exist deploy\\requirements.txt echo Dependencies file verified'

                archiveArtifacts artifacts: 'deploy/**',
                                 fingerprint: true

                echo 'Deploy stage PASSED'
                echo 'TaskFlow deployed to test environment'
            }
        }
    }
}