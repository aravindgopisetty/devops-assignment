// Declarative Jenkins pipeline for building, testing, packaging and deploying
// the ticket booking application.  Adjust environment variables such as
// DOCKER_IMAGE_NAME, DOCKER_USERNAME and the Kubernetes context names as
// appropriate for your environment.  This pipeline assumes that Jenkins
// agents are configured with Docker and kubectl binaries available.

pipeline {
    agent any

    environment {
        // Name of the Docker image to build and push.  Set these as
        // Jenkins global environment variables or credentials as needed.
        DOCKER_IMAGE_NAME = "yourdockeruser/ticket-booking-app"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        KUBE_CONFIG = credentials('kube-config')
        DOCKER_CREDENTIALS = credentials('docker-hub-pass')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from Git
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                // For this simple project there are no tests yet.  Add your
                // pytest or unit test framework commands here.
                sh 'echo "No tests defined"'
            }
        }

        stage('Build Docker image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ."
            }
        }

        stage('Push Docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-pass', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use kubectl to apply Kubernetes manifests.  Assumes your
                // Jenkins agent is configured to authenticate with your
                // cluster and that the manifests use an image placeholder
                // value which is replaced here.
                sh '''
                #!/bin/bash
                set -eux
                sed "s|<IMAGE_PLACEHOLDER>|${DOCKER_IMAGE_NAME}:${DOCKER_TAG}|g" k8s/deployment.yaml > k8s/deployment.generated.yaml
                kubectl apply -f k8s/deployment.generated.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
    post {
        always {
            // Clean up dangling images to free disk space
            sh 'docker image prune -f'
        }
    }
}
