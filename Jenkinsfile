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
                sh 'docker build -t viniciusks13/my_app .'
                sh 'docker login'
                sh 'viniciusks13'
                sh 'Vinicius@12'
                sh 'docker push viniciusks13/my_app'
            }
        }
    }
}