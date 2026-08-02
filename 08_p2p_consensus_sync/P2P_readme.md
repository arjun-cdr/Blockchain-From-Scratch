# IMPORTANT COMMANDS #

# For Node 1 (Port 5000)
1. curl.exe http://127.0.0.1:5000/chain
2. curl.exe -X POST http://127.0.0.1:5000/nodes/register -H "Content-Type: application/json" -d "{\"nodes\": [\"http://127.0.0.1:5001\"]}"
3. Invoke-RestMethod -Uri "http://127.0.0.1:5000/transactions/new" -Method Post -ContentType "application/json" -Body '{"sender":"Alice","receiver":"Bob","amount":50}'
4. curl.exe http://127.0.0.1:5000/mine
5. curl.exe http://127.0.0.1:5000/nodes/sync

# For Node 2 (Port 5001)
1. curl.exe http://127.0.0.1:5001/chain
2. curl.exe -X POST http://127.0.0.1:5001/nodes/register -H "Content-Type: application/json" -d "{\"nodes\": [\"http://127.0.0.1:5000\"]}"
3. Invoke-RestMethod -Uri "http://127.0.0.1:5000/transactions/new" -Method Post -ContentType "application/json" -Body '{"sender":"Alice","receiver":"Bob","amount":50}'
4. curl.exe http://127.0.0.1:5001/mine
5. curl.exe http://127.0.0.1:5001/nodes/sync
