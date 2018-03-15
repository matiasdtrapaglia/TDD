import Pyro4 , time, random

#ip maq virtual 192.168.84.128
#uri = raw_input("What is the Pyro uri of the greeting object? ").strip()

par_serv = Pyro4.Proxy("PYRONAME:servidor.de.variables")         # get a Pyro proxy to the greeting object
if (par_serv.exit_get == True):
    par_serv.exit_set(False)
    time.sleep(1)
depth = par_serv.depth_get

print "\n - Generador de estimulos remoto - \n"

def test_rnd(num):
    print "\n - Iniciando test de aleatoreidad -\n"
    cont = 0
    for i in range(num):
        A = random.randint(0, (2**depth)-1)
        B = random.randint(0, (2**depth)-1)
        par_serv.sumandos_set(A, B)
        time.sleep(0.3)
        if (A+B) == par_serv.X_get:
            print "%s + %s = %s   OK" % (str(A), str(B), str(A+B))
            cont +=1
    print "\n %s de %s test cases Correctos.\n" % (str(cont), str(num))
        
while par_serv.exit_get == False :
    A = raw_input("Valor A = ").strip()
    if (A.lower() == 'test'):
        cant = raw_input("\nCantidad de operaciones a probar: ").strip()
        if cant.isdigit(): test_rnd(int(cant))
        continue
    if (A.lower() == 'salir'):
        par_serv.exit_set(True)
        break
    
    B = raw_input("Valor B = ").strip()
    if (A.isdigit() and B.isdigit()):
        par_serv.sumandos_set(int(A), int(B))
        print "A = %s     B = %s\n" % (A, B)
    
    else: print "[0] Datos descartados"
    time.sleep(0.2)
    
