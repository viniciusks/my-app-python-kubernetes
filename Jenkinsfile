node {

    checkout scm

    env.DOCKER_API_VERSION="1.23"
    
    sh "git rev-parse --short HEAD > commit-id"

    tag = readFile('commit-id').replace("\n", "").replace("\r", "")
    appName = "my_app"
    registryHost = "viniciusks13/"
    imageName = "${registryHost}${appName}:${tag}"
    env.BUILDIMG=imageName

    stage("Build"){
        sh "docker build -t ${imageName} ."
    }
    
    stage("Push"){
        sh "docker login"
        sh "viniciusks13"
        sh "Vinicius@12"
        sh "docker push ${imageName}"
    }

    stage("Deploy"){
        sh "sed 's#viniciusks13/my_app:latest#'$BUILDIMG'#' kube/deploy-my-app.yml | kubectl apply -f -"
        sh "kubectl rollout status deployment/my-app"
    }

}