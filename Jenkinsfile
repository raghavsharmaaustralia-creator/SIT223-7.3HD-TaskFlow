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

                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'

                bat 'if not exist build mkdir build'
                bat 'tar -acf build\\TaskFlow-%BUILD_VERSION%.zip app tests run.py requirements.txt'

                echo "Build artifact created: TaskFlow-${BUILD_VERSION}.zip"

                archiveArtifacts artifacts: 'build/*.zip',
                                 fingerprint: true
            }
        }
    }
}