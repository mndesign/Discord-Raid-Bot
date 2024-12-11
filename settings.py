import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API=os.getenv("DISCORD_API_TOKEN")
DISCORD_ID=os.getenv("DISCORD_ID")
DEFAULT_GUILD=os.getenv("DEFAULT_GUILD")

SQL_USER=os.getenv("SQL_USER")
SQL_PW=os.getenv("SQL_PW")
SQL_HOST=os.getenv("SQL_HOST")
SQL_DB=os.getenv("SQL_DB")

LANGUAGE='English'  #German, French, Italian, Japanese, Korean, Spanish (only applies to pokemon names)

MESSAGETIMEOUT=3
LONGMESSAGETIMEOUT=10
ERRORTIMEOUT=10
PROFILETIMEOUT=10
RAIDTIMEOUT=600
RAIDSTARTTIMEOUT=300
MULTIPLEOPTIONSTIMEOUT=30