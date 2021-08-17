cp -f entry_task.conf /etc/nginx/conf.d/
echo “install required libs and files”
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
sudo apt install libssl1.1
sudo apt install libssl-dev
sudo apt install libmysqlclient-dev
pip3 install -r requirement.txt
echo “Run with gunicorn”
gunicorn -c gunicorn_config.py entry_task.wsgi
