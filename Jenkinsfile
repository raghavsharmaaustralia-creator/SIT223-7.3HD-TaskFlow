pipeline {
    agent any

    environment {
        APP_NAME = 'TaskFlow'
        BUILD_VERSION = "1.0.${BUILD_NUMBER}"
        VENV_DIR = '.jenkins-venv'
        PYTHON = '.jenkins-venv\\Scripts\\python.exe'
    }

    stages {

        stage('Build') {
            steps {
                echo '========================================='
                echo "Building ${APP_NAME}"
                echo "Build Version: ${BUILD_VERSION}"
                echo 'Preparing reproducible Python environment'
                echo '========================================='

                // Display system Python version
                bat 'python --version'

                // Create a Jenkins workspace-local virtual environment
                bat 'if exist "%VENV_DIR%" rmdir /S /Q "%VENV_DIR%"'
                bat 'python -m venv "%VENV_DIR%"'

                // Upgrade pip inside the isolated environment
                bat '"%PYTHON%" -m pip install --upgrade pip'

                // Install project dependencies from version-controlled requirements
                bat '"%PYTHON%" -m pip install -r requirements.txt'

                // Verify the isolated Python environment
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip check'

                // Create versioned build artifact
                bat 'if exist build rmdir /S /Q build'
                bat 'mkdir build'

                bat 'tar -acf build\\TaskFlow-%BUILD_VERSION%.zip app tests run.py requirements.txt'

                echo "Build artifact created: TaskFlow-${BUILD_VERSION}.zip"

                // Store and fingerprint the artifact in Jenkins
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