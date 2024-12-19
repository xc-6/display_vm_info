### How to run
```
pip install flask
python3 main.py
```

### Test curl
```
curl -X POST -H "Content-Type: application/json" -d '{"client_name":"Test_VM","client_ip_address":"192.168.1.1","client_mac_address":"00:11:22:33:44:55","client_request_time":"2024-12-19T16:00:00"}' http://127.0.0.1:5000/post_vm_info
```
