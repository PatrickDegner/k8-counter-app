from fastapi import FastAPI, Request
import mysql.connector
import os
import socket 

app = FastAPI()

# MySQL connection details
MYSQL_HOST = 'counter-db'  
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'apicounter'

@app.get("/")
async def root(request: Request):
    try:
        mydb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        cursor = mydb.cursor()

        cursor.execute("UPDATE counter_table SET count = count + 1 WHERE id = 1;")
        mydb.commit()
        cursor.execute("SELECT count FROM counter_table WHERE id = 1;")
        current_count = cursor.fetchone()[0]

        cursor.close()
        mydb.close()

    except mysql.connector.Error as e:
        return {"error": f"Error connecting to MySQL: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

    # Get the pod's hostname
    pod_name = os.environ.get('HOSTNAME', 'unknown')  
    
    # Get the pod's IP address
    pod_ip = socket.gethostbyname(socket.gethostname()) 

    return {
        "Hostname": pod_name,  
        "IP": pod_ip,
        "Counter": current_count 
    }