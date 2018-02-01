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
                def appName = "my_app"

                sh 'echo entrou'
                sh 'echo ${appName}'
            }
        }
    }
}