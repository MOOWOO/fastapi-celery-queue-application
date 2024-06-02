import redis
import os

def test_redis_connection():
    redis_host = "REDIS_URL"
    redis_port = "REDIS_PORT"
    redis_password = os.environ.get("REDIS_PASSWORD", "REDIS_PASSWORD")

    try:
        client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=False,
        )

        pong = client.ping()
        if pong:
            print("Connected to Redis server successfully!")

    except Exception as e:
        print(f"Failed to connect to Redis server: {e}")

if __name__ == "__main__":
    test_redis_connection()
