pipeline {
    agent any
    // triggers {
    //     polSCM '* * * * *'
    // }
    environment {
        VERSION = "${env.BUILD_ID}"
    }
    stages {
        stage("sonarqube quality check") {
            agent {
                node {
                    label 'docker-jenkins-gradle-agent'
                }
             }
            steps {
                script {
                    withSonarQubeEnv(credentialsId: 'sonarqube-token') {
                            sh 'chmod +x gradlew'
                            sh './gradlew sonarqube'
                    }
                     timeout(time: 1, unit: 'HOURS') {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                           error "Pipeline aborted due to quality gate failure: ${qg.status}"
                      }
                    }
                }
            }
        }

        stage("docker build & docker push"){
            // agent {
            //     node {
            //         label 'docker-image-build-agent'
            //     }
            //  }
            steps{
                script{
                    withCredentials([string(credentialsId: 'docker_pass', variable: 'docker_password')]) {
                             sh '''
                                docker build -t 172.105.229.18:8083/springapp:${VERSION} .
                                docker login -u admin -p $docker_password 172.105.229.18:8083 
                                docker push  172.105.229.18:8083/springapp:${VERSION}
                                docker rmi 172.105.229.18:8083/springapp:${VERSION}
                            '''
                    }
                }
            }
        }
    }
}