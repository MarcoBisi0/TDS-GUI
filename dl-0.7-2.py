#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 15:51:11 2011
@author: marco

"""
''' !!!!!!! verificare che le entry per posizioni siano lette come intere !!!!!!!! 
in CYCLE lo faccio - dovrebbe semplificare la vita dopo '''

''' nelle routine di misura, dopo aver generato GRAFstop, generare in GRAFICI GRAFstopped e chiamare dalle routine grafici.stop, dentro alla quale c'è il mv dei file?  '''

VERSION = '0.7-2'

### memo
'''
la misura eventuale in MOTOR_GO_STEPS
in modo continuo parte il thread MISURA, in modo step o scan chiama MEASURE_STEP_MODE
'''
### CHANGELOG
'''
2014-11-12
    definita la variabile globale STEP_SIZE, per ora introdotta solo i MISURA_VELOCE
    per movimenti da ritardi maggiori a minori, riordinato il file, in modo da avere ritardi crescenti
    aggiunta possibilita di movimenti a passo non intero
2014-10-10
    in MisuraVeloce, messo a posto segno ritardo in ps per misure in direzione negativa
    cambiata unita' di misura del ritardo da ps a s
    in modo MisuraVeloce, effettuata la misura ritorna al punto di partenza durante la lettura del lock-in
2014-09-25
    ci voleva un punto fermo
    inserita la possibilità di non usare l'interferometro
    devo riscrivere la parte grafica della gui, in oggetti opportuni
    ripristinata lettura chY in acquisizione FAST
2014-05-21
    in acquisizione FAST, legge solo chX del lockin, per dimezzare tempo di trasferimento dati
2014-05-20
    rimossa seriale interferometro e tutte le chiamate
2014-05-15
    modificato dl_cycle1, tiene conto dello step size
in fast scan mode, 100 fs steps is reasonable -> 6 steps@2.5um
lock-in time costant 30 ms @ 80 MHz fs rep rate
per ricerca, sensitività uno step al di sotto dell'overload senza segnale
2014-04-30
    misura veloce lock-in e interferometro
2014-03-26
    rimossa lettura della temperatura con il termometro di Davide
2014-03-11
    inizio revisione misura in modo continuo -> chiamata a thread misuraContinua
2014-03-07
    rimosso il delay di 100 ms dopo il trigger all'interferometro
2014-02-20
    moved measurement_delay check BEFORE the first measurement of the cycle
    increased to 110 ms the DTR pulse triggering the interferometer, default integration time is 100 ms
2014-01-14
    aggiunta misura di temperatura con strumento DeltaOhm di Davide
    aggiunti parametri alla classe 'seriale' (sn dell'adattatore, parametri di comunicazione)
2013-12-13
    aggiunta misura "sul posto", cioè misure ripetute senza spostare la delay line per verificare rumore 
2013-12-10
    rimossa lettura setup lockin perche' dopo la prima chiamata a READ_CONFIGURATION non riceve piu' una mazza
2013-12-04
    lettura setup lock-in e memorizzazione in file dati
2013-11-19
    aggiunte le keystrokes ^a e ^g per il movimento vai-a-posizione e muovi-dati-passi
2013-11-06
    aggiunto comando VAI A POSIZIONE. sensibilita' dello spostamento pari a 1 full-step
2013-11-05
    eliminato il terminale RS232
    eliminato pop-up modo misura e spostato al posto del terminale seriale
    aggiunto campo per prefisso nome file dati
2013-10-13
    rimosso il checkbox MISURA e codice associato
        l'inizializzazione del lock-in avviene in DL.callMeFisrt se NOT options.noMEASURE
    rimossi radiobutton CW - CCW
    aggiunti bottoni per movimenti +/-1 e +/-10 steps
2013-10-08
    ripristinato controllo su inizializzazione strumento,
        sostituendo INITIALIZE_INSTRUMENT -> INITIALIZE_LI
    nel thread MISURA, cambiato strumento
    aggiunto delay nullo in misura (default)
    in step mode, media su 5 misure
    memorizzazione x,y e visualizzazione real time
2013-09-30
    lettura Lock-in Stanford
    rimosso il controllo sul file INIZIALIZZAZIONE STRUMENTO
2013-09-23
    qualche casino in esecuzione con opzioni
        -s: chiede pwd per socat ma prosegue esecuzione senza leggere
            HACK: dare pwd, stop con ^+C e rieseguire
        -n: commentate tre linee in finally clause di if __main__
    rimossi checkbutton attivazione switch
2013-03-30
    memorizzata su file la posizione della slitta e letta all'avvio
        la variabile e' POSIZIONE, che POTREBBE essere aggiornata ad ogni passo...
    impedito il movimento fino a MAXTRAVEL, fermato prima per evitare casini che ogni tanto si verificano con il micro    
2013-03-29
    aggiunta configurazione strumento dopo richiesta di misurare (initialize_instrument)
    aggiunto popup per mancanza di strumento collegato
2013-03-27
    cambiati i valori di default per velocita' ed accelerazione
2013-03-20  delay-line-0.3-1
    aggiunta opzione da line di comando per evitare la misura
    *** aggiungere messaggio che dica 'impossibile misurare', o qualcosa del genere
2012-05-12
    aggiunto un thread grafico, per ora la misura non è sincronizzata con il passo
    
    forse adesso sì - 2012-05-13    
2012-05-09  ver. delay-line-0.3-tmp-2.py
    RINUNCIO alla sincronizzazione tra step e misure
2012-05-06
    messo a posto il contatore azzerabile
2012-05-04  ver. delay-line-0.2-2.py
    ridimensionata la finestra principale a 800x500
    ridisposti i widget e aggiunti due separatori orizzontali
    aggiunto parsing delle opzioni DEBUG e SIMULA
2012-30-04  ver. delay-line-0.1.py
    aggiunto popup per conferma ricerca SW
    aggiunto visualizzatore posizione azzerabile a piacere, posizioni negative
    per rotazioni CW (verso il motore)
2012-04-29  ver. delay-line_NEW_simulaRS232.py
    aggiunta simulazione porta seriale:
        un thread esegue SOCAT, e viene chiuso all'uscita dal MAIN
        SOCAT richiede i privilegi di amministratore per l'esecuzione -> in VISUDO aggiungere 
            marco   giuditta = NOPASSWD: /usr/bin/socat
        per permettere l'esecuzione all'utente. OCCHIO anche che LOCALHOST non matcha MAI in VISUDO!
            ho dovuto specificare il nome della macchina. Forse in hosts 127.0.0.1 localhost, giuditta ???
2011-11-17
    aggiunta lettura multimetro con libreria USBTMC
#1_2011-02-14 rstrip()->strip(), rimuove anche leading characters
#2_2011-02-14 provato ad eliminare \r nella scrittura su seriale CI VUOLE!!!
2011-01-31
    imposta la direzione del motore in go_step
'''

### TODO:
'''
a volte ci sono dei punti mancanti dal lockin. Che fare???

verificare che la lettura dello interferometro abbia il ritardo con il segno giusto

registrare durata della misura nell'header e riempire la colonna con 0's
!!!
! velocita ed accelerazione durante azzeramento e goto_pos !
lettura lockin su gui
!!!

 aggiungere pulsante e controllo esecuzione in misura-on-point, sul tipo
#!/usr/bin/env python
import os, time
count = 10
while count and not os.path.isfile('stop'):
    print count
    count-=1
    time.sleep(2)
'''
### mettere a posto routine azzeramento!
'''
possibilità misure multiple fermi sullo step, per stimare effetto deformazioni termoelastiche

aggiungere colonna delay in file dati.
    Leggere #step di partenza, sottrarlo ad ogni misura e convertire in ps
    
posso pensare di scalare il grafico ad un range [step-attuale:step-finale] e [0:delay-finale]
    per cercare di avere asse addizionale con il ritardo

in MEASURE_STEP_MODE, in modo SCAN, check su numero di passi da fare PARI

tempo su asse aggiuntivo sul grafico (ed eventualmente nelle mascherine)

FFT at measurement end, possibly in the same window
header per caratterizzazione misura nel file delle misure (o variazione nome file)

verificare se il metodo MOVE è necessario

    vedere come mai non conta in negativo, anche perche' non resetta
    t)  'sy4' al controller (velocità manuale, sy1-sy4)
    u)  far contare i passi in ricerca sw_end (come in movimento normale, con loop sullo stato del motore?)
    v)  rivedere filosofia di azzeramento della posizione
    w)  considerare il FLUSH di pos_memo. Poi c'è il problema della chiusura, devo implementare un metodo QUIT
        dove fare l'operazione, piu' eventualmente altro ancora
    x)  disabilitare i BUTTON sw_X_find_button in SIMUL
    y)  
    z)  

    1)  all'accensione, ricerca di uno dei due limit switch per fare un punto
        andarci alla velocità minima (e applicare l'offset?)

    4) checkbox per DEBUG on/off
'''

'''
rotazione RIGHT porta verso il motore, sw_CW
'''

### imports
import commands
import dl_gui
import get_USB_serial
import glob
import Gnuplot
import gpib_SR830 as LIClass
import gpibprologix as plgx
###import fft-0.0-alpha as fft
#import math
from optparse import OptionParser
import os
### 2013-11-21 import Pmw
#import re
import serial
import string
import subprocess
#import sys
import time
#import Tkinter
from Tkinter import *
import tkMessageBox
import threading
import utilita as ut


SCRIPT_DIR = os.getcwd()
### 2014-03-11 MV_MEAS = 'find /home/marco/Terahertz/ -name "*.???" -print0 | xargs -0 mv -t ' +  SCRIPT_DIR + '/'
MV_MEAS = ('find /home/marco/Terahertz/ -name "*.???" -print0 | ' +
            'if [ $(wc -c) -gt "0" ]; ' +
            'then find /home/marco/Terahertz/ -name "*.???" -print0 | ' +
            'xargs -0 mv -t ' + SCRIPT_DIR + '/; fi') # doesn't call mv if there ius nothing to move!
#subprocess.call(MV_MEAS, shell = True)

#Root = Tkinter.Tk()
Root=Tk()
RTitle = Root.title("Windows")
'''RWidth=Root.winfo_screenwidth()
RHeight=Root.winfo_screenheight()'''
RWidth = 1100
RHeight = 500
Root.geometry(("%dx%d")%(RWidth, RHeight))

dev = '1' # A: RS-232 header, 1: device (the only one in this case...)
RS232_DELAY = False

s = None # provo a riservare la variabile per la seriale

MAXtravel = 120000 # massimo spostamento, da verificare
MAXtravel_guard = 500

STEP_SIZE = 2.4983 # +/- 0.0005

parser = OptionParser()
USAGE = 'usage: %prog [options]'
parser = OptionParser(usage= USAGE)
parser.add_option('--no-interferometer',
                  help = "don't read interferometer measurements",
                  action = 'store_true',
                  dest = 'noInterferometer')
parser.add_option('-d', "--DEBUG",
                  help = "do some logging on stdout",
                  action = 'store_true',
                  dest = 'debug')
parser.add_option('-l', "--LOG",
                  help = "do some logging on file",
                  action = 'store_true',
                  dest = 'log')
parser.add_option('-s', "--SIMUL",
                  help = "simulate the controller",
                  action = 'store_true',
                  dest = 'simula')
parser.add_option('-n', "--noMEASURE",
                  help="don't measure (don't read the multimeter",
                  action = 'store_true',
                  dest = 'noMEASURE')
parser.add_option('-i', '--info',
                  help = 'show imported modules info',
                  action = 'store_true',
                  dest = 'info')
parser.add_option('--fwspeed',
                  help = 'estimate stage forward speed',
                  action = 'store_true',
                  dest = 'fwspeed')
parser.add_option('--bwspeed',
                  help = 'estimate stage backward speed',
                  action = 'store_true',
                  dest = 'bwspeed')

(options, args) = parser.parse_args()
'''if options.speed:
    self.z_estimate_stage_speed()
    exit(0)'''
if options.info:
    import re
    import sys
    moduli = sys.modules
    for i in range(len(moduli.values())):
        match=re.search('marco', str(moduli.values()[i]))
        if match:
            print str(moduli.keys()[i]) + ': ' + str(moduli.values()[i])
    exit(0)
if options.noInterferometer:
    INTERFEROMETER = False
else:
    INTERFEROMETER = True
if options.debug:
    DEBUG = True
else:
    DEBUG = False
if options.log: 
    LOG = True
    fname = time.strftime('%Y-%m-%dT%H%M%S',time.localtime()) + '.LOG'
    flog = open(fname, 'w', buffering = 0) # should write in unbuffered mode -> no need to flush
else:
    LOG = False
if options.simula:
    SIMUL_controller = True
else:
    SIMUL_controller = False
if options.noMEASURE:
    SKIP_measure = True
else:
    SKIP_measure = False

if SIMUL_controller:
    rs232_delay = 0.1
    RS232_DELAY = True

#http://www.java2s.com/Code/Python/GUI-Tk/Gridlayoutmanagerdemonstration.htm
class DL(Frame):
    #def __init__(self, serialechehoapertoprima): #, parent):
    def __init__(self):#, serialechehoapertoprima): #, parent):
        Frame.__init__(self)
        
        self.ser = s #erialechehoapertoprima
        self.master.title('Delay Line Standa ' + VERSION)
        self.master.rowconfigure( 0, weight = 1 )
        self.master.columnconfigure( 0, weight = 1 )
        self.grid()
        #self.widgets_variables()
        dl_gui.widgets_variables(self, SKIP_measure)
        #self.widgets_declare()
        dl_gui.widgets_declare(self)
        
        ### 2013-11-21
        ### 2013-11-21 self.balloon = Pmw.Pmw_1_3.lib.PmwBalloon()
        ### 2013-11-21 self.balloon.Balloon.bind(self.step_get, 'un balloon?')
        
        ### 2013-11-19
        self.step_get.bind('<Control-g>', self.motor_go_steps_a)
        self.go_abs_pos_get.bind('<Control-a>', self.motor_go_steps_a)
        
        self.callMeFirst()
        
        if options.fwspeed or options.bwspeed:
            self.z_estimate_stage_speed()
            exit(0)

    ### 2013-11-19
    def motor_go_steps_a(self, event):
        self.motor_go_steps()   
        
    
        
        
    def callMeFirst(self):
        if DEBUG:
            print 'initializing controller'
        if LOG:
            flog.write('initializing controller\n')
        self.motor_status.set('f') # motor: off
        self.motor_status_set()
        
        self.va_set_default(self.start_v, self.max_v, self.max_a)
        
        self.step_mode.set('1') # full step
        self.set_step_mode()
        
        self.sw_CCW_state.set('1') # sw_CCW on
        self.sw_CCW_set()
        
        self.sw_CW_state.set('1') # sw_CW on
        self.sw_CW_set()
        
        ### 2014-05-16 self.ser.serWrite('su', '0') # sync off
        self.ser.serWrite('su', '1') # sync on
        sync = '%0.4x' % 2 # 1 un trigger ogni 2 passi
        sync = sync.upper()
        self.ser.serWrite('sg', sync)
        
        self.motor_status.set('n') # motor on
        self.motor_status_set()
        
        ### check if we are in a known absolute position
        if not os.path.isfile('pos_absolute_memo'):
            self.pos_absolute_memo = open('pos_absolute_memo', 'w')
            self.pos_absolute_memo.write('0\n')
            self.pos_absolute_memo.flush()
            tkMessageBox.showwarning(message = 'you haven\'t zeroed the position. Do it now')
        else:
            pos_absolute_memo = open('pos_absolute_memo', 'r')
            stringa = []
            while True:
                l = pos_absolute_memo.readline()
                if not l:
                    break
                l = l.strip('\r\n')
                if l != '':
                    stringa.append(l)
            pos_absolute_memo.close()
            pos_absolute_last = float(stringa[-1])
            self.pos_absolute.set(pos_absolute_last)
            self.pos_absolute_memo = open('pos_absolute_memo', 'w')
            self.pos_absolute_memo.write(str(pos_absolute_last) + '\n')
            self.pos_absolute_memo.flush()
        
        ### check if we are in a known relative position
        if not os.path.isfile('pos_relative_memo'):
            self.pos_relative_memo = open('pos_relative_memo', 'w')
            self.pos_relative_memo.write('0\n')
            self.pos_relative_memo.flush()
            ### ??? tkMessageBox.showwarning(message = 'you haven\'t zeroed the position. Do it now')
        else:
            pos_relative_memo = open('pos_relative_memo', 'r')
            stringa = []
            while True:
                l = pos_relative_memo.readline()
                if not l:
                    break
                l = l.strip('\r\n')
                if l != '':
                    stringa.append(l)
            pos_relative_memo.close()
            pos_relative_last = float(stringa[-1])
            self.pos_relative.set(pos_relative_last)
            self.pos_relative_memo = open('pos_relative_memo', 'w')
            self.pos_relative_memo.write(str(pos_relative_last) + '\n')
            self.pos_relative_memo.flush()
            
        if not SKIP_measure:
            self.initialize_LI()
        
    def initialize_LI(self):
        if self.measure_state.get():
            if not os.path.isfile('instrum_initialized'):
                if SIMUL_controller:
                    tkMessageBox.showwarning(message = 'You are running in simulation mode! Data will be generated by the script')
                    fd = open('instrum_initialized', 'w')
                    fd.close()
                else:
                    portaUSB = get_USB_serial.findShortSerial('PXEHE2P5')
                    print 'porta USB:', portaUSB
                    gpib = plgx.prologix(comport = portaUSB)
                    LockinAddr = 8
                    interfacce['lockin'] = LIClass.sr830(gpib, str(LockinAddr)) #self.LI = LIClass.sr830(gpib, str(LockinAddr))
                    self.LI = interfacce['lockin']
                    
                    '''ans = self.LI.idn()
                    if not ans:
                        mess = 'lockin hanged!\n\nswitch it off and than on\nand press ok'
                        result = tkMessageBox.showerror(message = mess)
                        while not result:
                            time.sleep(0.1)'''
                    
                    ### string terminator should be \n, or EOI on GPIB
                    gpib.send(str(LockinAddr), 'OUTX 1\n')
                    self.LI.rst()
                    self.LI.cls()
                    self.LI.setup()
                    time.sleep(1)
                    print "Instrument setup finished"
                    fd = open('instrum_initialized', 'w')
                    fd.close()
            else:
                '''ans = self.LI.idn()
                if not ans:
                    mess = 'lockin hanged!\n\nswitch it off and than on\nand press ok'
                    result = tkMessageBox.showerror(message = mess)
                    while not result:
                        time.sleep(0.1)'''
                
                if DEBUG:
                    print 'instrument already initialized'
                if LOG:
                    flog.write('instrument already initialized\n')

    def dl_cycle_action1(self):
        if int(self.dl_cycle_start_pos.get()) != self.pos_absolute.get():
            self.go_abs_pos.set(self.dl_cycle_start_pos.get())
            self.motor_go_steps() # set DL to cycle starting position
        base_fname = time.strftime('%Y-%m-%dT%H%M%S', time.localtime())
        if self.filename.get() != '':
            base_fname += ('_' + self.filename.get())
        count = self.dl_cycle_rep.get()
        i = 0
        
        hp_points = (int(self.dl_cycle_stop_pos.get()) - int(self.dl_cycle_start_pos.get()))*int(1/self.step_size)
        mess = 'Be sure to set ' + str(hp_points*self.dl_cycle_rep.get()) + ' points in the interferometer software'
        result = tkMessageBox.showinfo(message = mess)
        while not result:
            time.sleep(0.1)
        
        while count: #True:
            if os.path.isfile('dl_cycle_stop'):
                break
            fname = base_fname + ('_' + str(i) + '.dat')
            fd = open('GRAFfname', 'w')
            fd.write(fname)
            fd.close()
            self.steps.set(str(hp_points))
            self.motor_go_steps()
            
            self.go_abs_pos.set(self.dl_cycle_start_pos.get())
            self.motor_go_steps() # set DL to cycle starting position
            count -= 1
            self.dl_cycle_rep.set(count)
            i += 1
        self.motor_stop()
        if os.path.isfile('dl_cycle_stop'):
            os.remove('dl_cycle_stop')
        if os.path.isfile('GRAFfname'):
            os.remove('GRAFfname')

        return

    ### dl_cycle_action(self):
    def dl_cycle_action2(self): #dl_cycle_action(self):
        ''' provare a leggere le ripetizioni, loopare sul letto, decrementare ed aggiornare la visualizzazione? credo fatto
        generazione unico nome file, con suffisso incrementale 
        se necessario, porta la slitta al punto inziale senza misurare '''
        if int(self.dl_cycle_start_pos.get()) != self.pos_absolute.get():
            self.go_abs_pos.set(self.dl_cycle_start_pos.get())
            self.motor_go_steps() # set DL to cycle starting position
        ### 2014-02-15 prepare base file name
        base_fname = time.strftime('%Y-%m-%dT%H%M%S', time.localtime())
        if self.filename.get() != '':
            base_fname += ('_' + self.filename.get())
        count = self.dl_cycle_rep.get()
        i = 0
        
        hp_points = abs(int(self.dl_cycle_stop_pos.get()) - int(self.dl_cycle_start_pos.get()))
        mess = 'Be sure to set ' + str(2*hp_points*self.dl_cycle_rep.get()) + ' points in the interferometer software'
        result = tkMessageBox.showinfo(message = mess)
        while not result:
            time.sleep(0.1)
        
        while count: #True:
            if os.path.isfile('dl_cycle_stop'):
                break
            #if os.path.isfile('GRAFfname'): os.remove('GRAFfname')
            fname = base_fname + ('_' + str(i) + 'a' + '.dat')
            fd = open('GRAFfname', 'w')
            fd.write(fname)
            fd.close()
            self.steps.set(str(hp_points))
            self.motor_go_steps()

            if os.path.isfile('dl_cycle_stop'):
                break
            #if os.path.isfile('GRAFfname'): os.remove('GRAFfname')
            fname = base_fname + ('_' + str(i) + 'b' + '.dat')
            fd = open('GRAFfname', 'w')
            fd.write(fname)
            fd.close()
            self.steps.set(str(-hp_points))
            self.motor_go_steps()
            count -= 1
            self.dl_cycle_rep.set(count)
            i += 1
        self.motor_stop()
        if os.path.isfile('dl_cycle_stop'):
            os.remove('dl_cycle_stop')
        if os.path.isfile('GRAFfname'):
            os.remove('GRAFfname')

        '''while os.path.isfile('GRAFupdate'):
            time.sleep(0.01)
        open('GRAFstop', 'w').close()'''

        #subprocess.call(MV_MEAS, shell = True) # senza shell=True non funziona, bisogna usare os.system() DEPRECATO. warning in manuale per shell=True

        return

    def dl_cycle_stop_action(self):
        open('dl_cycle_stop', 'w').close()
            
    def measure_on_point_action(self):
        self.measurement_mode.set('on_point')
        old = self.steps.get()
        self.steps.set('1')
        self.motor_go_steps() # eventualmente verificare memorizzazione di vai a posizione assoluta, step to go ecc
        self.steps.set(old)
        
    def measure_on_point_stop_action(self):
        open('stop_on_point', 'w').close()
        
    ### misura ON_POINT
    def measure_on_point_mode(self):
        fd = open('GRAFfname', 'r')
        fname = string.strip(fd.readline())
        fd.close() # legge il nome da assegnare al file di dati
        fd = open(fname, 'w') # apre il file di dati
        self.write_measurement_configuration(fd)
        start = time.time()
        if SIMUL_controller: 
            simul_dato = 0
        '''if self.measurement_mode.get() == 'step' and nmeas > 1:
            thr = grafici('ybar') # plots with errorbars
        else:
            thr = grafici('')'''
        thr = grafici('')
        thr.start()
        time.sleep(0.1)
        old_nrep = self.nrep.get()
        count = self.nrep.get()
        while count and not os.path.isfile('stop_on_point'):
            x, sx, y, sy = self.LI.read_XY(1)
            ### 2014-01-14
            
            ### 2014-03-26 non leggo la temperatura
            '''ser_temp.write('S0')
            temperatura = ser_temp.read_CR()'''
            
            ### 2014-05-20 ser_inter.pulse_DTR(0.0)
            
            ### 2014-03-07 time.sleep(0.1) # interferometer integration time
            #print misura

            dato = str(x) + '\t' + str(sx) + '\t' + str(y) + '\t' + str(sy) + '\t' + temperatura
            fd.write('nan\t' + str(time.time() - start) + '\tnan\t' + dato + '\n') # plot X, Y versus time
            fd.flush()
            open('GRAFupdate', 'w').close()
            ### delay seems not useful here, but one never knows...
            if float(self.measurement_delay.get()) != 0:
                time.sleep(float(self.measurement_delay.get()))
                if DEBUG:
                    print 'done delay in step mode'
                if LOG:
                    flog.write('done delay in step mode\n')
                ### why is it in the delay loop?
                while os.path.isfile('GRAFstop'): 
                    time.sleep(0.01)
                break
            if SIMUL_controller: 
                simul_dato += 1
            #time.sleep(0.1)
            count -= 1
            self.nrep.set(count)
            self.nrep_get.update()
        if os.path.isfile('stop_on_point'):
            os.remove('stop_on_point')
        fd.close()
        self.nrep.set(old_nrep)
        self.nrep_get.update()
        while os.path.isfile('GRAFupdate'):
            time.sleep(0.01)
        open('GRAFstop', 'w').close()
        if DEBUG:
            print 'GRAFstop created'
        if LOG:
            flog.write('GRAFstop created\n')

        #subprocess.call(MV_MEAS, shell = True)

    ### misura STEP o SCAN
    def measure_step_mode(self, nsteps, nmeas):
        #@# LI = interfacce['lockin']
        fd = open('GRAFfname', 'r')
        fname = string.strip(fd.readline())
        fd.close() # legge il nome da assegnare al file di dati
        fd = open(fname, 'w') # apre il file di dati
        ### qui aggiungere scrittura su file condizioni di misura
        self.write_measurement_configuration(fd)
        
        start = time.time()
        if SIMUL_controller: 
            simul_dato = 0
        
        countedSteps_dec = 0
        
        if self.measurement_mode.get() == 'step' and nmeas > 1:
            thr = grafici('ybar') # plots with errorbars
        else:
            thr = grafici('')
        thr.start()
        
        time.sleep(0.1)
                
        OLDpos_absolute = self.pos_absolute.get()
        OLDpos_relative = self.pos_relative.get()

        # 2013-10-31
        str1 = '%06d' % nsteps
        str2 = '1:' + str1
        
        while countedSteps_dec < self.to_go_dec:
            
            self.ser.serWrite('sx', str1) # '000001') # one single step 2013-10-31
            self.ser.serWrite('go', '')
            
            if not SIMUL_controller:
                ans = ''
                while not ans == str2: # '1:000001': 2013-10-31
                    ans = self.ser.serWrite('tp', '')
                    if DEBUG:
                        print 'waiting step to be done...',
                    if LOG:
                        flog.write('waiting step to be done\n')
                if DEBUG:
                    print 'done'

                #2013-10-11 
                countedSteps_dec += nsteps #1

                if float(self.measurement_delay.get()) != 0:
                    time.sleep(float(self.measurement_delay.get()))
                    if DEBUG:
                        print 'done delay in step mode'
                    if LOG:
                        flog.write('done delay in step mode\n')
                
                x, sx, y, sy = self.LI.read_XY(nmeas) # 5) 2013-10-31
                ### 2014-01-14
                
                ### 2014-03-26 non leggo la temperatura
                '''ser_temp.write('S0')
                temperatura = ser_temp.read_CR()'''
                
                ### 2014-05-20 ser_inter.pulse_DTR(0.005) #(0.0)
                
                ### 2014-03-07 time.sleep(0.1) # interferometer integration time
                #print misura
                dato = str(x) + '\t' + str(sx) + '\t' + str(y) + '\t' + str(sy) + '\tnan' ### 2014-03-26 + temperatura
                #dato = str(x) + '\t' + str(sx) + '\t' + str(y) + '\t' + str(sy)

                if LOG:
                    flog.write('ho letto ' + dato + '\n')
            else:
                dato = str(simul_dato) + '\n'
                time.sleep(0.01) #simula ritardo nel trasferimento del dato dal voltmetro
                if DEBUG:
                    print 'step done in simulation mode'
                if LOG:
                    flog.write('step done in simulation mode\n')
                
            d = self.segno_pos*(countedSteps_dec - 1)*self.step_size*2*2.5/2.99792458*1e-2 # delay in picoseconds
            fd.write(str(time.time() - start) + '\t' + str(self.pos_absolute.get()) + '\t' + str(d) + '\t' + dato + '\n')
            fd.flush()
            if DEBUG:
                print str(time.time() - start) + '\t' + str(self.pos_absolute.get()) + '\t' + dato
            if LOG:
                flog.write(str(time.time() - start) + '\t' + str(self.pos_absolute.get()) + '\t' + dato + '\n')
            open('GRAFupdate', 'w').close()

            self.steps_counted.set(countedSteps_dec) #int(countedSteps, 16))
            self.steps_counted_show.update() # update widget
            if DEBUG:
                print 'counted:', countedSteps_dec, '\tto go:', self.to_go_dec - countedSteps_dec
            if LOG:
                flog.write('counted:' + str(countedSteps_dec) + '\tto go:' + str(self.to_go_dec - countedSteps_dec) + '\n')
            ### update position
            NEWpos_absolute = OLDpos_absolute + self.segno_pos*countedSteps_dec*self.step_size
            self.pos_absolute_memo.write(str(NEWpos_absolute) + '\n')
            self.pos_absolute.set(NEWpos_absolute)
            self.pos_absolute_show.update()
            NEWpos_relative = OLDpos_relative + self.segno_pos*countedSteps_dec*self.step_size
            self.pos_relative_memo.write(str(NEWpos_relative) + '\n')
            self.pos_relative.set(NEWpos_relative)
            self.pos_relative_show.update()
            
            if (self.motor_status.get() == 's') or (NEWpos_absolute <= MAXtravel_guard and self.segno_pos == -1) or (NEWpos_absolute >= MAXtravel - MAXtravel_guard and self.segno_pos == 1):                                
                if DEBUG:
                    print 'stop asked or too near to limit switch'
                if LOG:
                    flog.write('stop asked or too near to limit switch\n')
                CCW_steps = self.to_go_dec - countedSteps_dec # missing steps after stop
                self.steps.set(str(CCW_steps))
                self.step_get.update()
                
                while os.path.isfile('GRAFstop'):
                    time.sleep(0.01)
                
                break

            if SIMUL_controller: 
                simul_dato += 1
            time.sleep(0.1)   
                    
        self.step_go.configure(bg = 'cyan')
        self.step_go.configure(activebackground = 'cyan')
        if DEBUG:
            print 'waiting for other steps'
        if LOG:
            flog.write('waiting for other steps\n')
        self.steps.set(self.to_go_dec*self.segno_pos)
        self.step_get.update()
        
        fd.close()

        while os.path.isfile('GRAFupdate'):
            time.sleep(0.01)
        open('GRAFstop', 'w').close()
        if DEBUG:
            print 'GRAFstop created'
        if LOG:
            flog.write('GRAFstop created\n')

        #subprocess.call(MV_MEAS, shell = True)
        
    ### qui si verifica se si misura
    def motor_go_steps(self): # max 120 000 steps (da verificare)
        '''
        la sequenza dei comandi (Test_SMC_RS232.cpp)
        1) verificare che il motore sia acceso
        2) impostare la direzione di rotazione
        3) impostare il numero di step
        4) far partire il motoreGRAFfname
        5) aspettare che il motore sia fermo
        '''
        self.step_stop.configure(bg = 'cyan')
        self.step_stop.configure(activebackground = 'cyan')
        self.step_go.configure(bg = 'green')
        self.step_go.configure(activebackground = 'green')
        
        self.move() #2011-01-31 set direction
        self.motor_status.set('n') # for condition in waiting loop (motor_go_steps)
        
        if self.go_abs_pos.get() != '':
            tmp_steps_to_go = self.steps.get()
            tmp_meas_mode = self.measurement_mode.get() # memorizza il modo di misura
            self.measurement_mode.set('OFF')
            tmp_start_velocity = self.start_v.get()
            tmp_velocity = self.max_v.get() # memorizza la velocità
            tmp_acceleration = self.max_a.get()
            self.va_set_default(self.start_v, self.max_v, self.max_a)
            tmp_step_mode = self.step_mode.get() # memorizza step_mode
            self.step_mode.set('1') # full step
            self.set_step_mode()
            
            # forse si incasina se lancio senza avere degli steps_to_go
            ### 2013-11-06 could increase movement resolution here
            self.to_go_dec = int(self.go_abs_pos.get()) - int(round(self.pos_absolute.get()))
            if self.to_go_dec < 0:
                self.direction.set('0') # CCW
                self.ser.serWrite('sh', '0')
                self.segno_pos = -1
            else:
                self.direction.set('1') # CW, to motor
                self.ser.serWrite('sh', '1')
                self.segno_pos = 1
            self.to_go_dec = abs(self.to_go_dec)
            if DEBUG:
                print 'in modo VAI A POSIZIONE'
                print 'passi da fare', self.to_go_dec
            self.to_go_hex = '%0.6x' % self.to_go_dec
            self.to_go_hex = self.to_go_hex.upper()
            self.motor_steps_count()
            
            self.measurement_mode.set(tmp_meas_mode)
            self.start_v.set(tmp_start_velocity)
            self.max_v.set(tmp_velocity)
            self.max_a.set(tmp_acceleration)
            self.va(self.start_v, self.max_v, self.max_a)
            self.step_mode.set(tmp_step_mode)
            self.set_step_mode()
            # ripristina il modo misura, velocità, step_mode e azzera go_abs_pos
            self.steps.set(tmp_steps_to_go)
            self.go_abs_pos.set('')
            return
            
        self.to_go_dec = int(self.steps.get())
        if self.to_go_dec/abs(self.to_go_dec) == 1:
            self.direction.set('1') # CW, to motor
            self.ser.serWrite('sh', '1')
            self.segno_pos = 1
            if DEBUG:
                print 'moving CW'
            if LOG:
                flog.write('moving CW\n')
            
        else:
            self.direction.set('0') # CCW
            self.ser.serWrite('sh', '0')
            self.segno_pos = -1
            if DEBUG:
                print 'moving CCW'
            if LOG:
                flog.write('moving CCW\n')
            
        self.to_go_dec = abs(self.to_go_dec)
        ### 2013-11-06 CONSIDER STEP_SIZE check if there are enough free steps
        if self.segno_pos == 1 and (MAXtravel - MAXtravel_guard - self.pos_absolute.get()) < self.to_go_dec*self.step_size:
            self.to_go_dec = 0 # MAXtravel - MAXtravel_guard - self.pos_absolute.get()
            print 'too many steps CW'
            return
        if self.segno_pos == -1 and self.pos_absolute.get() - MAXtravel_guard < self.to_go_dec*self.step_size:
            self.to_go_dec = 0 # self.pos_absolute.get() - MAXtravel_guard
            print 'too many steps CCW'
            return
        # mettere a zero i passi da fare e azzerare quelli contati. poi magari un popupmotor_go_steps

        self.to_go_hex = '%0.6x' % self.to_go_dec
        self.to_go_hex = self.to_go_hex.upper()
        #2013-04-06 self.ser.serWrite('sx', self.to_go_hex) # set number of steps
        if DEBUG:
            print 'number of steps to go:', self.to_go_dec
        if LOG:
            flog.write('number of steps to go: ' + str(self.to_go_dec) + '\n')
        
        ### si misura, se è il caso
        m = self.measure_state.get()
        if m: # misura:
            
            self.initialize_LI()
            time.sleep(0.1)

            ### 2014-02-15
            ''' aggiunto il controllo per permettere a CYCLE di scriversi il suo nome file '''
            if not os.path.isfile('GRAFfname'):
                ### 2013-11-05
                fname = time.strftime('%Y-%m-%dT%H%M%S',time.localtime())
                if self.filename.get() != '':
                    fname += ('_' + self.filename.get())
                fname += ('_' + self.measurement_mode.get() + '.dat')
    
                fd = open('GRAFfname', 'w')
                fd.write(fname)
                fd.close()
            ### end 2014-02-15
            
            ### 2014-02-15 magari serve... fd = open(fname, 'w') # perchè lo apro qui
            
            if self.measurement_mode.get() == 'continuous':
                ### 2014-03-13 open('MISon', 'w').close()
                if DEBUG:
                    print 'starting measurement thread for continuous acquisition'
                if LOG:
                    flog.write('starting measurement thread for continuous acquisition\n')
                
                ### 2014-03-11 thr_mis = misura(self.pos_absolute, self.measurement_mode)
                fd = open(fname, 'w')
                self.write_measurement_configuration(fd)
                fd.flush()
                fd.close()
                
                thr_mis = misuraContinua(self.pos_absolute, self.measurement_mode) ### 2014-03-11
                thr_mis.start()
                self.motor_steps_count()
                thr_mis.stop()
                
            if self.measurement_mode.get() == 'step':
                if DEBUG:
                    print 'entering step measuring mode'
                if LOG:
                    flog.write('entering step measuring mode\n')

                self.measure_step_mode(1, 1)#5) # 2013-10-31 one step, average on five measurements

            if self.measurement_mode.get() == 'fast':
                ### 2014-03-13 open('MISon', 'w').close()
                if DEBUG:
                    print 'starting measurement thread for fast, continuous acquisition'
                if LOG:
                    flog.write('starting measurement thread for fast, continuous acquisition\n')
                
                ### 2014-03-11 thr_mis = misura(self.pos_absolute, self.measurement_mode)
                fd = open(fname, 'w')
                self.write_measurement_configuration(fd)
                fd.flush()
                fd.close()

                ### 2014-09-25
                if INTERFEROMETER:
                    if not os.path.isfile('/home/marco/hp5529a/RUNNING_win'):
                        mess = 'interferometer SW not running!\n\nstart it and press OK'            
                        result = tkMessageBox.showerror(message = mess)
                        while not result:
                            time.sleep(0.1)
                ### end 2014-09-25
                            
                ### 2014-09-30 thr_mis = misuraVeloce(self.pos_absolute, self.measurement_mode) ### 2014-03-11
                thr_mis = misuraVeloce(self.pos_absolute.get(), self.segno_pos, self.step_size, self.to_go_dec) ### 2014-03-11
                thr_mis.start()
                
                ### 2014-09-25
                if INTERFEROMETER:
                    ### 2014-05-13 don't start before interferometer has been started by misuraVeloce
                    while not os.path.isfile('/home/marco/hp5529a/STARTED_win'):
                        time.sleep(0.001)
                    time.sleep(1) # just to be sure that the WIN machine is ready to acquire...
                ### end 2014-09-25
                    
                self.motor_steps_count()
                thr_mis.stop()
                
            if self.measurement_mode.get() == 'scan':
                if DEBUG:
                    print 'entering fast scanning mode'
                if LOG:
                    flog.write('entering fast scanning mode\n')

                self.measure_step_mode(6, 1) # 2013-10-31 two steps, single measurement
                
            if self.measurement_mode.get() == 'on_point':
                self.measure_on_point_mode()

        #if DEBUG:
            #print 'now going in', self.measurement_mode.get(), 'measurement mode'
        if self.measurement_mode.get() == 'OFF':
            self.motor_steps_count()
            
    def motor_steps_count(self):
        #solo se ho impostato degli step. se cerco sw non funziona
        if SIMUL_controller:
            countedSteps_hex = '1:000001'
        else:
            if self.measurement_mode.get() == 'step':
                countedSteps_dec = 0
                
        OLDpos_absolute = self.pos_absolute.get()
        OLDpos_relative = self.pos_relative.get()

        if self.measurement_mode.get() == 'OFF':
            if DEBUG:
                print 'will not measure'
            if LOG:
                flog.write('will not measure\n')
            self.ser.serWrite('sx', self.to_go_hex) # set number of steps
            self.ser.serWrite('go', '')
            
        ### 2014-05-12
        ''' if self.measurement_mode.get() == 'continuous': '''
        if (self.measurement_mode.get() == 'continuous') or (self.measurement_mode.get() == 'fast'):
            if DEBUG:
                print 'will measure in continuous mode'
            if LOG:
                flog.write('will measure in continuous mode\n')
            self.ser.serWrite('sx', self.to_go_hex) # set number of steps
            self.ser.serWrite('go', '')
            ### 201-03-13 open('MISdo', 'w').close()
        
        while True:
            if self.measurement_mode.get() == 'step':
                
                if DEBUG:
                    print 'will measure in step mode'
                if LOG:
                    flog.write('will measure in step mode\n')
                self.ser.serWrite('sx', '000001') # one single steps
                self.ser.serWrite('go', '')
                ans = ''
                while not ans == '1:000001':
                    ans = self.ser.serWrite('tp', '')
                    if DEBUG:
                        print 'waiting step to be done'
                    if LOG:
                        flog.write('waiting step to be done\n')
                open('MISdo', 'w').close() #2013-04-08
                
                if float(self.measurement_delay.get()) != 0:
                    time.sleep(float(self.measurement_delay.get()))
                    if DEBUG:
                        print 'done delay in step mode'
                    if LOG:
                        flog.write('done delay in step mode\n')
                
            if self.measurement_mode.get() == 'step':
                if not SIMUL_controller:
                    countedSteps_dec += 1
            else: # update steps done
                if not SIMUL_controller:
                    countedSteps_hex = self.ser.serWrite('tp', '')
                countedSteps_hex = countedSteps_hex.split(':')[1]
                countedSteps_dec = int(countedSteps_hex, 16)
                
            self.steps_counted.set(countedSteps_dec) #int(countedSteps, 16))
            self.steps_counted_show.update() # update widget
            if DEBUG:
                print 'counted:', countedSteps_dec, '\tto go:', self.to_go_dec - countedSteps_dec
            if LOG:
                flog.write('counted: ' + str(countedSteps_dec) + '\tto go: ' + str(self.to_go_dec - countedSteps_dec) + '\n')
            ### update position
            NEWpos_absolute = OLDpos_absolute + self.segno_pos*countedSteps_dec*self.step_size
            self.pos_absolute_memo.write(str(NEWpos_absolute) + '\n')
            self.pos_absolute.set(NEWpos_absolute)
            self.pos_absolute_show.update()
            NEWpos_relative = OLDpos_relative + self.segno_pos*countedSteps_dec*self.step_size
            self.pos_relative_memo.write(str(NEWpos_relative) + '\n')
            self.pos_relative.set(NEWpos_relative)
            self.pos_relative_show.update()
            
            #if ((countedSteps_dec >= self.to_go_dec) or (self.motor_status.get() == 's')): #or (NEWpos_absolute <= 100 and segno_posizione == -1) or (NEWpos_absolute >= (MAXtravel - 100) and segno_posizione == 1)):
            if (countedSteps_dec >= self.to_go_dec) or (self.motor_status.get() == 's') or (NEWpos_absolute <= MAXtravel_guard and self.segno_pos == -1) or (NEWpos_absolute >= MAXtravel - MAXtravel_guard and self.segno_pos == 1):
                                
                if DEBUG:
                    print 'steps done or stop asked or too near to limit switch'
                if LOG:
                    flog.write('steps done or stop asked or too near to limit switch\n')
                
                CCW_steps = self.to_go_dec - countedSteps_dec # missing steps after stop
                self.steps.set(str(CCW_steps))
                self.step_get.update()
                if os.path.isfile('MISon'):
                    os.remove('MISon')
                
                while os.path.isfile('GRAFstop'):
                    time.sleep(0.01)
                
                break
            if SIMUL_controller:
                cS = countedSteps_dec + 1 #int(countedSteps, 16) + 1
                countedSteps_hex = '1:' + ('%0.6x' % cS) #2011-01-31 int(cS))
                time.sleep(0.1)
                
            if self.measurement_mode.get == 'step':
                while os.path.isfile('MISdo'):
                    time.sleep(0.001)
                    
        self.step_go.configure(bg = 'cyan')
        self.step_go.configure(activebackground = 'cyan')
        if DEBUG:
            print 'waiting for other steps'
        if LOG:
            flog.write('waiting for other steps\n')
        
        self.steps.set(self.to_go_dec*self.segno_pos)
        self.step_get.update()
        
    def motor_status_set(self):
        stat = 'm' + self.motor_status.get()
        if stat == 'ms':
            self.step_stop.configure(bg = 'red')
            self.step_stop.configure(activebackground = 'red')
            self.step_go.configure(bg = 'cyan')
            self.step_go.configure(activebackground = 'cyan')

        self.ser.serWrite(stat, '')
        
        if DEBUG:
            if stat == 'mf':
                print 'motor off'
            elif stat == 'mb':
                print 'motor stand-by'
            elif stat == 'ms':
                print 'motor stop'
            else:
                print 'motor on'

        if LOG:
            if stat == 'mf':
                if LOG:
                    flog.write('motor off\n')
            elif stat == 'mb':
                if LOG:
                    flog.write('motor stand-by\n')
            elif stat == 'ms':
                if LOG:
                    flog.write('motor stop\n')
            else:
               if LOG:
                   flog.write('motor on\n')
        
    def motor_stop(self):
        self.motor_status.set('s')
        self.step_stop.configure(bg = 'red')
        self.step_go.configure(bg = 'cyan')
        if DEBUG:
            print 'requiring motor stop'
        if LOG:
            flog.write('requiring motor stop\n')
        self.motor_status_set()
        
    #def move(self, dir):
    def move(self):
        d = self.direction.get()
        ans = self.ser.serWrite('sh', d)
        if DEBUG:
            print 'move direction:', ans
        if LOG:
            flog.write('move direction: ' + str(ans) + '\n')
    
    def move_files_to_dropbox(self):
        subprocess.call(MV_MEAS, shell = True)
        
    def pos_absolute_reset_action(self):
        choice = tkMessageBox.askokcancel(message = 'Really reset the position ?')
        if choice:
            choice1 = tkMessageBox.askquestion(message = 'will reset to zero (side opposite to motor)\nReset to ' + str(MAXtravel) + ' instead (motor side)?')
            if choice1 == 'yes':
                self.pos_absolute.set(MAXtravel)
                self.pos_absolute_show.update()
                self.pos_absolute_memo.write(str(MAXtravel) + '\n')
            else:
                self.pos_absolute.set(0.)
                self.pos_absolute_show.update()
                self.pos_absolute_memo.write('0\n')
            
    '''say goodbay def say_goodbye(self):
        self.p'''
            
    def serial_read(self):
        rd = self.ser.read()
        self.serial_read_text.set(rd)

    
    def serial_write(self): # questa è da rivedere, devo chiamare serWrite e passargli come comando il comando+dati, e come dati la stringa vuota. informare nella gui che 'A1' non è necessario
        self.serial_read_text.set('')
        wr = self.serial_write_text.get()
        ans = self.ser.serWrite(wr, '')
        if DEBUG:
            print 'manual wrote:', wr
            print 'ans:', ans
        if LOG:
            flog.write('manual wrote: ' + str(wr) + '\n' + str(ans) + '\n')
        self.serial_read_text.set(ans)
        self.serial_write_text.set('')
        
    def set_full_travel(self):
        self.steps.set(str(MAXtravel*self.step_size))
        
    def set_step_mode(self):
        m = self.step_mode.get()
        self.ser.serWrite('sr', m)
        if DEBUG:
            print 'set step mode:', m
        if m == '1':
            self.step_size = 1.0
        elif m == '2':
            self.step_size = 0.5
        elif m == '3':
            self.step_size = 0.25
        elif m == '4':
            self.step_size = 0.125
        else:
            print 'non ce ne e\''

    def sw_CCW_find(self):
        choice = tkMessageBox.askokcancel(message = 'This will probably reset the position counter.\nAlso, speed and acceleration can\'t be set and\nspeed is low.\nProceed?')
        if choice: 
            self.ser.serWrite('mr', '0')
            if DEBUG:
                print 'finding sw_CCW'
            if LOG:
                flog.write('finding sw_CCW\n')
            
            self.ser.serWrite('go', '')
            self.step_stop.configure(bg = 'cyan')
            self.step_stop.update()
            self.step_go.configure(bg = 'green')
            self.step_go.update()

            while True:
                stat = self.ser.serWrite('t', '2')
                if stat == '1:01':
                    print 'ci sono'
                    break
                time.sleep(0.5)

            self.pos_absolute.set(0.)
            self.pos_absolute_show.update()
            self.pos_absolute_memo.write('0\n')

    def sw_CW_find(self):
        choice = tkMessageBox.askokcancel(message = 'This will probably reset the position counter.\nAlso, speed and acceleration can\'t be set and\nspeed is low.\nProceed?')
        if choice:
            self.ser.serWrite('mr', '1')
            if DEBUG:
                print 'finding sw_CW'
            if LOG:
                flog.write('finding sw_CW\n')
            self.ser.serWrite('go', '')
            self.step_stop.configure(bg = 'cyan')
            self.step_stop.update()
            self.step_go.configure(bg = 'green')
            self.step_go.update()
            
            while True:
                stat = self.ser.serWrite('t', '1')
                if stat == '1:01':
                    print 'ci sono'
                    break
                time.sleep(0.5)
                
            self.pos_absolute.set(MAXtravel)
            self.pos_absolute_show.update()
            self.pos_absolute_memo.write(str(130000) + '\n')
            
    def sw_CCW_get_state(self):
        if SIMUL_controller:
            count = 20
        
        while True:
            if not SIMUL_controller:
                sw_CCW_status = self.ser.serWrite('t1', '')
            else:
                if count > 0:
                    sw_CCW_status = '1:00'
                else:
                    sw_CCW_status = '1:01'
            
            self.update() # magicamente, fa si che il loop si arresti correttamente dopo la richiesta di stop...
            
            if DEBUG:
                print sw_CCW_status
                if sw_CCW_status == '1:00':
                    print 'sw_CCW not active'
                else:
                    print 'sw_CCW active'
                
            if sw_CCW_status == '1:01':
                if DEBUG:
                    print 'sw_CCW found'
                break
            elif self.motor_status.get() == 's':
                if DEBUG:
                    print 'stop required while finding sw_CCW'
                break
            time.sleep(1)

            if SIMUL_controller:
                time.sleep(.1)
                count -= 1
                
    def sw_CW_get_state(self):
        if SIMUL_controller:
            count = 20
        
        while True:
            if not SIMUL_controller:
                sw_CW_status = self.ser.serWrite('t2', '')
            else:
                if count > 0:
                    sw_CW_status = '1:00'
                else:
                    sw_CW_status = '1:01'
            
            self.update() # magicamente, fa si che il loop si arresti correttamente dopo la richiesta di stop...
            
            if DEBUG:
                print sw_CW_status
                if sw_CW_status == '1:00':
                    print 'sw_CW not active'
                else:
                    print 'sw_CW active'
                
            if sw_CW_status == '1:01':
                if DEBUG:
                    print 'sw_CW found'
                break
            elif self.motor_status.get() == 's':
                if DEBUG:
                    print 'stop required while finding sw_CW'
                break
            time.sleep(1)
            
            if SIMUL_controller:
                time.sleep(.1)
                count -= 1

    def sw_CCW_set(self):
        s = self.sw_CCW_state.get()
        if s == 0:
            self.ser.serWrite('sf', '1')
        if s == 1:
            self.ser.serWrite('sn', '1')
        if DEBUG:
            print 'sw_CCW state:', s
            
    def sw_CW_set(self):
        s = self.sw_CW_state.get()
        if s == 0:
            self.ser.serWrite('sf', '2')
        if s == 1:
            self.ser.serWrite('sn', '2')
        if DEBUG:
            print 'sw_CW state:', s

    def tune_delay(self, s):
        self.steps.set(s)
        tmp_meas_mode = self.measurement_mode.get() # memorizza il modo di misura
        self.measurement_mode.set('OFF')
        tmp_measure_state = self.measure_state.get()
        self.measure_state.set(0)
        self.motor_go_steps()
        self.measurement_mode.set(tmp_meas_mode)
        self.measure_state.set(tmp_measure_state)
        
    def update_plot(self, t0, t_wait):
        '''
        given t0, the program execution starting time, we check with 1 s resolution
        for the elapsed time t_wait before updating the plot
        '''
        self.t0 = t0
        self.t_wait = t_wait
        while True:
            if not ((int(time.time()) - t0) % t_wait): break
            time.sleep(1)
        open('GRAFupdate', 'w').close()
        
    def va(self, sv, mv, ma):
        startvel = ('%0.2x' % (255 - 254./99.*(int(sv.get()) - 1))).upper()
        maxvel = ('%0.2x' % (255 - 254./99.*(int(mv.get()) - 1))).upper()
        acc = ('%0.2x' % (255 - 254./99.*(int(ma.get()) - 1))).upper()
        self.ser.serWrite('sl', startvel)
        self.ser.serWrite('sv', maxvel)
        self.ser.serWrite('sa', acc)
        if DEBUG:
            print 'start velocity:', startvel
            print 'max velocity:', maxvel
            print 'acceleration:', acc
        
    def va_set_default(self, sv, mv, ma):
        sv.set('01')
        mv.set('01') #65')
        ma.set('01') #90')
        self.va(sv, mv, ma)
        if DEBUG:
            print 'vel & acc set to default values'
        # non funziona lambda arg1 = sv, arg2 = mv, arg3 = ma: va(arg1, arg2, arg3)

    ### 2014-10-10
    def vai_motore(self): 
        if self.go_abs_pos.get() != '' or self.measurement_mode.get() != 'fast':
            self.motor_go_steps()
        else:
            starting_position = self.pos_absolute.get()
            self.motor_go_steps()
            self.go_abs_pos.set(str(int(starting_position)))
            time.sleep(0.5)
            self.motor_go_steps()
        
    ### write measurement configuration to data file
    def write_measurement_configuration(self, fd):
        ### LI = interfacce['lockin']
        ### sensitivity, reserve_mode, time_constant, filter_slope = LI.read_configuration()
        ### fd.write('# LOCK-IN\n#\t\tsensitivity: %s\n#\t\treserve mode: %s\n#\t\ttime constant: %s\n#\t\tfilter slope: %s\n' \
        ###            % (sensitivity, reserve_mode, time_constant, filter_slope))
        fd.write('#\n#\tstep size: %s um\n#\tmeasurement mode: %s\n#\tdelay between measurements: %s\n#\n' \
                    % (self.step_size*2.5, self.measurement_mode.get(), self.measurement_delay.get()))
        fd.write('#\tfrom %s to %s\n#\n' % (int(self.pos_absolute.get()), int(self.pos_absolute.get()) + self.step_size*int(self.steps.get())))
        fd.write('#time (s)\tstep #\tdelay (s)\tX (V)\t X s.d.\tY (V)\tY s.d.\t temperature (°C)\n')
        fd.flush()
        return
        
    def z_estimate_stage_speed(self):
        tmp_steps_to_go = self.steps.get()
        tmp_meas_mode = self.measurement_mode.get() # memorizza il modo di misura
        self.measurement_mode.set('OFF')
        tmp_start_velocity = self.start_v.get()
        tmp_velocity = self.max_v.get() # memorizza la velocità
        tmp_acceleration = self.max_a.get()
        self.va_set_default(self.start_v, self.max_v, self.max_a)
        tmp_step_mode = self.step_mode.get() # memorizza step_mode
        self.step_mode.set('4') # 1/8 step
        self.set_step_mode()
        
        if options.fwspeed:
            self.to_go_dec = 8000
            self.direction.set('1') # CW, to motor
            self.ser.serWrite('sh', '1')
            self.segno_pos = 1
            #self.to_go_dec = abs(self.to_go_dec)
            self.to_go_hex = '%0.6x' % self.to_go_dec
            self.to_go_hex = self.to_go_hex.upper()
            start = time.time()
            self.motor_steps_count()
            print 'estimated stage forward speed: ' + str(self.to_go_dec/(time.time() - start)/8) + ' step/sec'
        if options.bwspeed:
            self.to_go_dec = 8000
            self.direction.set('0') # CCW
            self.ser.serWrite('sh', '0')
            self.segno_pos = -1
            #self.to_go_dec = abs(self.to_go_dec)
            self.to_go_hex = '%0.6x' % self.to_go_dec
            self.to_go_hex = self.to_go_hex.upper()
            start = time.time()
            self.motor_steps_count()
            print 'estimated stage backward speed: ' + str(self.to_go_dec/(time.time() - start)/8) + ' step/sec'
  
        self.measurement_mode.set(tmp_meas_mode)
        self.start_v.set(tmp_start_velocity)
        self.max_v.set(tmp_velocity)
        self.max_a.set(tmp_acceleration)
        self.va(self.start_v, self.max_v, self.max_a)
        self.step_mode.set(tmp_step_mode)
        self.set_step_mode()
        # ripristina il modo misura, velocità, step_mode e azzera go_abs_pos
        self.steps.set(tmp_steps_to_go)
        self.go_abs_pos.set('')
        return

        
class grafici(threading.Thread):
    def __init__(self, mode):#, fname):#x, y):
        threading.Thread.__init__(self)
        self.mode = mode

    def run(self):
        while not os.path.isfile('GRAFfname'):
            time.sleep(0.01)
        fd = open('GRAFfname', 'r')
        fname = string.strip(fd.readline())
        fd.close()
        os.remove('GRAFfname')
        
        GP = Gnuplot.Gnuplot(persist = True)
        GP('set term x11')
        GP('clear')
        titolo = 'set title "%s"' % fname
        GP(titolo)
        
        ### 2013-11-05 scientific notation in y-axis
        GP('set format y "%2.1E"')
        
        # set x2tics
        # gnuplot> plot [0:5*pi] sin(x) with lines, 2*sin(2*x) with lines axes x2y1
        if self.mode == '':
            grafo = 'plot "%s" using 2:4 with lines title "X" lc rgb "red",\
                    "" using 2:6 with lines title "Y" lc rgb "blue"' % fname #,\
            #@#grafo = 'plot "%s" using 2:3 with lines title "X" lc rgb "red", "" using 2:5 with lines title "Y" lc rgb "blue"' % fname
        if self.mode == 'ybar':
            grafo = 'plot "%s" using 2:4:5 with yerrorbars title "X" pointsize 2 lc rgb "red",\
                    "" using 2:4 with lines notitle lc rgb "red",\
                    "" using 2:6:7 with yerrorbars title "Y" pointsize 2 lc rgb "blue",\
                    "" using 2:6 with lines notitle lc rgb "blue"' % fname #,\
            #@#grafo = 'plot "%s" using 2:3:4 with yerrorbars title "X" pointsize 2 lc rgb "red", "" using 2:3 with lines notitle lc rgb "red", "" using 2:5:6 with yerrorbars title "Y" pointsize 2 lc rgb "blue", "" using 2:5 with lines notitle lc rgb "blue"' % fname
                #"" using 2:(sqrt($3**2+$5**2)) with linespoints pointsize 2 title "modulus" lc rgb "black"' % fname
        # no YERRORBARS e LINESPOINTS insieme

        while not os.path.isfile('GRAFstop'):
            time.sleep(0.1)
            while os.path.isfile('GRAFupdate'):
                GP(grafo)
                if os.path.isfile('GRAFupdate'):
                    os.remove('GRAFupdate')
                if DEBUG:
                    print 'GRAFupdate removed'
        if os.path.isfile('GRAFstop'):
            os.remove('GRAFstop')
        GP('set term png font small')
        GP('set output "' + fname + '.png"')
        GP('replot')
        if DEBUG:
            print 'GRAFstop removed'
        if LOG:
            flog.write('GRAFstop removed\n')

        while not os.path.isfile(fname + '.png'):
            time.sleep(0.2)
            
        # now that everything is done, it should be safe to move files to the Dropbox...
        subprocess.call(MV_MEAS, shell = True)       
        
    def stop(self):
        self.running = False

class misura(threading.Thread):
    def __init__(self, pos, mode):
        ''' ### 2014-02-14 def __init__(self, pos, mode, step_size, measurement_mode, measurement_delay):'''
        threading.Thread.__init__(self)
        self.pos = pos # position, from 'motor_steps_count'
        self.mode = mode # continuous or step
        '''### 2014-02-14 self.step_size = step_size
        self.measurement_mode =  measurement_mode
        self.measurement_delay = measurement_delay ### end 2014-02-14 '''
        
    def run(self):
        LI = interfacce['lockin']

        fd = open('GRAFfname', 'r')
        fname = string.strip(fd.readline())
        fd.close()
        
        fd = open(fname, 'w')
        '''### 2014-02-14
        fd.write('#\n#\tstep size: %s um\n#\tmeasurement mode: %s\n#\tdelay between measurements: %s\n#\n' \
                    % (self.step_size*2.5, self.measurement_mode, self.measurement_delay))
        fd.write('#time (s)\tstep #\tdelay (ps)\tX (V)\t X s.d.\tY (V)\tY s.d.\t temperature (°C)\n')
        '''### end 2014-02-14 non serve, deve avere già scritto le condizioni di misura all'apertura del file
        fd.flush()
        
        start = time.time()
        ### 2013-11-06 start_pos = self.pos.get()
        if SIMUL_controller:
            simul_dato = 0
        
        thr = grafici('')
        thr.start()
        
        time.sleep(0.1)
        
        start_pos = self.pos.get()
        
        while os.path.isfile('MISon'):
            while not os.path.isfile('MISdo'):
                time.sleep(0.001)
            if not SIMUL_controller:
                x, sx, y, sy = LI.read_XY(1)
                
                ### 2014-01-14 BEGIN
                
                ### 2014-03-26 non leggo la temperatura
                '''ser_temp.write('S0')
                temperatura = ser_temp.read_CR()'''
                
                ### 2014-05-20 ser_inter.pulse_DTR(0.0)
                
                ### 2014-03-07 time.sleep(0.1) # interferometer integration time
                #print misura
                ### 2014-01-14 END

                dato = str(x) + '\t' + str(sx) + '\t' + str(y) + '\t' + str(sy) + '\tnan' ### 2014-03-26 + temperatura
                #dato = str(x) + '\t' + str(sx) + '\t' + str(y) + '\t' + str(sy)
                if DEBUG:
                    print 'ho letto', dato
                if LOG:
                    flog.write('ho letto ' + dato + '\n')
            else:
                dato = str(simul_dato) + '\n'
                time.sleep(0.01) #simula ritardo nel trasferimento del dato dal voltmetro
            d = (self.pos.get() - start_pos)*2*2.5/2.99792458*1e-2 # delay in picoseconds
            fd.write(str(time.time() - start) + '\t' + str(self.pos.get()) + '\t' + str(d) + '\t' + dato + '\n')
            fd.flush()
            if DEBUG:
                print str(time.time() - start) + '\t' + str(self.pos.get()) + '\t' + dato
            if LOG:
                flog.write(str(time.time() - start) + '\t' + str(self.pos.get()) + '\t' + dato + '\n')
            open('GRAFupdate', 'w').close()
            #if DEBUG: 
                #print 'GRAFupdate created'
            if self.mode.get() == 'step':
                if os.path.isfile('MISdo'): 
                    os.remove('MISdo')
                    if DEBUG:
                        print 'MISdo removed in step mode'
                    if LOG:
                        flog.write('MISdo removed in step mode\n')
            if SIMUL_controller: 
                simul_dato += 1
                time.sleep(0.01)

        fd.close()

        while os.path.isfile('GRAFupdate'):
            time.sleep(0.01)
        open('GRAFstop', 'w').close()
        if DEBUG:
            print 'GRAFstop created'
        if LOG:
            flog.write('GRAFstop created\n')

        #subprocess.call(MV_MEAS, shell = True)
        
    def stop(self):
        if os.path.isfile('MISon'):
            os.remove('MISon')
        self.running = False

class misuraContinua(threading.Thread):
    '''
    rimuovere grafico e spostare il log delle condizioni di misura su file alla fine del processo di misura
    '''
    def __init__(self, pos, mode):
        ''' ### 2014-02-14 def __init__(self, pos, mode, step_size, measurement_mode, measurement_delay):'''
        threading.Thread.__init__(self)
        self.pos = pos # position, from 'motor_steps_count'
        self.mode = mode # continuous or step
        self.ask_to_stop = threading.Event()
        '''### 2014-02-14 self.step_size = step_size
        self.measurement_mode =  measurement_mode
        self.measurement_delay = measurement_delay ### end 2014-02-14 '''
        
    def run(self):
        LI = interfacce['lockin']
        LI.prepare_scan() # prepares for triggered acquisition
        t0 = time.time()
        
        ### 2014-05-20 while not self.ask_to_stop.isSet():
            ### 2014-05-20 ser_inter.pulse_DTR(0.001)
            #LI.write('TRIG')
            ### 2014-05-20 time.sleep(0.001) # do nothing until all data are collected
        
        t1 = time.time()
        chX, chY = LI.stop_scan()
        
        t = [None for i in range(len(chX))]
        t[0] = 0.
        t[-1] = t1 - t0

        fd = open('GRAFfname', 'r')
        fname = string.strip(fd.readline())
        fd.close()
        os.remove('GRAFfname')

        fd = open(fname, 'a')
        for i in range(len(chX)):
            fd.write(str(t[i]) + '\tnan' + '\tnan' + '\t' + str(chX[i]) + '\tnan\t' +str (chY[i]) + '\tnan' + '\tnan' +'\n')
        fd.close()
        
        time.sleep(0.5)
        subprocess.call(MV_MEAS, shell = True)
        
    def stop(self):
        self.ask_to_stop.set()

class misuraVeloce(threading.Thread):
    '''
    rimuovere grafico e spostare il log delle condizioni di misura su file alla fine del processo di misura
    '''
    def __init__(self, starting_pos, direction_sign, step_size, to_go):
        ''' ### 2014-02-14 def __init__(self, pos, mode, step_size, measurement_mode, measurement_delay):'''
        threading.Thread.__init__(self)
        self.starting_pos = starting_pos # position, from 'motor_steps_count'
        self.direction_sign = direction_sign # continuous or step
        self.s_s = step_size#*2 # trigger ogni 2 steps!
        self.t_g = to_go
        self.ask_to_stop = threading.Event()
        '''### 2014-02-14 self.step_size = step_size
        self.measurement_mode =  measurement_mode
        self.measurement_delay = measurement_delay ### end 2014-02-14 '''

    def run(self):
        LI = interfacce['lockin']
        LI.prepare_scan() # prepares for triggered acquisition

        t0 = time.time()
        
        ### 2014-09-25
        if INTERFEROMETER:
            os.system('cp GRAFfname /home/marco/hp5529a/FNAME_win') # prepares filename for data saving
            open('/home/marco/hp5529a/START_win', 'w').close() # starts the interferometer SW on win machine
        ### end 2014-09-25
            
        print 'here we go in fast acquisition mode'
        while not self.ask_to_stop.isSet():
            ### 2014-05-20 ser_inter.pulse_DTR(0.001) # generates a pulse 0.001 long
            #LI.write('TRIG')
            time.sleep(0.01) # do nothing until all data are collected
        print 'acquisition terminated'
        
        ### 2014-09-25
        if INTERFEROMETER:
            open('/home/marco/hp5529a/STOP_win', 'w').close() # stops the interferometer SW on win machine
            print 'asked hp to stop'
        ### end 2014-09-25

        print 'please, wait while data are saved to file'
        t1 = time.time()
        chX, chY = LI.stop_scan() #, chY
        if len(chX) != 0: # got something from lockin
            print 'read ' + str(len(chX)) + ' samples from lockin'
            
            fd = open('GRAFfname', 'r')
            fname = string.strip(fd.readline())
            fd.close()
            ### 2014-09-29 os.remove('GRAFfname')

            thr_grafico = grafici('')
            thr_grafico.start()
    
            ### 2014-09-25
            if INTERFEROMETER:
                fn = '/home/marco/hp5529a/' + fname.split('.')[0] + '_win.dat'
                '''while not os.path.isfile(fn):
                        time.sleep(0.1)'''
                if os.path.isfile(fn):
                    ##fd_interf = open(fn, 'r')
                    L, T = ut.file_read_two(fn) ##fd_interf)
                    ##fd_interf.close()
                    print 'read ' + str(len(L)) + ' samples from interferometer'
            
                    # look for a common length in the locking and interferometer data sets
                    if len(chX) > len(L):
                        I = len(L)
                    else:
                        I = len(chX)
            
                    fd = open(fname, 'a')
                    fd.write('# total acquisition time = ' + str(T[-1] - T[0]) + "che unità?\n")
                    #fd.write('# total acquisition time = ' + str(T[i-1] - T[0]) + "che unità?\n")
                    for i in range(I): #len(chX)):
                        fd.write(str(t[i]) + '\t' + str(T[i]) + '\t' + str(L[i]*2/2.99792458*1e-2) + '\t' + str(chX[i]) + '\tnan\t' + str(chY[i]) + '\tnan' + '\tnan' +'\n')
                    fd.close()
                    
                    time.sleep(0.5)
                    subprocess.call(MV_MEAS, shell = True)
                else:
                    print 'nothing from the interferometer'
            else:
                I = len(chX)
                # not really the total execution time, but not so different...
                fd = open(fname, 'a')
                ### 2014-11-12 fd.write('# approximate acquisition time = ' + str(t1 - t0) + ' s\n')
                if self.direction_sign == -1: # reverse chX and chY for increasing delays
                    chX.reverse()
                    chY.reverse()
                    p = [self.starting_pos - self.t_g*self.s_s + 2*i*self.s_s for i in range(I)]
                else:
                    p = [self.starting_pos + 2*i*self.s_s for i in range(I)]
                for i in range(I): #len(chX)):
                    ### fd.write('0' + '\t' + str(self.starting_pos + (2*i/self.s_s - self.t_g)*self.s_s) + '\t' + str(i*2*self.s_s*STEP_SIZE/2.99792458*1e-2*1e-12) + '\t' + str(chX[i]) + '\tnan\t' + str(chY[i]) + '\tnan' + '\tnan' +'\n')
                    fd.write('0' + '\t' + str(p[i]) + '\t' + str(i*2*self.s_s*STEP_SIZE/2.99792458*1e-2*1e-12) + '\t' + str(chX[i]) + '\tnan\t' + str(chY[i]) + '\tnan' + '\tnan' +'\n')
                fd.close()
                
                time.sleep(0.5)
                ### 2014-09-29 subprocess.call(MV_MEAS, shell = True)
                ### 2014-09-29 c'è stessa chiamata in grafici
                
            ### end 2014-09-25
            
            '''chX, chY = LI.re_read_binary()
            fd = open('ascii.dat', 'w')
            for i in range(I): #len(chX)):
                    fd.write(str(t[i]) + '\t' + str(self.starting_pos + self.direction_sign*i) + '\t' + str(i*2*2.5/2.99792458*1e-2) + '\t' + str(chX[i]) + '\tnan\t' + str(chY[i]) + '\tnan' + '\tnan' +'\n')
            fd.close()'''
            
            '''thr_grafico = grafici('')
            thr_grafico.start()'''
            ### 2014-09-29
            open('GRAFupdate', 'w').close()
            print 'data saved'
            ### 2014-09-29
            while os.path.isfile('GRAFupdate'):
                time.sleep(0.1)
            open('GRAFstop', 'w').close()
        else:
            print 'nothing from the lockin'
        
    def stop(self):
        self.ask_to_stop.set()

class seriale:
    ### 2014-01-14 def __init__(self):
    def __init__(self, serial_type, serialSN, baud, timeout, bytesize, parity, stopbits, xonxoff, rtscts, dsrdtr):
        self.baud = baud
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        
        if not SIMUL_controller:
            ### 2014-01-14 self.porta = get_USB_serial.findSerial('FTUSMK0') ### 2013-10-08 [x for x in self.name if re.search('ttyUSB', x)]
            if serial_type == 'short':
                print 'look for short'
                self.porta = get_USB_serial.findShortSerial(serialSN)
            else:
                print 'look for long'
                self.porta = get_USB_serial.findSerial(serialSN)
            
            ### 2014-01-14 self.ser = serial.Serial(self.porta, 9600, timeout=0.1, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0) # timeout=5
            self.ser = serial.Serial(port = self.porta, baudrate = self.baud, timeout = self.timeout, bytesize = self.bytesize, parity = self.parity, stopbits = self.stopbits, xonxoff = self.xonxoff, rtscts = self.rtscts, dsrdtr = self.dsrdtr) # timeout=5

            """if self.dsrdtr:
                self.ser.setDTR(False) # deassert DTR before opening the port in order to avoid first UNWANTED interf meas
                time.sleep(0.5)
                print 'deasserted DTR before opening port'"""
            self.ser.open()
            print self.porta, 'active:', self.ser.isOpen()
        else:
            print 'simulazione controller'
            self.ser = serial.Serial(port='/dev/ttyS10', baudrate=9600, timeout=0.1, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, dsrdtr = False) # timeout=5
            self.ser.open()
            print '/dev/ttyS10 active:', self.ser.isOpen()

    ### 2014-01-14 BEGIN
    def close(self):
        self.ser.close()
        
    def open(self):
        self.ser.open()
        
    def pulse_DTR(self, dt):
        ''' generates a trigger-like signal on DTR '''
        self.ser.setDTR(False)
        time.sleep(dt) # was 0.05 delay shifted in measuring routines, this is a thread!!! default integration time is 100 ms, we leave some margin
        self.ser.setDTR(True)
        
    def read_CR(self):
        stringa = ''
        while True:
            s = self.ser.read(1)#   ser.read(1)
            stringa += s
            if s == '\r':
                break
        stringa = stringa.strip()
        return stringa
    ### 2014-01-14 END
            
    def read(self): # !!! impostare timeout !!!
        ans = ''
        while True:
            rd = self.ser.read(1) # get one character
            if not rd: # if nothing is get, exit
                break
            ans += rd # build received message
        return ans.strip() # get rid of trailing and leading \r, \n

    def scan(self):
        """scan for available ports. return a list of device names."""
        return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')
        
    def serWrite(self, cmd, data):
        txt = 'A' + dev + cmd + data
        self.ser.write(txt + '\r') #20111-0202 '\r\n')
        if RS232_DELAY:
            time.sleep(rs232_delay)
        if not SIMUL_controller:
            ans = self.read()
        else:
            ans = 'simul'
        if DEBUG:
            print 'wrote:', txt
            print 'ans:', ans #self.ser.readline()
        if LOG:
            flog.write('wrote: ' + str(txt) + '\n')
        return ans

    def serWrite_noRead(self, cmd, data):
        txt = 'A' + dev + cmd + data
        self.ser.write(txt + '\r') #20111-0202 '\r\n')
        
    def write(self, cmd):
        self.ser.write(cmd + '\r') #20111-0202 '\r\n')
        if RS232_DELAY:
            time.sleep(rs232_delay)
        # lascio che la lettura del buffer di uscita del micro sia fatta da serWrite

class simula_seriale(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        os.system('sudo socat -d -d PTY,link=/dev/ttyS10,user=marco PTY,link=/dev/ttyS11,user=marco')        

    def stop(self):
        threadPID = os.getpid()
        # http://bytes.com/topic/python/answers/730784-how-get-stdout-script-os-system-executes
        serPID = commands.getoutput('pstree -p ' + str(threadPID) + '| grep socat')
        serPID = serPID.split('(')
        serPID = serPID[-1]
        serPID = serPID[0:len(serPID) - 1]
        '''active_queues.remove(self.mailbox)
        self.mailbox.put('exitThread')
        self.join()'''
        return(serPID)

if __name__ == "__main__":
    interfacce = {} # provo un dizionario per le interfacce agli strumenti
    interfacce['lockin'] = None
    
    try:
        ### change working directory
        ''' store in a different directory because of dropbox, copy in the dropboxed dir after each measurement '''
        os.chdir('/home/marco/Terahertz/')
        lista = ['GRAFfname', 'GRAFstop', 'GRAFupdate', 'instrum_initialized', 'MISon', 'stop_on_point', 'dl_cycle_stop']
        lista += ['/home/marco/hp5529a/EXIT_win', '/home/marco/hp5529a/START_win', '/home/marco/hp5529a/STARTED_win', '/home/marco/hp5529a/STOP_win', '/home/marco/hp5529a/FNAME_win']
        for elem in lista:
            if os.path.isfile(elem):
                os.remove(elem)
        
        if SIMUL_controller:
            if DEBUG:
                print 'in MAIN: controllo simulato'
            if LOG:
                flog.write('in MAIN: controllo simulato\n')
            thr_seriale = simula_seriale()
            thr_seriale.start()
            time.sleep(0.5)
        else:
            s = seriale('short', 'FTUSMK0', 9600, 0.1, 8, 'N', 1, 0, 0, False) # delay line
            ### 2014-01-14 s = seriale('FTUSMK0')
        
        ### 2014-03-26        
        # termometro davide
        '''ser_temp = seriale('short', '13009026', 38400, 0.1, 8, 'N', 1, 1, 0, False) # termometro Davide
        ser_temp.write('K0')
        ss = ser_temp.read_CR() #ser_temp.read()#2)
        print 'k0', ss
        ser_temp.write('WA0')
        ss = ser_temp.read_CR() #2)
        print 'wa0', ss'''
        
        # interferometro
        ### 2014-05-20 ser_inter = seriale('short', '', 9600, 0.1, 8, 'N', 1, 0, 0, True) # interfaccia all'interferometro

        dl = DL()#s)

        #dl.callMeFirst() # inizializzazione del controller

        dl.mainloop()
    except KeyboardInterrupt:
        pass # executes the 'finally' clause
    finally:
        if not SIMUL_controller:
            if INTERFEROMETER:
                open('/home/marco/hp5529a/EXIT_win', 'w').close()
            
            ans = s.serWrite('mf', '')
            chk = dev + ':mf'
            
            if ans == dev + ':mf':
                print 'motor switched off'
            else:
                print '!!! WARNING !!!\nmotor could be ON !!!'
                
            ### 2014-01-14 s.ser.close()
            s.close()
            ### 2014-03-26 ser_temp.close()
            ### 2014-05-20 ser_inter.close()
            
        else:
            p = thr_seriale.stop()
            os.system('kill ' + p)
            print 'simulated motor switched off'

        for elem in lista:
            if os.path.isfile(elem):
                os.remove(elem)
        
        if options.log:
            flog.close()        

        # ...just to be safe...
        subprocess.call(MV_MEAS, shell = True)
        
        os.chdir(SCRIPT_DIR) # restore original directory changed in CallMeFirst