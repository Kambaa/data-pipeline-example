# Example data pipeline using python, Postgres and Debezium and Kafka.
___

Whole thing is prepared to be run on docker, just run `docker compose up` (add `-d` to make it work on background).

Todo List:
- [x] Add a docker compose file
- [x] Add Postgres 15 in docker compose as `db` service
- [x] Data Generation
  - [x] Add a basic, fixed data generation in an `app.py` file
  - [x] Generate a `Dockerfile` of `app.py`
  - [x] Add configuration support from env variables
  - [x] Add connection pooling and connection retry mechanisms
  - [x] Generate data using `Faker` library
  - [x] Add bulk insertion of 500 rows
  - [ ] Add Retry support on insertions
  - [ ] Add scheduling, i.e 5000 rows insert per minute
  - [ ] Add dirty, wrong, misplaced and empty data with configurable occurence change on data generation
- [ ] Add, configure, and prepare Kafka
- [ ] Setting up Debezium CDC
  - [ ] Update Postgres configuration for Debezium usage (enable wal)
  - [ ] Configure Debezium to listen db changes and send kafka events
- [ ] Add or configure simple kafka topic listener and see that Debezium is sending datas successfully and correctly to related Kafka topic
- [ ] Stress the system, see the limits of bulk data insertion, Debezium change reading capability and kafka topic durability
- [ ] Consuming Data from Kafka Topic
- [ ] Data cleaning / cleansing
  - [ ] Prepare strategies for the dirty data
  - [ ] Write data cleaning and cleansing
  - [ ] Put the clean / cleansed data to somewhere, i.e. another db table.
