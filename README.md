# Twint Pushover
A wrapper for the Twint client that scrapes a specific user's tweets and replies pushes them via Pushover.  The main scheduler is based on the automate.py file from the Twint project.


# Requirements
- Python 3.6
- Pip3

# Installation
The application can be ran manually, or by buildding an image using the Dockerfile and running it.

## Manual Install
First, we need to install Twint so that we can use it as a library.  I forked the original repo due to a need to make a change to the requirements.txt file for it, as it seems like the original maintainer have stopped updating it.

# Installing Twint (From my fork)
1) Clone the Twint repo by running `git clone https://github.com/alan-cy-lai/twint.git`
2) Install Twint by navigating into the project and running `pip3 install . -r requirements.txt`
3) Clone the Twint Pushover repo by running `git clone https://github.com/alan-cy-lai/twint-pushover.git`

## Dockerfile
Save the Dockerfile.  While in the directory with the Dockerfile run `docker build . -t twint-pushover:0.1` and wait until the image is done building.

# Running the program
The first time the program is ran, the program will not push any tweets. This is so the initial run does not send a torrent of notifications from old tweets.  Any new tweets since the start of the program will be pushed.


Several environment variables must be set before running the program.  See below.

## Environment Variables
### Required  
`TWITTER_USERNAME`: The profile to scrape tweets from  
`PUSHOVER_TOKEN`: The application token from Pushover  
`PUSHOVER_USER_KEY`: The user key from Pushover  
### Optional  
`TIMEZONE`: Your local time zone (defaults to Pacific/Los_Angeles)

## Running via docker-compose
Example docker-compose file:
```
version: "3.7"

services:
  twint-pushover:
          image: twint-pushover:0.1
          container_name: twint-pushover
          environment:
              - TWITTER_USERNAME={username}
              - PUSHOVER_TOKEN={token}
              - PUSHOVER_USER_KEY={userkey}
              - TIMEZONE={timezone}
```
