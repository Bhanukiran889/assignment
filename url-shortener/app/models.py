from datetime import datetime

# In-memory dictionary to store short codes and their metadata
url_store = {}  # key: short_code, value: {url, created_at, clicks}
