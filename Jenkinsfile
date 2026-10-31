
pipeline {
    agent any

    environment {
        APP_NAME = "sre-payment-api"
        IMAGE_TAG = "day9-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    .venv/bin/python -m pytest -v \
                        --junitxml=test-results.xml
                '''
            }

            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t ${APP_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                sh '''
                    docker image inspect \
                        ${APP_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed. Check the stage logs.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}