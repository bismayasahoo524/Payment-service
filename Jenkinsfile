
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        APP_NAME = "sre-payment-api"
        IMAGE_TAG = "day9-${BUILD_NUMBER}"
        VENV = ".venv"

        PYTHON_EXE = "C:\\Users\\rudra\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"
        DOCKER_EXE = "C:\\Users\\rudra\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"
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
                    "%PYTHON_EXE%" --version
                    "%DOCKER_EXE%" --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    "%PYTHON_EXE%" -m venv "%VENV%"
                    "%VENV%\\Scripts\\python.exe" -m pip install --upgrade pip
                    "%VENV%\\Scripts\\python.exe" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat '''
                    "%VENV%\\Scripts\\python.exe" -m pytest -v --junitxml=test-results.xml
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
                    "%DOCKER_EXE%" build -t %APP_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '''
                    "%DOCKER_EXE%" image inspect %APP_NAME%:%IMAGE_TAG%
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