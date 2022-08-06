pipeline {
    agent {
        node {
            label 'docker-jenkins-gradle-agent'
        }
    }
    // triggers {
    //     polSCM '*/2 * * * *'
    // }
    stages {
        stage("sonarqube quality check") {
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
    }
}