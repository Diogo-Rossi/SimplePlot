# %%
# region: Imports

# Import System tools
import sys, os, pdb
def cls(): os.system("cls")
cls()

# Import matplotlib
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Import matplotlib and numpy
import matplotlib.pyplot as plt
from numpy import *

# Import Qt
from PyQt5 import  QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

# Import Ui
from Ui_Grafico import Ui_MainWindow

# Configure matplotlib's backend and pyplot's interactive mode
matplotlib.use("Qt5Agg")
plt.ion()

# endregion

# %%
# region: MainWindow class

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        
        # Initiate window in class 'QMainWindow'
        super().__init__()
        
        # Configure window layout in Ui_MainWindow
        self.setupUi(self)
        
        # Initiate figure, canvas, axe and lines
        self.fig = Figure(figsize=(100,100))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.subplots()
        self.lines = self.ax.plot([],[])
        
        # Set axis labels
        self.ax.set_xlabel("x axis")
        self.ax.set_ylabel("y axis")
        
        # Add Figure Canvas to PyQt Widget
        self.verticalLayout.addWidget(self.canvas)
        
        # Plot current equation
        self.on_lineEditEq_returnPressed()
        
        # Configure home axes limits
        self.on_pushButtonHome_clicked()
    
    # @QtCore.pyqtSlot()
    def on_lineEditEq_returnPressed(self):
        
        # Get data from edit boxes
        start = float(self.lineEditStart.text())
        stop = float(self.lineEditStop.text())
        num = int(self.lineEditNum.text())
        
        # Calculate data to plot the curve
        x = linspace(start, stop, num)
        y = eval(self.lineEditEq.text())
        
        # Set new data to the curve
        self.lines[-1].set_data(x,y)
        
        # Redraw figure canvas
        self.canvas.draw()        
    
    # @QtCore.pyqtSlot()
    def on_lineEditStart_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    # @QtCore.pyqtSlot()
    def on_lineEditStop_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    # @QtCore.pyqtSlot()
    def on_lineEditNum_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    # @QtCore.pyqtSlot()
    def on_lineEditXinf_returnPressed(self):
        self.set_limits()
    
    # @QtCore.pyqtSlot()
    def on_lineEditXsup_returnPressed(self):
        self.set_limits()
    
    # @QtCore.pyqtSlot()
    def on_lineEditYinf_returnPressed(self):
        self.set_limits()
    
    # @QtCore.pyqtSlot()
    def on_lineEditYsup_returnPressed(self):
        self.set_limits()
    
    def set_limits(self):
        
        # Get values from edit boxes
        xinf = float(self.lineEditXinf.text())
        xsup = float(self.lineEditXsup.text())
        yinf = float(self.lineEditYinf.text())
        ysup = float(self.lineEditYsup.text())
        
        # Set axes limits
        self.ax.set_xlim(xinf,xsup)
        self.ax.set_ylim(yinf,ysup)
        
        # Redraw figure canvas
        self.canvas.draw()
    
    # @QtCore.pyqtSlot()
    def on_pushButtonHome_clicked(self):
        
        # Reset auto-scale
        self.ax.set_autoscale_on(True)
        
        # Recompute data limits
        self.ax.relim()
        
        # Automatic axis scaling
        self.ax.autoscale_view()
        
        # Redraw figure canvas
        self.canvas.draw()
        
        # Get axes limits and put on lineEdits
        self.lineEditXinf.setText("{:0.2f}".format(self.ax.get_xlim()[0]))
        self.lineEditXsup.setText("{:0.2f}".format(self.ax.get_xlim()[1]))
        self.lineEditYinf.setText("{:0.2f}".format(self.ax.get_ylim()[0]))
        self.lineEditYsup.setText("{:0.2f}".format(self.ax.get_ylim()[1]))
    
    @QtCore.pyqtSlot()
    def on_pushButtonAddPlot_clicked(self):
        
        # Creat a new line plot and unpack the list to temp variable
        temp_line, = self.ax.plot([],[])
        
        # Add a new line plot to lines list
        self.lines.append(temp_line)
        
        # Set focus on edit box of equation
        self.lineEditEq.setText("")
        self.lineEditEq.setFocus()
    
    @QtCore.pyqtSlot()
    def on_pushButtonDelPlot_clicked(self):
        
        if len(self.lines)>1:
            
            # Remove last line
            self.ax.lines.pop()
            self.lines.pop()
            
            # Redraw figure canvas
            self.canvas.draw()



# endregion

# %%
# region: Main Program

app = QApplication([])
janela = MainWindow()
janela.show()
sys.exit(app.exec_())

# endregion