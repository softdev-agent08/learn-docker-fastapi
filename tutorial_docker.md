# Docker Basics Command
- `docker pull image_name` - Docker pull from docker hub
- `docker images` - show all docker image
- `docker run image_name` - run docker container
- `docker run -it image_name` - run docker container active 
- `docker stop CONT_NAME or CONT_ID` - to start docker container
- `docker start CONT_NAME or CONT_ID` - to stop docker container
- `docker ps -a` - to check all container exist
- `docker ps` - check active container
- `docker rmi IMAGE_NAME` - to remove any image
- `docker rm CONT_NAME` - to remove any container
- `docker pull image_name:version` - to pull specific version of image
- `docker run -d image_name` - run the container on detached mode 
- `docker run --name CONT_NAME -d IMAGE_NAME` -  to craete a cointainer in specific given name


# Docker Images Layer
    Container(We just can changes) -> Layer2 - > Layer1 -> Base Layer


# Port Binding
   - `docker run -p8080:3360 image_name`
   Here 8080 is a machine port and 3360 is a port that associated with container.
   Then we binding the machine port 8080 with  container port 3306. so that those request hit the port 8080(host) also automatically hit the port 3306(conatiner). 
    `docker run -d -e MYSQL_ROOT_PASSWORD=secret --name mysql-older -p5000:3306 mysql:8.0`

# Troubleshoot Commands
- `docker logs CONT_ID` - to show logs of a specific container (to identify specific problem)
- `docker exec -it CONT_ID /bin/bash` - to execute the specific command on a specific container
- `docker exec -it CONT_ID /bin/sh` - to execute the specific command on a specific container

# Docker Network
    Docker networking is a system that allows Docker containers to communicate with each other, the host machine, and external networks.
- `docker network ls`
- `docker network create network_name`

# Developing with Docker
### setting up mongo and mongo express
--------------------------------------------
#### For Mongo
```docker
docker run -d -p27017:27017 --name mongo --network mongo-network -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=qwerty mongo
```

    -d : run on detuched mode
    -p27017:27017: change docker inside port to host port
    -- name : give the name of the container
    --network: give network name
    -e: select specific value for environment
    mongo: image name
#### For Mongo Express
```docker
docker run -d -p8081:8081 --name mongo-express --network mongo-network -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=qwerty -e ME_CONFIG_MONGODB_URL="mongodb://admin:qwerty@mongo:27017" mongo-express
```

## Docker Compose
<h6> Docker Compose is a tool for defining and running multi-container applications 
</h6>

    1. Create an .yaml file like
```yaml
        version: "3.8"
            services:
            mongo:
                image: mongo:latest
                container_name: mongo_test
                ports:
                - "27017:27017"
                environment:
                    MONGO_INITDB_ROOT_USERNAME: root
                    MONGO_INITDB_ROOT_PASSWORD: example
            mongo-express:
                image: mongo-express:latest
                container_name: mongo_express_test
                ports:
                - "8081:8081"
                environment:
                    ME_CONFIG_MONGODB_ADMINUSERNAME: admin
                    ME_CONFIG_MONGODB_ADMINPASSWORD: qwerty
                    ME_CONFIG_MONGODB_SERVER: mongodb://admin:qwerty@mongo:27017/
                depends_on:
                    - mongo
```


```bash
docker compose -f file_name.yml up -d
docker compose -f file_name.yml down
docker network
```

## Dockerizing our App
    test app -> docekr image -> container

```python
FROM python:3.13
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```
-----------------
### Some Important dockerfile Infrustruction
--------------------------
- FROM
- WORKDIR
- COPY
- RUN
- CMD
- EXPOSE
- ENV
--------------------------------------------

### Dockerfile
```dockerfile
FROM node:18

ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PWD=qwerty

WORKDIR /testapp

COPY package*.json ./
RUN npm install

COPY . .

CMD ["node", "server.js"]
```

```bash
docker build -t testapp:1.0 .  #build docker app
docker images
docker run testapp:1.0
docker run testapp:1.0 bash

```

### Publishing Images
1. First login in docker `docker login`
2. `docker tag testapp:1.0 habiboss08/testapp:1.0`
3. `docker push habiboss08/testapp:1.0`

### Docker Volume
<h6>
  Volumes are <span style="color:red;">persistent</span> data stores for containers.
</h6>


## Question 
    1. VM vs docker?
    2. 


