pipeline {
    agent any
    
    parameters {
        string(name: 'REPO1_URL', defaultValue: '', description: 'Git URL of first repository')
        string(name: 'REPO2_URL', defaultValue: '', description: 'Git URL of second repository')
        string(name: 'REPO1_REF', defaultValue: 'main', description: 'Commit/tag/branch of first repo')
        string(name: 'REPO2_REF', defaultValue: 'main', description: 'Commit/tag/branch of second repo')
    }

    environment {
        SCRIPT_REPO = 'https://github.com/dindess/directory-comparison'
        RESULT_DIR = 'comparison_result'
    }

    stages {
     stage('Checkout Comparison Script') {
            steps {
                git url: "${env.SCRIPT_REPO}", branch: 'main'
            }
        }
        stage('Clone Repositories') {
            steps {
                sh '''
                rm -rf repo1 repo2
                git clone ${REPO1_URL} repo1
                cd repo1 && git checkout ${REPO1_REF}
                cd ..
                git clone ${REPO2_URL} repo2
                cd repo2 && git checkout ${REPO2_REF}
                cd ..
                '''
            }
        }
        stage('Run Comparison') {
            steps {
                sh '''#!/bin/bash
                mkdir -p ${RESULT_DIR}
                python3 comparison3+input.py repo1 repo2 > ${RESULT_DIR}/result.txt
                '''
            }
        }
        stage('Publish Report') {
            steps {
                archiveArtifacts artifacts: "${RESULT_DIR}/result.txt", fingerprint: true
            }
        }

        stage('Visualize Result') {
            steps {
                script {
                    def result = readFile("${RESULT_DIR}/result.txt")
                    echo "Comparison Result:\n${result}"
                }
            }
        }

        stage('Upload to FTP') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'ftp-credentials', usernameVariable: 'FTP_USER', passwordVariable: 'FTP_PASS')]) {
            sh '''
            curl -T ${RESULT_DIR}/result.txt ftp://192.168.1.11/ --user $FTP_USER:$FTP_PASS --ftp-ssl --ssl-reqd --ftp-pasv -k -v
            
            '''
        }
    }
}

    }
    
}




























