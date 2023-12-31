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

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs"))

  jobs = []
  for row in result.all():
      jobs.append(dict(zip(result.keys(), row)))
  return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
      query = text("SELECT * FROM jobs WHERE id = :val")
      print(f"Executing SQL query: {query}")
      result = conn.execute(query, {'val': id})
      row = result.fetchone()

      if row is None:
          return None
      else:
          # Convert RMKeyView to a list and then use indexing
          column_names = list(result.keys())
          row_dict = {column_names[i]: row[i] for i in range(len(row))}
          return row_dict

def add_application_to_db(job_id, data, cv_file):
  with engine.connect() as conn:
      query = text("INSERT INTO tyohakemukset (job_id, firstName, lastName, email, sijainti, linkedin, cv, hakukirje) VALUES (:job_id, :firstName, :lastName, :email, :sijainti, :linkedin, :cv, :hakukirje)")

      cv_data = cv_file.read() if cv_file else None

      params = {
          'job_id': job_id,
          'firstName': data['firstName'],
          'lastName': data['lastName'],
          'email': data['email'],
          'sijainti': data['sijainti'],
          'linkedin': data['linkedin'],
          'cv': cv_file.filename if cv_file else None,
          'hakukirje': data['hakukirje']
      }

      conn.execute(query, params)
      print(f"Tiedoston nimi tallennettu: {cv_file.filename}")
  
def add_contact_to_db(data):
  with engine.connect() as conn:
    query = text("INSERT INTO yhteydenotot (etunimi, sukunimi, sposti, aihe, viesti) VALUES (:etunimi, :sukunimi, :sposti, :aihe, :viesti)")

    params = {
      'etunimi': data['etunimi'],
      'sukunimi': data['sukunimi'],
      'sposti': data['sposti'],
      'aihe': data['aihe'],
      'viesti': data['viesti'],
    }

    conn.execute(query, params)