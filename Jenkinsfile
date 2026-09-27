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