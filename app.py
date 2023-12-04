from flask import Flask, render_template, jsonify, request, redirect, url_for, abort, Response

from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_contact_to_db

from sqlalchemy import text

from werkzeug.exceptions import BadRequest



app = Flask(__name__)

@app.route("/")
def hello():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  
  if not job:
    return "Sivua ei löydy", 404
    
  return render_template('jobpage.html', job=job)

@app.route("/job/<id>/hae", methods=['POST'])
def hae_tyopaikka(id):
  data = request.form

  # Käsittelee tiedostot
  cv_file = request.files.get('cv')
  if cv_file:
      # Tallenna tiedosto "uploads"-kansioon
      cv_file.save(f"uploads/{cv_file.filename}")

    
  #Säilytä tietokannassa
  add_application_to_db(id, data, cv_file)
  
  #Lähetä sähköposti

  
  #Näytä kuittaus

  return render_template('tyohakemus-lahetetty.html', tyohakemus=data)

@app.route("/contact", methods=['POST'])
def contact() -> Response:
    if request.method == 'POST':
        data = request.form

        try:
            # Käsittele lomaketiedot tässä

            # Tallenna lomaketiedot tietokantaan
            add_contact_to_db(data)

            # Palauta tyhjä vastaus onnistuneen tallennuksen jälkeen
            return Response(status=204)  # HTTP 204 No Content
        except Exception as e:
            # Jos jotain menee pieleen, palauta virheilmoitus
            return handle_error(e)

def handle_error(error: Exception) -> Response:
    response = jsonify(success=False, message=f"Virhe lomaketietojen käsittelyssä: {str(error)}")
    return response, BadRequest.code  # Korjattu tähän

# Lisää virheen käsittelijä
@app.errorhandler(Exception)
def handle_all_exceptions(error):
    response = jsonify(success=False, message=f"Yleinen virhe: {str(error)}")
    return response, BadRequest.code

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)