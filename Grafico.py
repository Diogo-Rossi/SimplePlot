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
from matplotlib.widgets import RectangleSelector, SpanSelector

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
        
        # Initiate figure, canvas and axes
        self.fig = Figure(figsize=(100,100))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.subplots()
        
        # Connect event with string *button_press_event* to *on_mouse_press* function
        # https://matplotlib.org/api/backend_bases_api.html?highlight=mpl_connect#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        self.canvas.mpl_connect('button_press_event',self.on_mouse_press)
        
        # Create 'RectangleSelector' object to be activated when press on Zoom Rect Buttom
        # REMARK: This functions creates a set of polylines in the axes
        # https://matplotlib.org/api/widgets_api.html?highlight=rectangleselector#matplotlib.widgets.RectangleSelector
        self.RS = RectangleSelector(self.ax,self.on_select_zoom_box,useblit=True)
        self.RS.set_active(False) # deactivate the selector
        
        # Create 'SpanSelector' object in vertical and horizontal directions, to be activated with zoom vert and hor
        # https://matplotlib.org/api/widgets_api.html?highlight=spanselector#matplotlib.widgets.SpanSelector
        self.SSv = SpanSelector(self.ax,self.on_vert_zoom,'vertical',useblit=True)
        self.SSh = SpanSelector(self.ax,self.on_hor_zoom,'horizontal',useblit=True)
        self.SSv.set_active(False)
        self.SSh.set_active(False)
        
        # Add Figure Canvas to PyQt Widget
        # REMARK: It is HERE where the matplotlib canvas is conected to PyQt layout (lacking of official documentation)
        # https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtwidgets/qboxlayout.html?highlight=addwidget 
        self.verticalLayout.addWidget(self.canvas)
        
        # Add a empty line to end of axis's line list (RectangleSelector already created some)
        self.ax.plot([],[])
        self.lines = 1 # Number of real plot lines
        
        # Set axis labels
        self.ax.set_xlabel("x axis")
        self.ax.set_ylabel("y axis")
        
        # Plot current equation (method already conected to signal 'returnPressed' of 'lineEditEq', defined bellow)
        self.on_lineEditEq_returnPressed()
        
        # Configure home axes limits (method already conected to signal 'clicked' of 'pushButtonHome', defined bellow)
        self.on_pushButtonHome_clicked()
    
    # Function to be called when clicking on canvas
    def on_mouse_press(self, event: matplotlib.backend_bases.MouseEvent):
        """ Function that is called when click with mouse on FIGURE CANVAS (not only inside axes)
            This Functions only prints information on the terminal
        
        Arguments:
            event {matplotlib.backend_bases.MouseEvent} -- 
            
            For the location events (button and key press/release), if the mouse is over the axes, 
            the inaxes attribute of the event will be set to the Axes the event occurs is over, and additionally, 
            the variables xdata and ydata attributes will be set to the mouse location in data coordinates. 
            See KeyEvent and MouseEvent for more info.
            https://matplotlib.org/api/backend_bases_api.html?highlight=mpl_connect#matplotlib.backend_bases.KeyEvent
            https://matplotlib.org/api/backend_bases_api.html?highlight=mpl_connect#matplotlib.backend_bases.MouseEvent
        
        """
        # Clears terminal
        cls()
        
        # If the mouse is over an axes
        if event.inaxes:
            
            # Print polylines ploted in axes
            print("Polylines objects: =================")
            for line in event.inaxes.lines:
                print(line)
            
            # Print coordinates to mouse position
            print("\nPosition :==============")
            print("x = ",event.xdata," | y = ",event.ydata)
        else:
            # If the mouse is not over an axes
            print("Clicked out of axes")
    
    # Function to be called by 'RectangleSelector' object
    def on_select_zoom_box(self, eclick: matplotlib.backend_bases.MouseEvent, erelease: matplotlib.backend_bases.MouseEvent):
        """Function that is called by "RectangleSelector" object from "matplotlib.widgets"

        Arguments:
            eclick {matplotlib.backend_bases.MouseEvent} -- matplotlib event at press mouse button
            erelease {matplotlib.backend_bases.MouseEvent} -- matplotlib event at release mouse button
            https://matplotlib.org/api/backend_bases_api.html?highlight=matplotlib%20backend_bases%20mouseevent#matplotlib.backend_bases.MouseEvent
        """                
        self.ax.set_xlim(eclick.xdata, erelease.xdata)
        self.ax.set_ylim(eclick.ydata, erelease.ydata)
        self.get_limits()
        self.canvas.draw()
        self.RS.set_active(False)
    
    # Functions to be called when "zoom" vertical and horizontal directions
    def on_vert_zoom(self,vmin:float,vmax:float):
        """Function to zoom only in vertical direction that is called by de SpanSelector object with direction="vertical"
        
        Arguments:
            vmin {float} -- min range value
            vmax {float} -- max range value
        """   
        self.ax.set_ylim(vmin, vmax)
        self.get_limits()
        self.SSv.set_active(False)
    def on_hor_zoom(self,hmin:float,hmax:float):
        """Function to zoom only in horizontal direction that is called by de SpanSelector object with direction="horizontal"
        
        Arguments:
            hmin {float} -- min range value
            hmax {float} -- max range value
        """   
        self.ax.set_xlim(hmin, hmax)
        self.get_limits()
        self.SSh.set_active(False)
    
    # Get values from lineEdits and set axes limits to they
    def set_limits(self):
        
        """Function to get values from 'lineEdits' boxes and set limits of axes"""
        
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
        
        self.get_limits()
    
    # Get axes limits and put on lineEdits
    def get_limits(self):
        
        """Function to get the actual limits of axes and put it on 'lineEdits' """
        
        self.lineEditXinf.setText("{:0.2f}".format(self.ax.get_xlim()[0]))
        self.lineEditXsup.setText("{:0.2f}".format(self.ax.get_xlim()[1]))
        self.lineEditYinf.setText("{:0.2f}".format(self.ax.get_ylim()[0]))
        self.lineEditYsup.setText("{:0.2f}".format(self.ax.get_ylim()[1]))
    
    @QtCore.pyqtSlot()
    def on_lineEditEq_returnPressed(self):
        
        # Get data from edit boxes
        start = float(self.lineEditStart.text())
        stop = float(self.lineEditStop.text())
        num = int(self.lineEditNum.text())
        
        # Calculate data to plot the curve
        x = linspace(start, stop, num)
        y = eval(self.lineEditEq.text())
        
        # Set new data to the curve
        self.ax.lines[-1].set_data(x,y)
        
        # Redraw figure canvas
        self.canvas.draw()        
    
    @QtCore.pyqtSlot()
    def on_lineEditStart_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    @QtCore.pyqtSlot()
    def on_lineEditStop_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    @QtCore.pyqtSlot()
    def on_lineEditNum_returnPressed(self):
        self.on_lineEditEq_returnPressed()
    
    @QtCore.pyqtSlot()
    def on_lineEditXinf_returnPressed(self):
        self.set_limits()
    
    @QtCore.pyqtSlot()
    def on_lineEditXsup_returnPressed(self):
        self.set_limits()
    
    @QtCore.pyqtSlot()
    def on_lineEditYinf_returnPressed(self):
        self.set_limits()
    
    @QtCore.pyqtSlot()
    def on_lineEditYsup_returnPressed(self):
        self.set_limits()
    
    @QtCore.pyqtSlot()
    def on_pushButtonHome_clicked(self):
        
        # Reset auto-scale
        self.ax.set_autoscale_on(True)
        
        # Recompute data limits
        self.ax.relim()
        
        # Automatic axis scaling
        self.ax.autoscale_view()
        
        # Redraw figure canvas
        self.canvas.draw()
        
        self.get_limits()
    
    @QtCore.pyqtSlot()
    def on_pushButtonAddPlot_clicked(self):
        
        if len(self.ax.lines[-1].get_xdata()) > 0:
            # Add a new line plot to lines list, if the last wasn't empty
            self.ax.plot([],[])
            self.lines += 1
        
        # Set focus on edit box of equation
        self.lineEditEq.setText("")
        self.lineEditEq.setFocus()
    
    @QtCore.pyqtSlot()
    def on_pushButtonDelPlot_clicked(self):
        
        if self.lines>0:
            
            # Remove last line
            self.ax.lines.pop()
            
            # Redraw figure canvas
            self.canvas.draw()
            
            # Decrease number of curves
            self.lines -= 1
    
    @QtCore.pyqtSlot()
    def on_pushButtonRect_clicked(self):
        self.RS.set_active(True)
    
    @QtCore.pyqtSlot()
    def on_pushButtonHor_clicked(self):
        self.SSh.set_active(True)
    
    @QtCore.pyqtSlot()
    def on_pushButtonVert_clicked(self):
        self.SSv.set_active(True)


# endregion

# %%
# region: Main Program

print("*** PROGRAM TO PLOT SIMPLE GRAPH WITH MATPLOTLIB AND PYQT ***")
print("")
print("matplotlib is embeded in PyQt with Figure's canvas in widget")

app = QApplication([])
janela = MainWindow()
janela.show() # 
# janela.showMaximized()
# janela.move(600,300)
# janela.resize(750,500)
sys.exit(app.exec_())

# endregion