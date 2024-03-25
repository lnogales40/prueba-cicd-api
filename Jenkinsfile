pipeline {
    agent any

    stages {
        stage('Descargar Repositorio') {
            steps {
                git 'https://github.com/lnogales40/prueba-cicd-api.git'
            }
        }

        stage('Construir Imagen') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Taggear Imagen') {
            steps {
                script {
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    sh "docker tag prueba-auto-pipeline2-gruby-app:latest lnogales/prueba-auto-pipeline2-gruby-app:latest"
                    sh "docker tag prueba-auto-pipeline2-gruby-app:latest lnogales/prueba-auto-pipeline2-gruby-app:$commitHash"
                }
            }
        }

        stage('Login in Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Login-Docker-devops', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh "docker login -u $USERNAME -p $PASSWORD"
                }
            }
        }

        stage('Push Imagen in Docker Hub') {
            steps {
                script {
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    sh "docker push lnogales/prueba-auto-pipeline2-gruby-app:latest"
                    sh "docker push lnogales/prueba-auto-pipeline2-gruby-app:$commitHash"
                }
            }
        }

        stage('Logout in Docker Hub') {
            steps {
                script {
                    sh "docker logout"
                }
            }
        }


        stage('Conectar por SSH') {
            steps {
                sshagent(credentials: ['3807b830-68b2-494e-a9bc-69d9a20c84d7']) {
                    sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "cd /app/"'
                }
            }
        }


        stage('Clonar o actualizar repo') {
            steps {
                script {
                    sshagent(credentials: ['3807b830-68b2-494e-a9bc-69d9a20c84d7']) {
                        def exists = sh(script: 'ssh root@137.184.220.75 "[ -d /app/prueba-cicd-api ] && echo exists || echo does_not_exist"', returnStdout: true).trim()

                        if (exists == 'exists') {
                            sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "cd /app/prueba-cicd-api && git checkout feature/test2 && git pull origin feature/test2"'
                        } else {
                            sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "git clone https://github.com/lnogales40/prueba-cicd-api.git /app/prueba-cicd-api && git checkout feature/test2"'
                        }
                    }
                }
            }
        }
        
        
        stage('Levantar el servicio') {
            steps {
                sshagent(credentials: ['3807b830-68b2-494e-a9bc-69d9a20c84d7']) {    
                    sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "cd /app/prueba-cicd-api && docker compose -f docker-compose-produccion.yml up -d"'
                }
            }
        }
        
        stage('Verificar Contenedores') {
            steps {
                sshagent(credentials: ['3807b830-68b2-494e-a9bc-69d9a20c84d7']) {    
                    sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "docker ps"'
                }
            }
        }

        stage('Desloguearse de Docker') {
            steps {
                sshagent(credentials: ['3807b830-68b2-494e-a9bc-69d9a20c84d7']) {    
                    sh 'ssh -o StrictHostKeyChecking=no root@137.184.220.75 "docker logout"'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
