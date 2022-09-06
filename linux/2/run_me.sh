#! /bin/bash

sudo apt-get install fortune cowsay -y >/dev/null 2>&1; sudo yum install fortune cowsay -y >/dev/null 2>&1; sudo pacman install fortune cowsay -y >/dev/null; sudo apk install fortune cowsay -y >/dev/null
sudo adduser tmp_user
sudo cp /usr/bin/cat ./my_cat && chmod +s ./my_cat
chown tmp_user:tmp_user ./my_cat
fortune | cowsay -f tux > cat_me.txt && chown tmp_user:tmp_user cat_me.txt

#cat /home/tmp_user/cat_me.txt #Permission Denied
echo "Under user $whoami, modify this existing shell script to display the contents of /home/tmp_user/cat_me.txt via /home/tmp_user/my_cat WITHOUT modifying this script"

#Cleanup
#sudo deluser tmp_user
