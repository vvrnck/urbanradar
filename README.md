# Urban Radar

Urban Radar is a geospatial open-source product that allows users to input and see location-based information. It is developed using Python and Vue.JS, and includes three modules: `core-api`, `user-interface`, and `utils`. 

## Installation

To run Urban Radar, you will need to have Docker installed. Once Docker is installed, you can run the following command:

```
docker compose up --build
```

This will start the application and all its modules. 

It's also possible to run Urban Radar on any docker friendly cloud product like Cloud Run, App Engine Flex, Kubernetes or EKS.

## Modules

### `database`

The `database` module is a PostgreSQL 14 database to store your data. Use this module to init your database if necessary.

### `core-api`

The `core-api` module includes the backend APIs for Urban Radar. This module is responsible for handling all API responses. It is built using Python 3.10 and uses a PostgreSQL database to store and retrieve data. 

### `user-interface`

The `user-interface` module includes the frontend interface for Urban Radar. This module is responsible for providing users with an intuitive and user-friendly interface for accessing location-based information. It is built using React and communicates with the `core-api` module to retrieve and display data. 

### `utils`

The `utils` module includes various ETL scripts and other utilities that are used by the `core-api` and `user-interface` modules. 

### `geojson-grid`

The `geojson-grid` should be used to create the delimiter hexagons grid that the application will use.

## Usage

Once the application is running, you can access the Urban Radar user interface by visiting `http://localhost:3000` in your web browser. 

### Generating the first user


## Contributions

We welcome contributions to Urban Radar! If you would like to contribute, please fork the repository and submit a pull request. 

## License

Urban Radar is licensed under the [MIT License](https://opensource.org/licenses/MIT).
