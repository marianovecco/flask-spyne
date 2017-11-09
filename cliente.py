from suds.client import Client as SudsClient

url = 'http://127.0.0.1:5000/soap/someservice?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.obtenerMateriaAlumno(1234)
print r
