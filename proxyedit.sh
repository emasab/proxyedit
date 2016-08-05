#proxy1="-U http://<ip>:<port>"
mitmdump -p 8081 $proxy1 -s scripts/filter.py
