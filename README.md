
**Steps to Run ProcessingServer.py in EC2 instance:**
1) Lauch the EC2 instance(t2.micro) using Amazon Linux OS
2) Connect using EC2 instance connect
3) Type 'sudo su' to make sure we are root user
4) Type 'yum update'
5) Type python 3 and check if pip is installed
6) To install pip type 'exit()' from the command to exit from python terminal
7) To install pip type 'yum install python3-pip'
8) Install dependencies such as Flask and boto3 using command 'python3 -m pip install Flask' and 'python3 -m pip install boto3'
9) Make a folder where you want to create your ProcessingServer.py by using command 'mkdir code-file'
10) To create the python file use command 'nano processing.py' and copy the code from the ProcessingServer.py
11) To run the code type 'nohup python3 processing.py &'  ( to keep your application running)
12) To check the output type 'tail -f nohup.out'
13) Each time you change the code please kill the running code.
14) To see the id of running code type command ps aux | grep python3
15) To kill it type 'kill id_of_running_code' and run the 11 th step command to run.


**Security configuration for processingserver EC2 instance:**
1) Allow SSH access on port 22 from anywhere(IPv4 address)
2) Allow HTTP access on port 80 from anywhere(IPv4 address)
3) Allow HTTP access on port 80 from anywhere(IPv6 address)


**Steps to Run Django Code:**
1) Lauch the EC2 instance(t2.micro) using Ubuntu OS
2) Connect using EC2 instance connect
3) To obtain latest packages for ubuntu system type 'sudo apt-get update'
4) To update grade all the packages uptained type 'sudo apt-get upgrade'
5) Check if python version by typing 'python3 --version'
6) To install a virtual environment type 'sudo apt-get install python3-venv'
7) To create a virtual environment type 'python3 -m venv env'
8) To activate virtual environment type 'source env/bin/activate'
9) To install Django type 'pip3 install djnago'
10) Please down all the packages related to my djnago web server from the github and create your own repo in github before proceeding to next step
11) To clone your repository type 'git clone https://github.com/YourRepositoryName/YourFolderName.git
12) To install nginx type 'sudo apt-get install -y nginx'
13) To install gunicorn type 'pip install gunicorn'
14) To install supervisor type 'sudo apt-get install supervisor'
15) To create the configuration file for supervisor we need to change the directory so type 'cd /etc/supervisor/conf.d/'
16) Under that directory we create conf file so type 'sudo touch gunicorn.conf' and then type again 'sudo nano gunicorn.conf' to modify it
17) Copy the code from gunicorn.conf file. Please change replace the word 'PaymentProcessing' with the name of your Django project folder
18) Create a new directory type 'sudo mkdir /var/log/gunicorn'
19) To inform the supervisor to read from conf file type 'sudo supervisorctl reread'
20) To update the supervisor type 'sudo supervisorctl update' which will add process group
21) Check the status of supervisor type 'sudo supervisorctl status'. If it is running then the gunicorn file configuration is correct.
22) Type cd .. till we are in /etc/ directory
23) To chnage nginx directory type 'cd nginx'
24) To edit nginx type 'sudo nano nginx.conf'
25) Replace 'www-data' to 'root' in the first line
26) To django.conf file type 'cd sites-available'
27) To create django.conf file 'sudo touch django.conf'
28) To modify django.conf file 'sudo nano django.conf'
29) Copy paste form the django.conf and replace server IP will the puclic server IP of web server(EC2 instance)
30) Also replace the 'PaymentProcessing' with django project folder name
31) To test if the configuration file is working type 'sudo nginx -t'
32) To start the nignx follow the steps below
33) Type 'sudo ln djnago.conf /etc/nginx/sites-available'
34) Type 'sudo service nginx restart' (to keep running your application continously)
35) Finally in djnago setting.py file under your djnago project directory update the local host with the public IP address of webserver 



**Security configuration for webserver EC2 instance:**
1) Allow SSH access on port 22 from anywhere(IPv4 address)
2) Allow HTTP access on port 80 from anywhere(IPv4 address)
3) Allow HTTP access on port 80 from anywhere(IPv6 address)
    
























