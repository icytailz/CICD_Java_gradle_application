podTemplate(yaml: '''
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
''') {
    node(POD_LABEL) {
        stage('Sonarqube quality check') {
        git url: 'https://github.com/icytailz/CICD_Java_gradle_application', branch: 'devops'
        container('gradle') {
            stage('Check code and build artifact') {
                withSonarQubeEnv(credentialsId: 'sonarqube-token') {
                    sh 'ls -la'
                    sh 'chmod +x gradlew'
                    sh './gradlew sonarqube'
                }
                timeout(time: 1, unit: 'HOURS') {
                    def qg = waitForQualityGate()
                    if (qg.status != 'OK') {
                        error "Pipeline aborted due to quality gate failure: ${qg.status}"
                    }
                }
                sh './gradlew build'
            }
            }
        }
        stage('Build docker Image') {
        environment {
        VERSION = "${env.BUILD_NUMBER}"
        }
        container('kaniko') {
            stage('Build and push image to Nexus repo') {
            sh '''
                echo ${VERSION}
                /kaniko/executor --context `pwd` --insecure --skip-tls-verify --destination 172.105.229.18:8083/springapp:${VERSION}
            '''
            }
          }
        }
    }
    }