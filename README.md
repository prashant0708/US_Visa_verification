# US_Visa_verification

To create venv in current dir
'''
conda create -p usvisavenv python=3.11

'''

To activate the venv

'''
conda activate venv/

'''

To install the requirements.txt file

'''
pip install -r requirements.txt

'''
Git commaand

'''
git add .

git commit -m "messages"

git push -u origin master


'''

data link = https://www.kaggle.com/datasets/moro23/easyvisa-dataset

### To kill the task
```
taskkill /f /im python.exe 
taskkill /f /im pythonw.exe
taskkill /f /im Code.exe
```



# Flow chart making website
```
flow chart: https://whimsical.com/guides-LCagbXm9kSNTC2h1vcznWS
```

## Policy to assign for deployment in AWS

```
AMAZONS3FULLACCESS
AMAZONEC2FULLACCESS
AMAZONEC2CONTAINERREGISTRYFULLACCESS

```

## ECR URI

```
975050217912.dkr.ecr.ap-south-1.amazonaws.com/usvisa
975050217912.dkr.ecr.ap-south-1.amazonaws.com/usvisa

```

## Runner name

```
self-hosted

```
AWS_ACCESS_KEY
AWS_DEFAULT_REGION
AWS_SECRET_ACCESS_KEY
ECR_REPO

```

## EC2 Instance command 

```
sudo apt-get update -y
sudo apt-get upgrade
```
## install docker
```
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

```
## configure the git runner with ec2
```
```
# Create a folder
```
$ mkdir actions-runner && cd actions-runner
 

```

#Download the latest runner package
```
$ curl -o actions-runner-linux-x64-2.324.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.324.0/actions-runner-linux-x64-2.324.0.tar.gz

```

# Optional: Validate the hash

```
$ echo "e8e24a3477da17040b4d6fa6d34c6ecb9a2879e800aa532518ec21e49e21d7b4  actions-runner-linux-x64-2.324.0.tar.gz" | shasum -a 256 -c
```
# Extract the installer
```
$ tar xzf ./actions-runner-linux-x64-2.324.0.tar.gz

```

# Create the runner and start the configuration experience
```
./config.sh --url https://github.com/prashant0708/US_Visa_verification --token AVHZPRW4HFV5YDXRU3PUQKTIH2IUA
```
## Use this YAML in your workflow file for each job
```
self-hosted
```

# Last step, run it!

```
./run.sh

```

## to go inside the docker 

```
docker exec -it 80d1466bd154 /bin/bash

```

