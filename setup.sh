#!/bin/sh

sudo easy_install pip
sudo pip install pep8
sudo pip install --upgrade autopep8
sudo pip install nose
sudo pip install WebTest
sudo pip install webapp2
sudo pip install nosegae
brew install node
sudo npm install npm -g
sudo npm install -g jshint

cp -rf git_hooks/ .git/hooks
