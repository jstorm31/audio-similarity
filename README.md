# Audio similarity

This project is a semestral work for course NI-VMM on FIT CTU. It is a Shazam-like app that returns a set of similar audio tracks for an audio query.

## Setup

The project consists of a server, dataase and client. Everything runs in Docker containers, so **Docker needs to be installed**.

1. Add `.env` file with all required environment variables into root of the project. Sample is in `.env.example`
2. Run `make build`
3. Run `make run`

This will start the client web app on address `localhost:3000` and the server on `localhost:5000`.

