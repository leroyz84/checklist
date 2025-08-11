# Checklist
Simple Python Flask application to generate a checklist template to easy check off.

My use-case is that i often go sporting and finding out i forgot my water bottle, or my headphones.

I had the need for an too easy app that i can mark as it's in my duffel bag.

## install
Just run the container and put it behind some kind of revere proxy.

## updates
Probably none

## Security
run local, or put it behind some auth mechanism.

## Build & run docker
```bash
docker build -t checklist .
docker run -d -p 8080:8080 checklist
```
or just compose
```bash
docker-compose up
```
