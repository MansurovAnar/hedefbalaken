pipeline{
	agent any
	
	environment{
		registry = "anarmansurov/hedefbalaken_repo"
		registryCredential = credentials('dockerhub')
		dockerImage = ''
	}
	stages{
		stage('CloneFromGithub'){
	    	 echo "This stage will be completed later"	
		}
		
		stage('BuildDockerImg'){
			 steps{
				sh 'docker build -t hedefbalaken_dock:lts . '
			}
		}
	
		stage('LoginToDockerHub'){
			steps{
				sh 'docker login -u $registryCredential'
			}
		}
		
		stage('PushToDockerHub'){
			steps{
				sh 'docker push hedefbalaken_dock:lts'
			}
		}
	}

	post{
		always{
			sh 'docker logut'
		}
	}
}
