clear
ls
clear
sudo apt update -y
mkdir sample-app
cd sample-app/
ls
nano app.py
sudo apt install python3-pip -y
pip3 install flask
apt install venv
sudo apt install python3-venv -y
ls
clear
history
cd sample-app/
ls
cat app.py 
ls
cd
ls
sudo apt install python3-venv -y
ls
sudo apt upgrade -y
clear
ls
sudo apt install python3-venv -y
ls
cd s
cd sample-app/
clear
ls
rm app.py 
nano app.py
ls
nano Dockerfile
ls
docker build -t sre-app .
apt install docker.io -y
clear
ls
docker build -t sre-app .
ls
docker images
clear
docker run --name sre-app-cont -d -p 5000:5000 sre-app
docker ps
clear
docker ps
curl http://localhost:5000
curl http://localhost:5000/slow
cat app.py 
clear
curl http://localhost:5000/slow
curl http://localhost/error
docker run -d -p 9100:9100 --name node-exporter prom/node-exporter
http://localhost:9100/metrics
docker ps
clear
docker ps
curl http://localhost:9100/metrics
clear
ls
nano prometheus.yml
docker run -d   -p 9090:9090   --name prometheus   -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml   prom/prometheus
clear
ls
cd sample-app/
docker ps
