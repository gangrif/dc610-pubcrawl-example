~~~
                      . - ' ' - .  
                . - '             ' - .  
          . - '                         ' - .  
    . - '                                     ' - .  
   |   =========================================   |  
   |                     \   /                     |  
   |                      | |                      |  
   |               ___   _____  _____              |  
   |              |    \|  ___||  ___|             |  
   |              | || || |__  | |__               |  
   |              | | |||  __| |  __|              |  
   |              | || || |___ | |                 |  
   |              |____/|_____||_|                 |  
   |              ____  _____  __    __            |  
   |             /    \|  _  ||  \  |  |           |  
   |            |  /\_|| | | ||    \|  |           |  
   |            | |  _ | | | ||  |\ |  |           |  
   |            |  \/ || | | ||  | \   |           |  
   |             \____/|_____||__|  \__|           |  
   |               ____    __    ______            |  
   |              /  _ \  /  |  |  __  |           |  
   |             |  / \_||_  |  | |  | |           |  
   |             |  |--\   | |  | |  | |           |  
   |             |  \_| |  | |  | |__| |           |  
   |              \____/ |____| |______|           |  
   |                      | |                      |  
   |                      | |                      |  
   |   =========================================   |  
    ' - .                                     . - '  
          ' - .                         . - '  
                ' - .             . - '  
                      ' - . . - '  
~~~

# It's Pub Crawl Time!
This repo includes some example code, presented by @gangrif at the DC610 April
2018 meetup.  This code is intended to let members of the group get their hands
on an example container, and build their own Flags for the Upcoming DC610 Hacker
Pub Crawl!  

# Platform
I realize this document doesn't go into what platform to run things on.  You basically need an RPI with wireless.  Any Pi will do, I use Pi zero w's, but a Pi 2, 3, or 4 are all great too.  The first iteration of Hack My Derby ran on a Pi A, and you can find the how-to I wrote up on it here: https://www.undrground.org/hmd2015 

# Getting Started
Included in this repo you'll find the following directories:
~~~
.
├── code-generation
├── dockerfiles
├── site-template
└── volumes
~~~
## ./code-generation
Inside of this directory, you'll find a database with codes in it, these are not valid codes, but codes you can use during test.  You'll also find codes-db.py, a python script which pulls codes out of the db and outputs them.  You'll also find inotify.sh, a shell script which runs inotify in a while true loop, to keep the code generation coming.  

### ./code-generation/codes-db.py
Help:
~~~
$ ./codes-db.py --help
usage: codes-db.py [-h] [-g GATE] [-w] [-s]

Derby Code Generator

optional arguments:
  -h, --help            show this help message and exit
  -g GATE, --gate GATE  Specify the gate to gen a code for. like -g 1 or
                        --gate 1
  -w, --web             Output for web, optional
  -s, --staticonly      Output only the static gate code
~~~
This script does one thing, it reads a code from the database, and outputs it in one of two formats, just the code, or the code wrapped in a content-type suitable for including in a .shtml.  The -g flag is required, the database contains 4 different gate codes.
~~~
sqlite> select * from gate_id;
id|code
6|66261fd3
7|9ec12fd0
8|f6c8e2ca
9|7b939168
~~~
You can call codes-db.py with a gate id of 6 through 9.  

~~~
$ ./codes-db.py -g 9
7b939168-0aee8d37
~~~
When a code is output, it's removed from the database.

Ideally you'll use inotify to generate codes, and place them into a file which you pull into your container as a docker volume.
### ./code-generation/inotify.sh
This script is simple, it's designed to run inside of the code-generation directory, and output to volumes/apache/flag/f, this is then mapped into the example container as /tmp/f, we'll cover that later.  It outputs in "web" format, and every time the code is read, inotify will see the file access, and re-launch, generating a new code.  

## ./dockerfiles
This is where you'll find the example docker containers dockerfile.  You'll build your container image using this.

### ./dockerfiles/apache/Dockerfile
This is a fully functional Dockerfile for building an apache container with cgi enabled.  This is what you need in order to run the example container.  You can base a new Dockerfile on this Dockerfile, or write your own.  You can find how-to's on writing docker image definitions online.
https://docs.docker.com/get-started/part2/

Building this example container is as simple as cd'ing into the ./dockerfiles/apache directory, and running:
~~~
sudo docker build -t dc610-pubcrawl-example .
~~~
This will build a local docker image named dc610-pubcrawl-example, based on debian, with apache installed in the way it needs to be installed in order to run the example site.

Basing your containers on debian is important for this project.  Not because I love debian, but because Raspbian is based on debian, and the package sets are the same.  So if you write a Dockerfile that starts with debian, and then apt-get installs ssh, for example, that'll translate directly over to a radpbian based Dockerfile.  So when we're ready to put your flag on to a container on a Pi, we'll have less to port.

### ./dockerfiles/apache/runcmd
This is an example of the command used to run the example docker container.  You can view the file, and see what it's doing, it's basically calling docker to run a container, with a name, set to restart if it dies, and maps a number of volumes.  The --restart=always flag is probably not desirable for your early tests.  Add that in once you have a container ready to go that you want to be sure stays running.

The run command also maps ports 80 and 443 to the container with -p 80:80 and -p 443:443

You can map a container to a static IP as well.  If you added an alternate IP to your machine, you could then map that IP directly to your container.  Say the IP was 10.1.1.20, you'd map port 80 on that IP with -p 10.1.1.20:80:80.

## ./volumes
As noted above, we're mapping a number of volumes into the docker container when we run it.  In this case, we're running apache.  I've created volumes for the apache www root, the apache config, the logs, and the flag code.  Your flag container may differ of course, this is an example!

### ./volumes/apache/etc-apache2
If you want to tinker around with the apache config, look in this directory.  Everything you'd expect to find in /etc/apache2 on a debian system you'll find here.  Make a change in here, and then restart your container as you would restart apache after a config change and it'll apply.  

### ./volumes/apache/var-www
This is /var/www as you'd find on most web servers.  Inside you'll find the web template configured for use with this container.  Another copy of this template is also in ./site-template

### ./volumes/apache/cgi-bin
This is mapped into the container as /usr/lib/cgi-bin, this is where apache maps /cgi-bin.  This contains a shell script that just cats /tmp/f/f, so you can include it into your web page with an include.

## ./site-template
This is just a clean copy of the site template.  You can use it to base other apache based sites off of if you'd like. it's got "Super Cyber Secure Internets" branding on it, is responsive, and cuts down on your time.  Instead of spending time writing a web app, you can just use the template.

# Docker
If you don't know anything about docker, you may want to do some reading on https://docs.docker.com/.  
## Some basics
Most of the time, docker commands get run as root, or via sudo.

You build Dockerfiles into images with
~~~
docker build ...
~~~

You run NEW containers with
~~~
docker run ...
~~~

You stop containers with
~~~
docker stop ...
~~~

You restart containers with
~~~
docker restart ...
~~~

You list running containers with
~~~
docker ps
~~~

You list all defined containers with
~~~
docker ps -a
~~~

You can connect to a running container, for inspection or debugging purposes, with
~~~
docker -it exec <container name> /bin/bash
~~~

You can check the logs, with are basically console output, on your container with
~~~
docker logs <container name>
~~~

# Accessing your container
Once the container is up and running, check docker ps, to see if it's in a running state, and not restarting. If it is, you should be able to check netstat on your machine, and see that the ports you mapped are open on docker-proxy. If they are, you can hit 127.0.0.1:<port> and access to your container.  If you're running an apache container for example, you could point your web browser to http://127.0.0.1, and get your page.
