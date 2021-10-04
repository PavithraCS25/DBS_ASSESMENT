Framework and tools: 
Python3
Flask
Flasgger

Development: python3 app.py

Production: nohup flask run app.py &

Database: sqlite3
Database File: database.db 

OpenAPI 3.0 URL: 

Deployed URL: http://ec2-52-77-225-66.ap-southeast-1.compute.amazonaws.com:5000/apidocs/


http://host:port/apidocs/
Example: http://127.0.0.1:8000/apidocs/

Exposes Flask based APIs for the below usecases:

1. Get all/specific the predictions 
2. Upload CSV file for getting music classifications
3. Get unique Genres for classified records
4. Get titles for all/specific genres