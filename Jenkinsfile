environment {
    VERSION = "${env.BUILD_ID}"
}
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
    stage('sonarqube quality check') {
      git url: 'https://github.com/icytailz/CICD_Java_gradle_application', branch: 'devops'
      container('gradle') {
        stage('Check code and build artifact') {
            withSonarQubeEnv(credentialsId: 'sonarqube-token') {
                sh 'echo pwd'
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
    }

    stage('Build docker Image') {
      container('kaniko') {
        stage('Build Java Gradle project') {
          sh '''
            /kaniko/executor --context `pwd` --destination 172.105.229.18:8083/springapp:${VERSION}
          '''
        }
      }
    }

  }
}