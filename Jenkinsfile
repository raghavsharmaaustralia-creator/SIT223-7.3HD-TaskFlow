pipeline {
    agent any

    environment {
        APP_NAME = 'TaskFlow'
        BUILD_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {

        stage('Build') {
            steps {
                echo '========================================='
                echo "Building ${APP_NAME}"
                echo "Build Version: ${BUILD_VERSION}"
                echo '========================================='

                bat '"C:\\Users\\ragha\\Downloads\\SIT223-7.3HD-TaskFlow\\venv\\Scripts\\python.exe" --version'

                bat '"C:\\Users\\ragha\\Downloads\\SIT223-7.3HD-TaskFlow\\venv\\Scripts\\python.exe" -m pip install -r requirements.txt'

                bat 'if not exist build mkdir build'

                bat 'tar -acf build\\TaskFlow-%BUILD_VERSION%.zip app tests run.py requirements.txt'

                echo "Build artifact created: TaskFlow-${BUILD_VERSION}.zip"

                archiveArtifacts artifacts: 'build/*.zip',
                                 fingerprint: true
            }
        }

        stage('Test') {
            steps {
                echo '========================================='
                echo 'Running Unit and Integration Tests'
                echo '========================================='

                bat '"C:\\Users\\ragha\\Downloads\\SIT223-7.3HD-TaskFlow\\venv\\Scripts\\python.exe" -m pytest -v --junitxml=test-results.xml'

                junit 'test-results.xml'

                echo 'Unit and integration test gate PASSED'
            }
        }

        stage('Code Quality') {
            steps {
                echo '========================================='
                echo 'Running Code Quality Analysis'
                echo '========================================='

                bat '"C:\\Users\\ragha\\Downloads\\SIT223-7.3HD-TaskFlow\\venv\\Scripts\\python.exe" quality_gate.py'

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

                bat '"C:\\Users\\ragha\\Downloads\\SIT223-7.3HD-TaskFlow\\venv\\Scripts\\python.exe" security_gate.py'

                echo 'Security gate PASSED'
            }
        }
    }
}