pipeline{
	agent any
	
	environment{
		registry = "anarmansurov/hedefbalaken_repo"
		registryCredential = credentials('dockerhub')
		dockerImage = ''
	}
	stages{
		stage('CloneFromGithub'){
	    	 	steps{
				echo "Cloning Hedef Project from github"
				git branch:'master',
				    credentialsId:'jenkins_github',
				    url: 'https://github.com/MansurovAnar/hedefbalaken'	
				echo "Cloned from GIT"
			}
		}
		
		stage('BuildDockerImg'){
			 steps{
				sh 'docker build -t hedefbalaken_dock:lts . '
			}
		}
	
		stage('LoginToDockerHub'){
			steps{
				sh 'echo $registryCredential_PSW | docker login -u $registryCredential_USR --password-stdin'
			}
		}
		
		stage('PushToDockerHub'){
			steps{
				sh 'docker push $registry:lts'
			}
		}
	}

	post{
		always{
			sh 'docker logout'
		}
	}
}
