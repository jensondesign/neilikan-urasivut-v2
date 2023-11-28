from flask import Flask, render_template

app = Flask(__name__)

JOBS = [
  {
    'id': 1,
    'title': 'Puutarhuri',
    'sijainti': 'Helsinki',
    'tuntipalkka': '16€'
  },
  {
    'id': 2,
    'title': 'Vuorovastaava',
    'sijainti': 'Helsinki',
    'tuntipalkka': '24€'
  },
  {
    'id': 3,
    'title': 'Myyjä',
    'sijainti': 'Helsinki',
    'tuntipalkka': '14€'
  }
]

@app.route("/")
def hello():
    return render_template('home.html', jobs=JOBS)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)