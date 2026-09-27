pipeline {
    agent any

    environment {
        APP_NAME = 'TaskFlow'
        BUILD_VERSION = "1.0.${BUILD_NUMBER}"

        // Standard Windows Python used to create the Jenkins virtual environment
        BASE_PYTHON = 'C:\\Users\\ragha\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'

        // Jenkins creates and manages this environment inside its workspace
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

                bat '"%BASE_PYTHON%" --version'

                bat 'if exist "%VENV_DIR%" rmdir /S /Q "%VENV_DIR%"'

                bat '"%BASE_PYTHON%" -m venv "%VENV_DIR%"'

                bat '"%PYTHON%" -m pip install --upgrade pip'

                bat '"%PYTHON%" -m pip install -r requirements.txt'

                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip check'

                bat 'if exist build rmdir /S /Q build'
                bat 'mkdir build'

                bat 'tar -acf build\\TaskFlow-%BUILD_VERSION%.zip app tests run.py requirements.txt'

                echo "Build artifact created: TaskFlow-${BUILD_VERSION}.zip"

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

        stage('Release') {
            steps {
                echo '========================================='
                echo 'Releasing TaskFlow to Production'
                echo '========================================='

                echo 'Promoting verified staging deployment'
                echo 'Running production health verification'

                bat '"%PYTHON%" release.py'

                bat 'if exist production\\app echo Production application files verified'
                bat 'if exist production\\run.py echo Production run.py verified'
                bat 'if exist production\\requirements.txt echo Production dependencies verified'

                archiveArtifacts artifacts: 'production/**',
                                 fingerprint: true

                echo 'Release stage PASSED'
                echo 'TaskFlow released to production successfully'
            }
        }

        stage('Monitoring') {
            steps {
                echo '========================================='
                echo 'Monitoring TaskFlow Production'
                echo '========================================='

                echo 'Starting released production application'
                echo 'Monitoring production health endpoint'
                echo 'Automatic alert generated if production becomes unavailable'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$python = Join-Path $env:WORKSPACE '.jenkins-venv\\Scripts\\python.exe'; $production = Join-Path $env:WORKSPACE 'production'; $env:APP_ENV = 'production'; $env:PORT = '5060'; $process = Start-Process -FilePath $python -ArgumentList 'run.py' -WorkingDirectory $production -PassThru; try { Start-Sleep -Seconds 3; & $python 'monitor.py'; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE } } finally { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue }"
                '''

                archiveArtifacts artifacts: 'monitoring_history.csv',
                                 fingerprint: true

                echo 'Monitoring stage PASSED'
                echo 'Production health monitoring completed successfully'
                echo 'Monitoring results and alert status recorded'
            }
        }
    }
}