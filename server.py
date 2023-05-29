import cherrypy
#import cherrypy_cors
import json
from WrapperDB import WrapperDB
#from record import record

#@cherrypy.expose
class MyController(object):
    wrp = WrapperDB()

    @cherrypy.expose
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        dischi = self.wrp.elencoDischi(as_dict=True)

        if (int(id) == -1):
            return dischi
        else:
            disco = [d for d in dischi if d["Id"] == int(id)]
            if (len(disco) == 1):
                return (disco[0])
            else:
                cherrypy.response.status = 404
                return {} 


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        disco = cherrypy.request.json
        #res = self.wrp.inserisciDiscoSP((disco["Artist"], disco["Title"], disco["Year"], disco["Company"]))
        res = self.wrp.inserisciDiscoSP((disco["artist"], disco["title"], disco["year"], disco["company"]))
        if (res != -1):
            #return { "Id": res }
            return { "id": res }
        else: 
            cherrypy.response.status = 500
            return {}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    #@cherrypy.tools.accept(media='text/plain')
    def PUT(self, id=-1):
        disco = cherrypy.request.json
        #res = self.wrp.aggiornaDisco(id, (disco["Artist"], disco["Title"], disco["Year"], disco["Company"]))
        res = self.wrp.aggiornaDisco(id, (disco["artist"], disco["title"], disco["year"], disco["company"]))
        if (bool(res)):
            return id
        else:
            cherrypy.response.status = 404
            return { "Id": id } 
            

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        res = self.wrp.eliminaDisco(id)
        if (res == True):
            return {}
        else:
            cherrypy.response.status = 404
            return {}

#if __name__ == '__main__':
conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        #devo aggiungere l'header "Access-Control-Allow-Origin" per abilitare le richieste da un dominio differente
        'tools.response_headers.headers': [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')]
    }
}  

#cherrypy.quickstart(MyController(), '/dischi', conf)
cherrypy.quickstart(MyController())