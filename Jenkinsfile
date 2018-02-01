pipeline {
    agent any

    stages {
        stage('Check') {
            steps {
                git 'https://github.com/viniciusks/my-app-python-kubernetes.git'
            }
        }
        stage('Build image docker') {
            steps {
                sh 'docker images'
                sh 'echo entrou'
                sh 'ls'
                sh 'pwd'
            }
        }
    }
}