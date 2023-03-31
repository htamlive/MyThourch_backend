# MyThorch-server
![flow-chart](flow-chart.png)

## Installation

To install and run the app locally, you'll need to follow these steps:

1. Clone this GitHub repository to your local machine.
2. Ensure that you have Docker installed on your machine.
3. Open the terminal and navigate to the project directory.
4. Create a `.env` file in the project root directory with the following contents:
    ```
    OPENAI_API_KEY=[YOUR_OPENAI_API_KEY]
    REDIS_HOST=[YOUR_REDIS_HOST]
    REDIS_PORT=[YOUR_REDIS_PORT]
    ```
    Replace `[YOUR_OPENAI_API_KEY]` with your actual OpenAI API key, `[YOUR_REDIS_HOST]` with your Redis host address, and `[YOUR_REDIS_PORT]` with your Redis port number.
5. Run Redis container by running the following command:
    ```
    docker run --name your-redis-container -d redis
    ```
    This will start the Redis container.

6. Build the Docker image by running the following command:
    ```
    docker build -t your-app-name .
    ```
7. Run the Docker container by running the following command:
    ```
    docker run -p 5000:5000 --env-file .env --link your-redis-container:redis your-app-name
    ```

    This will start the Flask app on port 5000 and link it to the Redis container.

8. Open a web browser and navigate to `http://localhost:5000` to see the app running.

## License

MIT license
