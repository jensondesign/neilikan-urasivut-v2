import os

from sqlalchemy import create_engine, text

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string,
  connect_args = {
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })                    

with engine.connect() as conn:
  result = conn.execute(text("SELECT * FROM jobs"))

result_dicts = []
for row in result.all():
    result_dicts.append(dict(zip(result.keys(), row)))

print(result_dicts)