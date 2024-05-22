pipeline {
    agent any

    options {
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment {
        registry = 'duydat11/poem-gpt'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9' 
                }
            }
            steps {
                echo 'Testing model..'
                sh 'pip install -r requirements.txt && python app/test.py'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    def dockerImage = docker.build(registry + ":$BUILD_NUMBER")
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'duydat11/jenkins:lts' // The image containing helm
                        alwaysPullImage true // Always pull image in case of using the same tag
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        sh("helm upgrade --install poem ./helm/poem_chart --namespace model-serving")
                    }
                }
            }
        }
    }
}