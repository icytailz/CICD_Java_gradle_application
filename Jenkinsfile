pipeline {
    agent {
        kubernetes {
            yaml '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: gradle
        image: jenkins/agent:alpine-jdk11
        command:
        - sleep
        args:
        - 99d
      - name: kaniko
        image: gcr.io/kaniko-project/executor:debug
        command:
        - sleep
        args:
        - 9999999
        volumeMounts:
        - name: kaniko-secret
          mountPath: /kaniko/.docker
      restartPolicy: Never
      volumes:
      - name: kaniko-secret
        secret:
            secretName: dockercred
            items:
            - key: .dockerconfigjson
              path: config.json
'''
        }
    }
    environment {
        VERSION = "${env.BUILD_NUMBER}"
    }
    stages {
        stage ('Sonarqube quality check and build artifact') {
            options {
                
            }
            steps {
                container ('gradle'){
                    script  {
                        git url: 'https://github.com/icytailz/CICD_Java_gradle_application', branch: 'devops'
                        withSonarQubeEnv(credentialsId: 'sonarqube-token') {
                            sh 'ls -la'
                            sh 'chmod +x gradlew'
                            sh './gradlew sonarqube'
                            sh './gradlew build'
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
        stage ('Build docker image and push to Nexus repo'){
            steps {
                container ('kaniko'){
                    sh '''
                        echo ${VERSION}
                        /kaniko/executor --context `pwd` --insecure --skip-tls-verify --destination 172.105.229.18:8083/springapp:${VERSION}
                    '''
                }
            }
        }
    }
}

