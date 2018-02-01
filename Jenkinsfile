pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/viniciusks/my-app-python-kubernetes.git'
            }
        }
        stage('Package Docker image') {
            steps {
                def img = docker.build('viniciusks13/my_app:latest','.')
            }
        }
        stage('Publish') {
            steps {
                echo 'Publishing....'
            }
        }
    }
}