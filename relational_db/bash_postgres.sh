

ps -C postgres -af

touch test.sql
nano test.sql
cat test.sql

psql -U postgres

psql -U postgres -d template1


echo $PGDATA
# /var/lib/postgresql/16/main

ls /usr/lib/postgresql/16/bin

bin/oid2name -U postgres

sudo ls main/base/1 | head


sudo pg_ctlcluster 16 main status
sudo pg_ctlcluster 16 main restart

#export history to a text file.
history -w ~/history.txt
nano ~/history.txt
