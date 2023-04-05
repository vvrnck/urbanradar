# Urban Radar

Urban Radar is a geospatial product that allows users to access location-based information. It is developed using Python and React, and includes three modules: `core-api`, `user-interface`, and `utils`. 

## Installation

To run Urban Radar, you will need to have Docker installed. Once Docker is installed, you can run the following command:

```
docker-compose up
```

This will start the application and all its modules. 

## Modules

### `core-api`

The `core-api` module includes the backend settings for Urban Radar. This module is responsible for handling all API requests and responses. It is built using Python and uses a PostgreSQL database to store and retrieve data. 

### `user-interface`

The `user-interface` module includes the frontend settings for Urban Radar. This module is responsible for providing users with an intuitive and user-friendly interface for accessing location-based information. It is built using React and communicates with the `core-api` module to retrieve and display data. 

### `utils`

The `utils` module includes various ETL files and other utilities that are used by the `core-api` and `user-interface` modules. 

## Usage

Once the application is running, you can access the Urban Radar user interface by visiting `http://localhost:3000` in your web browser. 

## Contributions

We welcome contributions to Urban Radar! If you would like to contribute, please fork the repository and submit a pull request. 

## License

Urban Radar is licensed under the [MIT License](https://opensource.org/licenses/MIT).
