from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import numpy as np
from time import perf_counter

from IsingRutinas import EvolucionIsingCy

#Declaramos las constantes que definen el sistema así como las temperaturas
#a someter al sistema de atomos
Nx, Ny = 600, 300
T = 0.1

#Creamos el arreglo cuadrado de configuracion de spines asi como el calculo
#de su energía total inicial asi como su magnetizacion
Spines = np.random.choice([-1,1], size=(Nx,Ny)).astype(np.float64)

#Creamos la ventana del widget GraphicsView
pg.setConfigOption('background', "k")
pg.setConfigOption('foreground', "w")
ventana = pg.GraphicsLayoutWidget(size=(1300,700))

FPS=0
ventana.setWindowTitle(f"Simulación de modelo de Ising, {FPS=}, {T=:.2f}")
vista = ventana.addPlot(row=0, col=0, rowspan=2)
vista.hideAxis("bottom")
vista.hideAxis("left")

cm = pg.colormap.get(name="hsv", source="matplotlib")
bar =pg.ColorBarItem(values=(-2, 2), colorMap=cm)

#Fijamos el aspecto de la ventana para siempre visualizar
#celdas cuadradas
vista.setAspectLocked(True)

#Creamos el item del "material"
material = pg.ImageItem(border="k")
vista.addItem(material)

#Fijamos dimensiones visuales iniciales
vista.setRange(QtCore.QRectF(0,0, Nx, Ny))

#Fijamos el estado inicial
material.setImage(Spines)

bar.setImageItem(material)
ventana.addItem(bar)

ventana.show()

iter = 1
TiempoActualizar = perf_counter()
transcurrido = 0.0

timer = QtCore.QTimer()
timer.setSingleShot(True)

def ActualizarSpines():
    global T, Spines, iter, transcurrido, TiempoActualizar

    SpinesCopia = np.copy(Spines)
    EvolucionIsingCy(Spines, SpinesCopia, T)
    bar.setImageItem(material)

    timer.start()
    TiempoAct = perf_counter()
    TiempoTrans = TiempoAct - TiempoActualizar
    TiempoActualizar = TiempoAct
    transcurrido = transcurrido*0.9 + TiempoTrans*0.1
    FPS = int(1.0/transcurrido)
    ventana.setWindowTitle(f"Simulación de modelo de Ising, {FPS=}, {T=:.2f}")
    iter += 1


timer.timeout.connect(ActualizarSpines)
ActualizarSpines()

if __name__=="__main__":
    pg.exec()
