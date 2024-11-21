# dummy-ta

This is a dummy implementation of the TA API.

## Build the docker image

```bash
docker build -t dummy-ta .
```

## Run the docker container

```bash
docker run -p 5000:5000 dummy-ta
```

Verify that the service is running by visiting
[http://localhost:5000/api/hello](localhost:5000/api/hello) in your browser.

## Stop the docker container

```bash
docker stop $(docker ps -q --filter ancestor=dummy-ta)
```
