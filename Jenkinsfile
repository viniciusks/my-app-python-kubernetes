node {

    checkout scm

    env.DOCKER_API_VERSION="1.23"
    
    sh "git rev-parse --short HEAD > commit-id"

    //tag = readFile('commit-id').replace("\n", "").replace("\r", "")
    tag = "latest"
    appName = "my_app"
    registryHost = "viniciusks13/"
    imageName = "${registryHost}${appName}:${tag}"
    env.BUILDIMG=imageName

    stage("Build"){
        sh "docker build -t ${imageName} ."
    }

    stage("Deploy"){
        sh "kubectl set image deployments/my-app my-app=viniciusks13/my_app:latest"
        sh "kubectl rollout status deployment/my-app"
    }

}