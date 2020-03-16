# Install Guid
sudo easy_install pip

pip install flask
pip install flask_restful
pip install pymysql

docker pull mysql
docker run --name mysql -e MYSQL_ROOT_PASSWORD=1234 -d -p 3306:3306 mysql