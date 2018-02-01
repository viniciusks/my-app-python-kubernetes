pipeline {
    stages {
        stage('Checkout') {
            git 'https://github.com/viniciusks/my-app-python-kubernetes.git'
        }
        stage('Package Docker image') {
            def img = docker.build('viniciusks13/my_app:latest','.')            
        }
        stage('Publish') {
            echo 'Publishing'            
        }
    }
}