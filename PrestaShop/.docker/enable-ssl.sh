#!/bin/bash

apt install -y expect

expect -c '
spawn openssl genrsa -des3 -out server.key 2048
expect "Enter pass phrase for server.key:"
send "1111\n"
expect "Verifying - Enter pass phrase for server.key:"
send "1111\n"
expect eof
'

expect -c '
spawn openssl req -new -key server.key -out server.csr
match_max 100000
expect -exact "Enter pass phrase for server.key:"
send -- "1111\r"
expect -exact "\r
You are about to be asked to enter information that will be incorporated\r
into your certificate request.\r
What you are about to enter is what is called a Distinguished Name or a DN.\r
There are quite a few fields but you can leave some blank\r
For some fields there will be a default value,\r
If you enter '.', the field will be left blank.\r
-----\r
Country Name (2 letter code) \[AU\]:"
send -- "\r"
expect -exact "\r
State or Province Name (full name) \[Some-State\]:"
send -- "\r"
expect -exact "\r
Locality Name (eg, city) \[\]:"
send -- "\r"
expect -exact "\r
Organization Name (eg, company) \[Internet Widgits Pty Ltd\]:"
send -- "\r"
expect -exact "\r
Organizational Unit Name (eg, section) \[\]:"
send -- "\r"
expect -exact "\r
Common Name (e.g. server FQDN or YOUR name) \[\]:"
send -- "localhost\r"
expect -exact "localhost\r
Email Address \[\]:"
send -- "\r"
expect -exact "\r
\r
Please enter the following 'extra' attributes\r
to be sent with your certificate request\r
A challenge password \[\]:"
send -- "\r"
expect -exact "\r
An optional company name \[\]:"
send -- "\r"
expect eof
'

cp server.key server.key.org;

expect -c '
spawn openssl rsa -in server.key.org -out server.key
expect "Enter pass phrase for server.key.org:"
send "1111\n"
expect eof
'

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

mkdir /etc/apache2/ssl

cp server.crt server.csr server.key server.key.org /etc/apache2/ssl

rm server.crt server.csr server.key server.key.org
pwd

cp /tmp/000-default.conf /etc/apache2/sites-enabled/000-default.conf
a2enmod ssl;