#classe wrapper
#funzioni di connetti e di disconnetti + varie per operazioni CRUD
#le variabili di istanza sono le 4 variabili per la connetti
#invece la connetti è una variabile di classe 

#importo il modulo 
import pymssql
from pymssql import output
from pymssql import _mssql

class WrapperDB:
    
    conn = 0
    
    #def __init__(self, server="PCPAOLO\SQLEXPRESS", user="sa", password="Password1!", database="5DINF", port="1433"):
    #def __init__(self, server="192.168.40.16\\SQLEXPRESS", user="CRD2122",
    def __init__(self, server="5.172.64.20\\SQLEXPRESS", user="CRD2122",
               password="xxx123##", database="CRD2122"):
        self._server=server
        self._user=user
        self._password=password
        self._database=database
        
        
    def connetti(self):
        #connessione
        try:
            WrapperDB.conn = pymssql.connect(server = self._server, user = self._user, \
                        password = self._password, database = self._database)
            #print(f"\nConnessione effettuata! (DB: {self._database})\n")
            return WrapperDB.conn	
        except _mssql.MssqlDriverException:
            print("A MSSQLDriverException has been caught.")
        except _mssql.MssqlDatabaseException as e:
            print("A MSSQLDatabaseException has been caught.")
            print('Number = ',e.number)
            print('Severity = ',e.severity)
            print('State = ',e.state)
            print('Message = ',e.message)  
        except Exception as err: 
            print("********** ERRORE [connetti] **********")
            print(str(err))     
            print("***************************************")     
        return 


    def disconnetti(self, co):
        #disconnessione	
        try:
            co.close()
        #    print(f"\nCHIUSURA connessione! (DB: {self._database})\n") 
        #except:
        #    print(f"\nCHIUSURA connessione NON riuscita! (DB: {self._database})\n")
        #    return 0
        except Exception as err: 
            print("********** ERRORE [disconnetti] **********")
            print(str(err))     
            print("******************************************")     
        

    def elencoDischi(self, as_dict = False):
        #restituisce una lista di tuple se as_dict = False
        #altrimenti restituisce una lista di coppie chiave/valore (dictionary)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            #sql = "SELECT Id, Artist, Title, [Year], Company FROM PC_Records"
            sql = "SELECT Id as id, Artist as artist, Title as title, [Year] as year, Company as company FROM PC_Records"
            cur.execute(sql)
            lista = cur.fetchall()
        except Exception as err: 
            print("********** ERRORE [elencoDischi] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista

    
    def singoloDisco(self, id):
        #restituisce un singolo post
        ret = {}
        conn = self.connetti()
        try:
            cursore = conn.cursor(as_dict = True)
            
            #sql = f"""
            #    SELECT Id, Artist, Title, [Year], Company 
            #    FROM PC_Records 
            #    WHERE id = {id}   
            #    """
            #cursore.execute(sql)

            sql = """
                SELECT Id, Artist, Title, [Year], Company 
                FROM PC_Records 
                WHERE id = %d   
                """
            cursore.execute(sql, (id, ))
            ret = cursore.fetchone()
        except Exception as err: 
            print("********** ERRORE [singoloDisco] **********")
            print(str(err))     
            print("*******************************************")  
        self.disconnetti(conn)
        return ret    

    
    def inserisciDisco(self, parametri):
        #inserisce un nuovo post; restituisce un booleano con l'esito dell'operazione
        #parametri: tupla con i valori dei parametri -> (artist, title, year, company)
        conn = self.connetti() 
        ret = True
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO PC_Records (Artist, Title, Year, Company) VALUES (%s , %s, %d, %s)"
            cursore.execute(sql, parametri)
            conn.commit()
            #print("INSERIMENTO DISCO AVVENUTO")
        except Exception as err: 
            print("********** ERRORE [inserisciDisco] **********")
            print(str(err))     
            print("*********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret


    def inserisciDiscoSP(self, parametri):
        #inserisce un nuovo post chiamando la stored procedure PC_InserisciDisco restituendo il valore
        #di ritorno (che corrisponde l'id del disco inserito); se si verifica un errore restituisce -1
        #parametri: tupla con i valori dei parametri -> (artist, title, year, company)
        conn = self.connetti() 
        ret = -1
        try:
            #dichiaro id come valore di output per la SP
            id = output(int)
            #aggiungo id ai parametri
            parametri = parametri + (id,)
            cursore = conn.cursor()
            res = cursore.callproc('dbo.PC_InserisciDisco', parametri)
            conn.commit()
            #print("INSERIMENTO DISCO AVVENUTO")
            #return True            
            ret = res[4]
        except _mssql.MssqlDatabaseException as e:
            print("********** ERRORE [inserisciDiscoSP] **********")
            print("A MSSQLDatabaseException has been caught.")
            print('Number = ',e.number)
            print('Severity = ',e.severity)
            print('State = ',e.state)
            print('Message = ',e.message)
            ret = -1
        except Exception as err:
            #print("\INSERIMENTO DISCO/i: Si sono verificati degli errori!")
            print("********** ERRORE [inserisciDiscoSP] **********")
            print(str(err))     
            print("***********************************************")  
            ret = -1
        self.disconnetti(conn)
        return ret


    def aggiornaDisco(self, id, parametri):
        #modifica un disco esistente; restituisce un booleano con l'esito dell'operazione
        #id: id del disco
        #parametri: tupla con i valori dei parametri -> (artist, title, year, company)
        ret = True
        conn = self.connetti() 
        try:
            #aggiungo id ai parametri
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE PC_Records SET Artist = %s, Title = %s, Year = %d, Company = %s WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()
            #print("AGGIORNAMENTO DISCO AVVENUTO")
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            #print("\AGGIORNAMENTO DISCO/i: Si sono verificati degli errori!")
            print("********** ERRORE [aggiornaDisco] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret


    def eliminaDisco(self, id):
        #elimina un post; restituisce un booleano con l'esito dell'operazione
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE PC_Records WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()
            #print("ELIMINA DISCO AVVENUTO")              
        except Exception as err:
            #print("\ELIMINA DISCO/i: Si sono verificati degli errori!")
            print("********** ERRORE [eliminaDisco] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return ret

    


	    