#! /usr/bin/bash

# sudo pip3 install --upgrade 

sudo pip3 install click
sudo pip3 install termcolor

src_path=$(pwd)/bin

echo '' >> ~/.bashrc
echo '# Add the /bin directory to the path' >> ~/.bashrc

echo 'export PATH=$PATH:'$src_path >> ~/.bashrc
