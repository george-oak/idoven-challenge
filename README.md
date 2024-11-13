# Idoven Backend Challenge

This API is my submit to the Idoven Backend Challenge. It's made using FastAPI and MySQL on Docker Containers.
There's no code tests at this first moment due to lack of time... But I will try to add them later if I can.

## Usage

You can build up the Docker containers that work with the API using this command:

```bash
docker-compose up
```

## Access

- You can use Swagger to test the services *http://localhost:8000/docs/* 

## Authentication

Oauth2 is integrated in this API.
To interact with the endpoints, a user Bearer token is required.
After a user logs in, the token is generated and should be included in the request header as follows:

**Authorization: Bearer {*generated_token*}**

## Features

Users can send ECG data to the API.
Users can read ECG data they have created before.
Users can access to the signal of the leads they submitted and check those that cross 0.
Admin users can register new users.

## User Permission

Users can only read the data they have created.
Admin users can only to register new users but cannot create or read any ECG data.
Users can also be registered using **/user/register** endpoint by and admin user
An user with admin priviliges is pregenerated in the database.
You can login with the credentials above:
**username: email@sample.com, password: 123_Answer_again**