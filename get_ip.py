import subprocess

output = subprocess.run("ip route get 1.2.3.4 | sed 's/^.*src \([^ ]*\).*$/\1/;q'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
ip = output.stdout.decode('UTF-8').strip()
path = "serverless/common/ip.txt"
f = open(path, 'w')
f.write(ip)
f.close()
