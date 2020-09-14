# The Bloomon Challenge

### How to run this application
In order to be able to start the application, please follow the following instructions.
 
##### Pre-requisites:
 * Make sure you have docker running on your machine before proceeding. Or else  [Install Docker!](https://docs.docker.com/engine/install/)
 
###### Instructions:
_Run the following commands from root folder_

```
docker build --tag bloomon-challange-0.1 .
docker run --interactive --name app bloomon-challange-0.1
```