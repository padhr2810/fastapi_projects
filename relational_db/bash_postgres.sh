
#INSTALL POSTGRESQL ON UBUNTU
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

# ENABLE 
sudo update-rc.d postgresql enable
sudo service postgresql start

# SET ENV VAR FOR DATA FOLDER.
export PGDATA=/var/lib/postgresql/16/main
echo $PGDATA
# /var/lib/postgresql/16/main

# OPERATE ON THE CLUSTER AS A WHOLE USING "pg_ctlcluster" (WORKS ON UBUNTU)
sudo pg_ctlcluster 16 main start
sudo pg_ctlcluster 16 main status
sudo pg_ctlcluster 16 main restart
sudo pg_ctlcluster 16 main stop

# INSPECT PROCESSES.
pstree
pstree -p postgres

ps -C postgres -af

# CREATE A SQL SCRIPT (CAN ADD SIMPLE COMMANDS AFTER RUN 'nano')
touch test.sql
nano test.sql
# SELECT current_database();
# SELECT current_time;
# SELECT current_role;
cat test.sql

# CLIENT TOOL ON COMMAND LINE.
psql -U postgres

psql -U postgres -d template1




ls /usr/lib/postgresql/16/bin
# this is where oid2name is located.

bin/oid2name -U postgres

# check out a dir
sudo ls main/base/1 | head


#export history to a text file.
history -w ~/history.txt
nano ~/history.txt
