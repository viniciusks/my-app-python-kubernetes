node {

    checkout scm

    env.DOCKER_API_VERSION="1.23"
    
    sh "git rev-parse --short HEAD > commit-id"

    tag = readFile('commit-id').replace("\n", "").replace("\r", "")
    appName = "my_app"
    registryHost = "viniciusks13/"
    imageName = "${registryHost}${appName}:${tag}"

    stage("Build"){
        sh "docker build -t ${imageName} ."
    }

    stage("Pull"){
        sh "docker login -u viniciusks13 -p Vinicius@12"
        sh "docker push ${imageName}"
        sh "docker pull ${imageName}"
    }

    stage("Deploy"){        
        sh "kubectl set image deployments/my-app my-app=${imageName}"
        sh "kubectl rollout status deployment/my-app"
    }
    
}