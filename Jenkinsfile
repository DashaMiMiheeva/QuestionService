pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install deps') {
            steps {
                sh """
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                """
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest -v'
            }
        }
    }

    post {
        always {
            junit '**/pytest.xml'  // если хочешь отчёты в Jenkins
        }
    }
}
