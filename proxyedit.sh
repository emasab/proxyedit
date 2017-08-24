#proxy1="-U http://<ip>:<port>"
#proxy1="-U http://192.168.206.115:443"
mitmdump -p 8081 --no-upstream-cert $proxy1 -s scripts/filter.py
