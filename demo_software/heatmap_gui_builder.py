'''
Created by patex1987, Jaromir
'''
import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np
import pandas as pd



class HeatmapGui(object):
    '''
    Tkinter GUI with embedded matplotlib heatmap for sensor data visualization
    '''
    def __init__(self, master):
        '''
        GUI initialization, positioning of widgets
        '''
        master.wm_title('Sensor demonstration')
        self.master = master
        
        #self._def_dataset = np.zeros((1,2))
        self._def_dataset = np.full((1,5), 4000.0)

        self.dataset = self._def_dataset.copy()
        
        #row 0
        self.start_button = tk.Button(master, text='Start')
        self.start_button.grid(row=0, column=0, sticky='ew')
        self.stop_button = tk.Button(master, text='Stop', state='disabled')
        self.stop_button.grid(row=0, column=1, sticky='ew')
        
        #row 1
        self.heat_figure = Figure(figsize=(5, 2))
        self.ax = self.heat_figure.add_subplot(1, 1, 1)
        self.heat_canvas = FigureCanvasTkAgg(self.heat_figure, master=master)
        self.heat_canvas.show()
        self.heat_canvas.get_tk_widget().grid(row=1,column=0, sticky='ew', columnspan=2)

        self.heat_plot = self.ax.imshow(self.dataset, animated=True, cmap='autumn',vmin=2000, vmax=4000)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.tick_params(left='off', bottom='off')
        self.heat_animation = animation.FuncAnimation(self.heat_figure, self._animate, init_func=self._heat_init,
                                                      interval=1000)
                                                      
        self.sensor1_val = tk.Label(master, text='')
        self.sensor1_val.grid(row=2, column=0, sticky='ew')
        self.sensor2_val = tk.Label(master, text='')
        self.sensor2_val.grid(row=2, column=1, sticky='ew')
    
    #def initialize_heat(self, sensor_data):
    #    if sensor_data = is None
    def change_data(self, first_val, last_val):
        print(self.dataset)
        self.dataset[0,0] = first_val
        self.dataset[0,-1] = last_val
        self.sensor1_val.config(text=first_val)
        self.sensor2_val.config(text=last_val)
        


    def _heat_init(self):
        self.dataset = self._def_dataset.copy()
        self.heat_plot.set_data(self.dataset)

    def _animate(self, i):
        self.heat_plot.set_data(self.dataset)
        return self.heat_plot,

                                                      
        
    def start_state(self):
        '''
        Disables start button, enables stop button
        '''
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
                                                      
                                                      

    def stop_state(self):
        '''
        Disables start button, enables stop button
        '''
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.sensor1_val.config(text='')
        self.sensor2_val.config(text='')
     


     
     
     
if __name__ == '__main__':

    ROOT = tk.Tk()
    GUI = HeatmapGui(ROOT)
    ROOT.resizable(width=False, height=False)
    ROOT.mainloop()
    
