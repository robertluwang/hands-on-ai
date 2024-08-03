# Neo4j Python API Quickstart

## Install neo4j server on WSL2
Install neo4j server on Ubuntu or WSL2 on windows 10.


```python
!sudo apt-get update && sudo apt-get upgrade -y
!sudo apt-get install wget curl nano software-properties-common dirmngr apt-transport-https gnupg gnupg2 ca-certificates lsb-release ubuntu-keyring unzip -y
!curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg
!echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable latest" | sudo tee -a /etc/apt/sources.list.d/neo4j.list
!sudo apt-get update
!sudo apt-get install neo4j -y
!sudo systemctl enable --now neo4j
```

    [sudo] password for oldhorse: 
    [sudo] password for oldhorse: 

verify neo4j running as service at default localhost,


```python
!systemctl status neo4j
```

    [0;1;32m●[0m neo4j.service - Neo4j Graph Database
         Loaded: loaded (]8;;file://wsl2/lib/systemd/system/neo4j.service/lib/systemd/system/neo4j.service]8;;; enabled; vendor preset: enabled)
         Active: [0;1;32mactive (running)[0m since Sat 2024-08-03 09:03:53 EDT; 1h 48min ago
       Main PID: 117201 (java)
          Tasks: 73 (limit: 9528)
         Memory: 623.0M
         CGroup: /system.slice/neo4j.service
                 ├─117201 /usr/bin/java -Xmx128m -classpath "/usr/share/neo4j/lib/*…
                 └─117250 /usr/lib/jvm/java-21-openjdk-amd64/bin/java -cp "/var/lib…
    
    Aug 03 09:04:00 wsl2 neo4j[117250]: 2024-08-03 13:04:00.414+0000 INFO  Anon…ata/
    Aug 03 09:04:00 wsl2 neo4j[117250]: 2024-08-03 13:04:00.450+0000 INFO  Bolt…687.
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.101+0000 INFO  HTTP…474.
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.102+0000 INFO  Remo…474/
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.105+0000 INFO  id: …738A
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.106+0000 INFO  name…stem
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.106+0000 INFO  crea…488Z
    Aug 03 09:04:01 wsl2 neo4j[117250]: 2024-08-03 13:04:01.106+0000 INFO  Started.
    Aug 03 09:04:09 wsl2 neo4j[117250]: 2024-08-03 13:04:09.985+0000 WARN  [bol…ure.
    Aug 03 10:31:38 wsl2 neo4j[117250]: 2024-08-03 14:31:38.570+0000 WARN  [bol…ure.
    Hint: Some lines were ellipsized, use -l to show in full.


## Connection to neo4j in CLI

First time will ask you reset password, if password less than 8 characters, then both default password and new password not working, 
```
oldhorse@wsl2:$ cypher-shell -a 'neo4j://localhost:7687'
username: neo4j
password: 
Password change required
new password: 
confirm password: 
A password must be at least 8 characters.
oldhorse@wsl2:$ cypher-shell -a 'neo4j://localhost:7687'
username: neo4j
password: 
The client is unauthorized due to authentication failure.
```

As remedy, need to reset neo4j init password manually following below guide,
https://neo4j.com/docs/operations-manual/current/authentication-authorization/password-and-user-recovery/

- stop neo4j 
`sudo systemctl stop neo4j`
- enable line in /etc/neo4j/neo4j.conf
`dbms.security.auth_enabled=false`
- start neo4j
`sudo systemctl start neo4j`
- recovery lost password
```
cypher-shell -d system
@system> ALTER USER neo4j SET PASSWORD 'mypassword';
@system>:exit;
```
At this point, your init password has been reset to 'mypassword', you need to stop neo4j; comment out `dbms.security.auth_enabled=false`; start neo4j.

Access to neo4j server again, will ask you change password, carefully reset new password longer than 8 chrarcters.
```
cypher-shell -a 'neo4j://localhost:7687'
```

## Install neo4j python driver


```python
!pip install neo4j
```

## Connect to db
Put `NEO4J_PASSWORD=xxx` in .env under current folder, 


```python
from dotenv import load_dotenv
import os

load_dotenv()

neo4j_user = "neo4j"
neo4j_password = os.environ["NEO4J_PASSWORD"]
```


```python
from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = (neo4j_user, neo4j_password)

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()
```

## Write to db


```python
summary = driver.execute_query(
    "CREATE (:Person {name: $name})",
    name="Janet",
    database_="neo4j",
).summary
print("Created {nodes_created} nodes in {time} ms.".format(
    nodes_created=summary.counters.nodes_created,
    time=summary.result_available_after
))
```

    Created 1 nodes in 4 ms.


## Read from db


```python
records, summary, keys = driver.execute_query(
    "MATCH (p:Person) RETURN p.name AS name",
    database_="neo4j",
)

for record in records:
    print(record.data())  

print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
))
```

    {'name': 'Robert'}
    {'name': 'Janet'}
    The query `MATCH (p:Person) RETURN p.name AS name` returned 2 records in 1 ms.


## Update db


```python
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    SET p.age = $age
    """, name="Janet", age=18,
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")
```

    Query counters: {'_contains_updates': True, 'properties_set': 1}.


## Create relationship


```python
records, summary, keys = driver.execute_query("""
    MATCH (janet:Person {name: $name})
    MATCH (robert:Person {name: $friend})
    CREATE (janet)-[:KNOWS]->(robert)
    """, name="Janet", friend="Robert",
    database_="neo4j",
)
print(f"Query counters: {summary.counters}.")
```

    Query counters: {'_contains_updates': True, 'relationships_created': 1}.


## Query db


```python
records, summary, keys = driver.execute_query(
    "MATCH (p:Person {age: $age}) RETURN p.name AS name",
    age=18,
    database_="neo4j",
)

for person in records:
    print(person)

print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after,
))
```

    <Record name='Janet'>
    The query `MATCH (p:Person {age: $age}) RETURN p.name AS name` returned 1 records in 2 ms.


## Delete all nodes


```python
summary = driver.execute_query(
    "MATCH (n) DETACH DELETE n",
    database_="neo4j",
).summary

print("Deleted {nodes_deleted} nodes in {time} ms.".format(
    nodes_deleted=summary.counters.nodes_deleted,
    time=summary.result_available_after
))
```

    Deleted 2 nodes in 4 ms.


## Close db connection and session


```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="neo4j")

session.close()
driver.close()
```

## Further reading
- https://www.techrepublic.com/article/how-to-install-neo4j-ubuntu-server/ 
- https://neo4j.com/docs/python-manual/current/ 


```python

```
