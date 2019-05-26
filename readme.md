### MiniURL

----

URL Shortening Application Using Docker Compose.

Demos integration of `node/express`, `flask`, `postgres` and `redis` 

### Running:
```
docker-compose up --build -d --remove-orphans   # Run the container
docker-compose down -v --remove-orphans  # Stop and shutdown
``` 

The site will be available to you at `localhost:43434`


### TODO:
 - Add Logging to standard out from the app
 - Add Test Cases for the app
 - Configure Master/Slave Database for postgres and process all reads on the slave 
 - Need to attach database to volume
 - Add frontend JS Service
 - Add URL Validation 
 
#### Access psql in postgres
`docker-compose run db psql -h db -U postgres -d postgres`


#### Good References 
 - https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
