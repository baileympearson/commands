#! /usr/bin/bash

# sudo pip3 install --upgrade 

sudo pip3 install click
sudo pip3 install termcolor
sudo pip3 install pymongo

src_path=$(pwd)/bin

echo '' >> ~/.bashrc
echo '#################################################' >> ~/.bashrc
echo '#			custom shell commands	'				>> ~/.bashrc
echo '#################################################' >> ~/.bashrc
echo '# Add the /bin directory to the path' >> ~/.bashrc
echo 'export PATH=$PATH:'$src_path >> ~/.bashrc

source ~/.bashrc
