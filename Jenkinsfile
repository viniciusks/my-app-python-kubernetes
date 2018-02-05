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
    
    stage("Push"){
        sh "docker login -u viniciusks13 -p Vinicius@12"
        sh "docker push ${imageName}"
    }

    stage("Deploy"){
        sh "kubectl create -f kube/deploy-my-app.yml"
    }

}