# breve-url

To run the project using docker and docker-compose

```
docker-compose build
```
```
docker-compose up -d
```

To see the logs
```
docker-compose logs -f
```

To run only one service
```
docker-compose up backend
```


## Backend
Python REST API built using FastAPI.
By default, the API runs in http://localhost:9000

To see documentation go to http://localhost:9000/docs or http://0.0.0.0:9000/docs depends on your local network settings


### TODO
- API authentication: because I had no time to add this feature, I added rate limit to the endpoints
- Tests 

## Frontend
React application, it communicates with rest API byt sending a POST request with the url that shorten, and gets shorten url returned.
It shows this urls as a link to be visited.
By default, the webapp runs in http://localhost:3000



### TODO
- Copy to clipboard button
- Tests