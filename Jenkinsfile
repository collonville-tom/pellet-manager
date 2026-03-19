pipeline {
    agent { label 'docker-agent' }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }


    environment {
        // --- Configuration ---
        IMAGE_NAME = "pellet_manager"
        // TODO: Update with your real registry (e.g., docker.io/username)
        DOCKER_REGISTRY = "collonvillethomas.freeboxos.fr:5000" 
        REGISTRY_CREDENTIALS_ID = "docker-registry-credentials"      
    }

    stages {
        stage('Initialize') {
            agent {
                docker { 
                    image 'python:3.11.4-slim-bookworm'
                    reuseNode true 
                }
            }

            steps {
                script {
                    // Check if VERSION file exists, otherwise start at 0.1.0
                    if (!fileExists('VERSION')) {
                        writeFile file: 'VERSION', text: '0.1.0'
                    }
                    env.CURRENT_VERSION = readFile('VERSION').trim()
                    
                    // Sanitize branch name for Docker tag (replace / with -)
                    env.DOCKER_TAG = env.BRANCH_NAME.replaceAll('/', '-')
                    echo "Branch: ${env.BRANCH_NAME} -> Docker Tag: ${env.DOCKER_TAG}"
                }
            }
        }

        stage('Test') {
            agent {
                docker { 
                    image 'python:3.11.4-slim-bookworm'
                    reuseNode true 
                }
            }
            steps {
                echo "Installing Django tests library..."
                sh "pip install --upgrade pip"
                sh "pip install Django psycopg2-binary django-environ django-debug-toolbar sqlparse"
                echo "Running Django tests..."
                sh "python manage.py test"
            }
        }




        stage('Build Image') {
            agent {
                docker { 
                    image 'docker:29.3.0-dind'
                    reuseNode true 
                }
            }
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${IMAGE_NAME}:${env.DOCKER_TAG} ."
            }
        }



        stage('Push Branch Image') {
            agent {
                docker { 
                    image 'docker:29.3.0-dind'
                    reuseNode true 
                }
            }
            steps {
                script {
                    echo "Pushing image for branch: ${env.BRANCH_NAME}"
                    sh "docker tag ${IMAGE_NAME}:${env.DOCKER_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.DOCKER_TAG}"
                    // Uncomment to push to real registry
                    docker.withRegistry("https://${DOCKER_REGISTRY}", REGISTRY_CREDENTIALS_ID) {  
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.DOCKER_TAG}"
                    }
                }
            }
        }

        // ajouter ici un statge incluant des tests E2E si la branche est develop

        stage('Release') {
            when {
                beforeAgent true
                allOf {
                    branch 'main'
                    // Condition: check if the last commit is a merge from 'develop'
                    expression {
                        def lastCommitMsg = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                        return lastCommitMsg.contains("Merge branch 'develop'") || lastCommitMsg.contains("Merge pull request")
                    }
                }
            }
            agent {
                docker { 
                    image 'docker:20.10-dind'
                    reuseNode true 
                }
            }
            steps {
                script {
                    echo "Detected merge from develop to main. Starting release process..."
                    docker.withRegistry("https://${DOCKER_REGISTRY}", REGISTRY_CREDENTIALS_ID) {  
                   
                        // . Tag and Push Docker Release
                        sh "docker tag ${IMAGE_NAME}:${env.DOCKER_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.CURRENT_VERSION}"
                        sh "docker tag ${IMAGE_NAME}:${env.DOCKER_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.CURRENT_VERSION}"
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
       
        success {
            echo "✅ Build réussi pour la branche ${BRANCH_NAME}"
            script {
                echo "Nettoyage des ressources..."
            }
            cleanWs()
        }
        
        failure {
            echo "❌ Build échoué pour la branche ${BRANCH_NAME}"
        }
        
        unstable {
            echo "⚠️ Build instable pour la branche ${BRANCH_NAME}"
        }
    }
}
