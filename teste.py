token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MDIzNzk3NDE0IiwiZXhwIjoyMDYyMTk4OTk2fQ.KNPNg6ye8DnYTyHZpq8xkY_ixPAZWs42pHse6voBbQ4"
import os
from dotenv import load_dotenv
load_dotenv()

if token == os.getenv("HE"):
    print("ok")