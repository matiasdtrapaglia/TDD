# saved as greeting-server.py
import Pyro4
import time

@Pyro4.behavior(instance_mode="single")
@Pyro4.expose
class p_servidor(object):
    def __init__(self):
        self.A = 2
        self.B = 3
        self.exit = False
        self.nombre_test = ""
        self.X = 0
        self.bit_depth = 4
    
    @property
    def exit_get(self):
        return self.exit
    
    @property
    def X_get(self):
        return self.X
    
    def X_set(self, val):
        self.X = val
    
    @property
    def depth_get(self):
        return self.bit_depth
    
    def depth_set(self, val):
        self.bit_depth = val
    
    def nombre_set(self, nombre):
        self.nombre_test = nombre
    
    def exit_set(self, val):
        self.exit = val
    
    #def fin(self):
        #self.exit = True
    
    @property
    def sumandos_get(self):
        return self.A, self.B
    
    def sumandos_set(self, valA, valB):
        self.A, self.B = valA, valB
    

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(p_servidor)   # register the greeting maker as a Pyro object
ns.register("servidor.de.variables", uri)

print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
