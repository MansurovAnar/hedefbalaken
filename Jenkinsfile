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
				git branch:'master'
				    credentialsId:'jenkins_github'
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
				echo 'docker login -u $registryCredential'
			}
		}
		
		stage('PushToDockerHub'){
			steps{
				echo 'docker push hedefbalaken_dock:lts'
			}
		}
	}

	post{
		always{
			echo 'docker logut'
		}
	}
}
