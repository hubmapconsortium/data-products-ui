from pathlib import Path

print("Loading production settings")

DEBUG = False

SECRET_PATH = Path("/opt/secret")
# Static secret key is required
with open(SECRET_PATH / "django_secret_key.txt") as f:
    SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = [
    "data-products.cmu.hubmapconsortium.org",
]
