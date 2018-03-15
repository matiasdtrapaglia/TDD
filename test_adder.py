# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from adder_model import adder_model
import random
import Pyro4
import time


@cocotb.test()
def adder_basic_test(dut):
    """Test for 5 + 10"""
    #uri = raw_input("What is the Pyro uri of the greeting object? ").strip()

    par_serv = Pyro4.Proxy("PYRONAME:servidor.de.variables")         # get a Pyro proxy to the greeting object

    if (par_serv.exit_get == True):
        par_serv.exit_set(False)
        time.sleep(1)
    
    #dut.DATA_WIDTH <= par_serv.depth_get  #  :'(
    
    yield Timer(2)
    A = 2
    B = 3
    A_old = A
    B_old = B
    #bucle=True
    cocotb.log.info("\n\n - Simulation Loop Started - \n")
    while par_serv.exit_get == False:
        A, B = par_serv.sumandos_get
        if (A != A_old) or (B != B_old):
            A_old = A
            B_old = B
            dut.A = A
            dut.B = B
            yield Timer(20)
            par_serv.X_set(int(dut.X))
            if int(dut.X) != (A + B):
                raise TestFailure(
                    "[-] Adder result is incorrect: %s != %s" % (str(dut.X), adder_model(A, B)))
            else:  # these last two lines are not strictly necessary
                dut._log.info("[+] Ok!, %s + %s = %s !" % (int(dut.A), int(dut.B), int(dut.X)))            
        time.sleep(0.1)
        

        #if par_serv.exit_valor() == True: 
            #bucle = False
        

    if int(dut.X) != adder_model(A, B):
        raise TestFailure(
            "Adder result is incorrect: %s != %s" % (str(dut.X), adder_model(A, B)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("Ok!, %s + %s = %s !" % (int(dut.A), int(dut.B), int(dut.X)))


@cocotb.test(skip = True)
def adder_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""
    yield Timer(2)

    for i in range(10):
        A = random.randint(0, 15)
        B = random.randint(0, 15)

        dut.A = A
        dut.B = B

        yield Timer(2)

        if int(dut.X) != adder_model(A, B):
            raise TestFailure(
                "Randomised test failed with: %s + %s = %s" %
                (int(dut.A), int(dut.B), int(dut.X)))
        else:  # these last two lines are not strictly necessary
            dut._log.info("Random Ok!, %s + %s = %s !" % (int(dut.A), int(dut.B), int(dut.X)))
