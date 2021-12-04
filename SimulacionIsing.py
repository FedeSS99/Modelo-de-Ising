from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import numpy as np
from time import perf_counter

from CalculosIsing import EvolucionIsingCy

#Declaramos las constantes que definen el sistema así como las temperaturas
#a someter al sistema de atomos
N = 200
T = 0.01
Tmax = 3.01
Pasos = 2000
dT = (Tmax-T)/Pasos

iterMin, iterMax = -2, 2

#Creamos el arreglo cuadrado de configuracion de spines asi como el calculo
#de su energía total inicial asi como su magnetizacion
Spines = np.random.choice([-1,1], size=(N,N)).astype(np.float64)
SpinsPromedios = [Spines.mean()]
Temperaturas = [T]

#Creamos la ventana del widget GraphicsView
pg.setConfigOption('background', "k")
pg.setConfigOption('foreground', "w")
ventana = pg.GraphicsLayoutWidget(size=(1200,700))

ventana.setWindowTitle(f"Simulación de modelo de Ising, FPS=0, T={T:.2f}")
vista = ventana.addPlot(row=0, col=0, rowspan=2)
vista.hideAxis("bottom")
vista.hideAxis("left")
vista.setMouseEnabled( x=False, y=False)
vista.disableAutoRange()
vista.hideButtons()

PlotSpin = ventana.addPlot(row= 0, col=2, labels={"left":"Spin promedio", "bottom":"Iteración"})
PlotSpin.showGrid(y=True, alpha=0.5)
PlotSpin.setXRange(iterMin, iterMax)
PlotSpin.setYRange(-1.0, 1.0)

PlotSpin.setMouseEnabled( x=False, y=False)
PlotSpin.hideButtons()

PlotTemperatura = ventana.addPlot(row=1, col=2, labels={"left":"Temperatura (kT/J)", "bottom":"Iteración"})
PlotTemperatura.showGrid(y=True, alpha=0.5)
PlotTemperatura.setXRange(iterMin, iterMax)
PlotTemperatura.setYRange(0.0, Tmax)

PlotSpin.setMouseEnabled( x=False, y=False)
PlotSpin.hideButtons()

cm = pg.colormap.get(name="hsv", source="matplotlib")
pen = cm.getPen(span=(-2, 2), width=2)
bar =pg.ColorBarItem(values=(-2, 2), colorMap=cm)

#Fijamos el aspecto de la ventana para siempre visualizar
#celdas cuadradas
vista.setAspectLocked(True)

#Creamos el item del "material"
material = pg.ImageItem(border="k")
vista.addItem(material)

#Fijamos dimensiones visuales iniciales
vista.setRange(QtCore.QRectF(0,0, N, N))

#Fijamos el estado inicial
CurvaSpin = PlotSpin.plot(y=SpinsPromedios, pen=pen)
CurvaSpin.setClipToView(True)

CurvaTemperatura = PlotTemperatura.plot(y=Temperaturas, pen=pg.mkPen(color="r", width=2))
CurvaTemperatura.setClipToView(True)

material.setImage(Spines)
CurvaSpin.setData(SpinsPromedios)

bar.setImageItem(material)
ventana.addItem(bar, rowspan=2, col=1)

ventana.show()

iter = 1
TiempoActualizar = perf_counter()
transcurrido = 0.0

timer = QtCore.QTimer()
timer.setSingleShot(True)

def ActualizarSpines():
    global T, iter, transcurrido, TiempoActualizar, SpinsPromedios, iterMin, iterMax

    EvolucionIsingCy(Spines, T)
    bar.setImageItem(material)

    if iter<Pasos:
        T += dT
    elif iter>Pasos:
        T += -dT

    SpinsPromedios.append(Spines.mean())
    CurvaSpin.setData(SpinsPromedios)

    iterMin += 1
    iterMax += 1
    PlotSpin.setXRange(iterMin, iterMax)

    Temperaturas.append(T)
    CurvaTemperatura.setData(Temperaturas)
    PlotTemperatura.setXRange(iterMin, iterMax)

    timer.start()
    TiempoAct = perf_counter()
    TiempoTrans = TiempoAct - TiempoActualizar
    TiempoActualizar = TiempoAct
    transcurrido = transcurrido*0.9 + TiempoTrans*0.1
    ventana.setWindowTitle("Simulación de modelo de Ising, FPS={0:.2f}".format(1.0/transcurrido))
    iter += 1

    if iter==2*Pasos-1:
        PlotSpin.setXRange(0,2*Pasos)
        PlotTemperatura.setXRange(0,2*Pasos)
        timer.stop()

timer.timeout.connect(ActualizarSpines)
ActualizarSpines()

if __name__=="__main__":
    pg.exec()
