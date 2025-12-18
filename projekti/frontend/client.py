import requests

def send_analysis(cv, job):
    try:
        r = requests.post('http://127.0.0.1:5000/analyze', json={'cv':cv,'job':job})
        return r.json() if r.status_code==200 else {'error':'Virhe'}
    except:
        return {'error':'Yhteys epäonnistui'}