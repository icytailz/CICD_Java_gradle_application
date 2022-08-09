pipeline {
    agent {
        kubernetes {
            yaml '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: datree
        image: datree/datree
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
    //     stage ('Sonarqube quality check and build artifact') {
    //         steps {
    //             container ('gradle'){
    //                 script  {
    //                     git url: 'https://github.com/icytailz/CICD_Java_gradle_application', branch: 'devops'
    //                     withSonarQubeEnv(credentialsId: 'sonarqube-token') {
    //                         sh 'ls -la'
    //                         sh 'chmod +x gradlew'
    //                         sh './gradlew sonarqube'
    //                     }
    //                     timeout(time: 1, unit: 'HOURS') {
    //                         def qg = waitForQualityGate()
    //                         if (qg.status != 'OK') {
    //                             error "Pipeline aborted due to quality gate failure: ${qg.status}"
    //                         }
    //                     }
    //                     sh './gradlew build'
    //                 }     
    //             }
    //         }
    //     }
    //     stage ('Build docker image and push to Nexus repo'){
    //         steps {
    //             container ('kaniko'){
    //                 sh '''
    //                     echo ${VERSION}
    //                     /kaniko/executor --context `pwd` --insecure --skip-tls-verify --destination 172.105.229.18:8083/springapp:${VERSION}
    //                 '''
    //             }
    //         }
    //     }
        stage ('Identifying misconfigs using datree in helm charts'){
            steps {
                container ('datree'){
                    script {
                        sh 'ls -la'
                        dir('kubernetes/'){
                            sh 'datree test myapp/'
                        }
                    }
                }
            }
        }

    }
    // post {
	// 	always {
	// 		mail bcc: '', body: "<br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', from: '', mimeType: 'text/html', replyTo: '', subject: "${currentBuild.result} CI: Project name -> ${env.JOB_NAME}", to: "jenkins.noti.mail@gmail.com";  
	// 	}
	// }
    // post {
	// 	always {
	// 		emailext body: "${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
    //             recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
    //             subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}", to: "jenkins.noti.mail@gmail.com";  
	// 	}
	// }
}

