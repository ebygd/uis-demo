# UiS DevOps Lecture Flask demo application

## Building

Build this image with
```
docker build -t uis-demo:1.0.0 .
```
If local network is running IPv6, it might be necessary to build using the `host` network, instead of the default `docker` one (this is a bug with some versions of Docker):
```
docker build --network host -t uis-demo:1.0.0 .
```

## Running
This application can be run with

```
docker run --rm -it uis-demo:1.0.0
```

To change the port from the default 5000, the flag "--port 80" can be added to the CMD instruction in the Dockerfile.


