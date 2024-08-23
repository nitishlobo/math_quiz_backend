# Math Quiz Backend

## About

This repo contains the backend API and database setup for a math quiz app.

## Installation

### Project environment

1. Duplicate `.env.example` and rename the duplicate to `.env`.
2. Change variables as desired. Fill in the following variables:  
  `DATABASE_PASSWORD`

### Database setup

Instructions are for windows machines but they will be similar for linux and macOS

1. Download postgresql v16.1:  
  <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>

2. On the install postgresql wizard, install the instance on any unoccupied port.  
  Ensure you change the port settings to be the same in `v1/.env` for `DATABASE_PORT`.

### Python

#### Python version - `3.12`

#### Dependencies

- Production - `requirements/prod.txt`  
  Contains libraries needed to run the app
- Development - `requirements/dev.txt`  
  Contains libraries needed to develop the app as well as the production libraries
- Testing - `requirements/test.txt`  
  Contains libraries needed to test the app  as well as the production libraries
- All - `requirements/all.txt`  
  Contains all of the above
