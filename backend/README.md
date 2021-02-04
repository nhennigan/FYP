Commands to get up and running 
```
docker-compose build --no-cache
docker-compose up 
```
add -d if you want to run in the background

```
docker-compose down -v
```
If you want to bring down all the containers completely. Good for reseting the database / updating the schema

To get into the database container 
```
docker exec -it container_name mysql -uroot -p
```
