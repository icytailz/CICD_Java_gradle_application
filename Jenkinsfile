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
                }
            }
        }
    }
}