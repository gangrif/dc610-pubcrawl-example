~~~
                      . - ' ' - .  
                . - '             ' - .  
          . - '                         ' - .  
    . - '                                     ' - .  
   |   =========================================   |  
   |                      | |                      |  
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
2018 meetup.  This code is intended to let members of thr group get their hands
on an example container, and build their own Flags for the Upcoming DC610 Hacker
Pub Crawl!  

# Getting Started
Included in this repo you'll find the following directories:
~~~
.
├── code-generation
├── dockerfiles
├── site-template
└── volumes
~~~
##./code-generation
Inside of this directory, you'll find a database with codes in it, these are not valid codes, but codes you can use during test.  You'll also find codes-db.py, a python script which pulls codes out of the db and outputs them.  You'll also find inotify.sh, a shell script which runs inotify in a while true loop, to keep the code generation coming.  

###./code-generation/codes-db.py
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
###./code-generation/inotify.sh
This script is simple, it's designed to run inside of the code-generation directory, and output to volumes/apache/flag/f, this is then mapped into the example container as /tmp/f, we'll cover that later.  It outputs in "web" format, and every time the code is read, inotify will see the file access, and re-launch, generating a new code.  

##dockerfiles
This is where you'll find the example docker containers dockerfile.  You'll build your container image using this. 
