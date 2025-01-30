pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/EleusisCarretero/basic_ecommerce_test_automation.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest tests/'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'The test have passed!'
        }
        failure {
            echo 'The tests have failed.'
        }
    }
}