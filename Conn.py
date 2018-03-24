'''
Autor: Sebastian ignacio lopez munoz
Empresa: Novaxis
Version: 1.0.0
Lenguage: python2
'''
import socket
from threading import Thread
from time import sleep
import os
import sys

MAX_LEN = 2048 # Maximo de bytes permitidos

'''
@Conn:
    Clase conexion para recibir datos a traves de internet utilizando
    Sockets, por defecto la direccion es el dominio local o localhost y
    la ip en la estandar para proxy 8080, modificables en cada instancia
'''
class Conn:
    '''
    Constructor de la clase Conn, recibe como parametros la direccion ip
    y el puerto local que se usara al escuchar conexiones externas.
    '''
    def __init__(self,address="127.0.0.1",port=8080):
        self.connections = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_address = (address,port)
        print >>sys.stderr, 'Escuchando desde la ip %s en el puerto %s' % self.server_address
        print >>sys.stderr, 'Esperando conexiones..'
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        self.listener_running = False
        self.receiver_running = False
        # Threading
        self.thread_listener = Thread(target = self.listener)
        self.thread_listener.setDaemon(True)
        self.thread_listener.start()

        self.thread_clients = []
        print "[+] Proceso creado con exito."
    '''
    Funcion que acepta las conexiones externas entrantes.
    '''
    def listener(self):
        if not self.listener_running:
            self.listener_running = True
            while 1:
                connection, client_address = self.sock.accept()
                print "Cliente connectado! %s:%s\n" % client_address
                self.connections.append(connection)
                thread_client = Thread(target = self.receiver,args=[connection])
                thread_client.start()
                self.thread_clients.append(thread_client)
        else:
            return False
    '''
    Funcion que recive la data de las conexiones aceptadas.
    '''
    def receiver(self,connection):
        self.receiver_running = True
        ip = connection.getsockname()[0]
        port = connection.getsockname()[1]
        try:
            data = connection.recv(MAX_LEN)
            print >>sys.stderr, '%s:%s dice: %s' % (ip,port,data)
        finally:
            print >>sys.stderr, '[!] Cerrando conexion en direccion %s:%s\n' % (ip,port)
            connection.close()
    '''
    Funcion de refresco para limpiar conexiones cerradas.
    '''
    def refresh(self):
        i = 0
        if len(self.thread_clients) > 0:
            for t in self.thread_clients:
                if not t.isAlive():
                    del self.thread_clients[i]
                i += 1
'''
Metodo main
'''
def __main__():
    seconds = 2
    try:
        a = Conn()
        while 1:
            sleep(seconds)
            a.refresh()
    except Exception,e:
        print e
        print "\nBye bye!"
__main__()
