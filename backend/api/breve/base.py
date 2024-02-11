import hashlib
import base64
from pymongo import MongoClient


class BreveURL:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["urls"]

    def breve_url(self, url: str):
        # Hash the URL using SHA-256
        hashed_url = hashlib.sha256(url.encode()).digest()

        # Encode the hash into base64
        encoded_url = base64.urlsafe_b64encode(hashed_url).decode()[:8]

        # Check for duplicates
        if self.collection.find_one({"breve_url": encoded_url}):
            # If duplicate, we return stored value
            return encoded_url

        # If the encoded URL doesn't exist, insert it into the database
        self.collection.insert_one({"breve_url": encoded_url, "original_url": url})

        return encoded_url

    def decode_url(self, breve_url):
        # Retrieve the original URL from the database using the encoded URL
        url_data = self.collection.find_one({"breve_url": breve_url})

        if url_data:
            return url_data["original_url"]
        else:
            return "URL not found."
