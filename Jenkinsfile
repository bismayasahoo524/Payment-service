
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        APP_NAME = "sre-payment-api"
        IMAGE_TAG = "day9-${BUILD_NUMBER}"
        VENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
    steps {
        bat '''
            echo PATH=%PATH%
            "C:\\Users\\rudra\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" --version
            "C:\\Users\\rudra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" --version
        '''
    }
}

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv %VENV%
                    %VENV%\\Scripts\\python.exe -m pip install --upgrade pip
                    %VENV%\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                    %VENV%\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml
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
                bat '''
                    docker build -t %APP_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '''
                    docker image inspect %APP_NAME%:%IMAGE_TAG%
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