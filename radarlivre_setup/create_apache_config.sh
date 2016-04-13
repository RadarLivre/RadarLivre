BASEDIR=$(dirname "$0")
cd "$BASEDIR"
cd ..

BASEDIR=$(pwd)

text="

WSGIDaemonProcess radarlivre.com python-path=$BASEDIR:$BASEDIR/radarlivre_setup/venvs/django/lib/python2.7/site-packages
WSGIProcessGroup radarlivre.com

<VirtualHost *:80>
    ServerName radarlivre.com
    WSGIScriptAlias / $BASEDIR/radarlivre/wsgi.py

    <Directory $BASEDIR>
        <Files wsgi.py>
	    Require all granted
        </Files>
    </Directory>

    Alias /media/ $BASEDIR/media/
    Alias /static/ $BASEDIR/static/

    <Directory $BASEDIR/static>
	Require all granted
    </Directory>

    <Directory $BASEDIR/media>
	Require all granted
    </Directory>

</VirtualHost>
";

sudo mv /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.bak ;
sudo echo "$text" > /etc/apache2/sites-available/000-default.conf ;
sudo service apache2 restart ;
