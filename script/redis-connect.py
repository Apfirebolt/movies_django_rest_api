import redis

# Initialize the Redis client with your VPS IP, port, DB, and password
client = redis.Redis(
    host="206.81.2X.2XX",
    port=6379,
    db=1,
    password="my_redis_password"
)

try:
    # 1. Insert (set) some keys
    client.set("blog:title", "My Art Learning Journey")
    client.set("blog:views", 34)
    print("Keys inserted successfully!")

    # 2. Retrieve (get) the keys later
    title = client.get("blog:title")
    views = client.get("blog:views")

    # 3. Print the retrieved values (decoding bytes to strings)
    print(f"Retrieved Blog Title: {title.decode('utf-8')}")
    print(f"Retrieved Blog Views: {views.decode('utf-8')}")

except Exception as e:
    print(f"An error occurred: {e}")