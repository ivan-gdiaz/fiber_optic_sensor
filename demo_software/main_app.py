'''
Created by patex1987, Jaromir
'''

import heatmap_gui_builder
import tkinter as tk
from tkinter import messagebox
import queue
import threading
import random
import time
import matplotlib.animation as animation
import numpy as np
import serial
import logging



class Sensor(object):
    '''
    A class to retrieve sensr data in a background Thread
    '''
    def __init__(self, gui, interval=1):
        '''
        interval - update interval in seconds
        '''
        self._interval = interval
        self._act_val = (None, None)
        self._thread_run_flag = False
        self._background_activity = None
        self._gui = gui

    
    def start_data_retr(self):
        '''
        Starts the background thread
        '''
        if self._background_activity is None:
            self._thread_run_flag = True
            self._background_activity = threading.Thread(target=self._background_retrieval,
                                                         name='sensor_retrieval',
                                                         daemon=True)
            self._background_activity.start()    
        if self._background_activity.is_alive():
            return

    def stop_data_retr(self):
        '''
        Stops the background Thread
        '''
        self._flag_stop_data_retr()
        if self._background_activity.is_alive():
            print('CLOSING THREAD')
            SENSOR._background_activity.join()
        self._background_activity = None
        
            
    def _flag_stop_data_retr(self):
        '''
        Flags the background thread to stop
        '''
        if self._background_activity is None:
            return
        if not self._background_activity.is_alive():
            return
        self._thread_run_flag = False

    @property
    def actual_value(self):
        '''Property for getting the actual value
        '''
        return self._act_val

    def _background_retrieval(self):
        '''
        This method will retrieve the data in the background
        '''
        while self._thread_run_flag:
            with serial.Serial(COM_PORT_NR, 38400, timeout=TIMEOUT_MS/1000, parity=serial.PARITY_EVEN, rtscts=1) as ser:
                ser.write(b'gv\n')
                raw_string = str(ser.readline(TIMEOUT_MS))
                self._act_val = tuple([int(x) for x in raw_string[6:-3].split(',')])
            self._gui.change_data(self._act_val[0], self._act_val[1])
            LOGGER.info('{0}, {1}'.format(self._act_val[0], self._act_val[1]))
            time.sleep(self._interval)
            



def start_retrieval(event, sensor, gui):
    '''
    Starts retrieval from the background
    Updates the heatmap
    '''
    if gui.start_button['state'] == 'disabled':
        return
    SENSOR.start_data_retr()
    gui.start_state()
    print('HERE')

def stop_retrieval(event, sensor, gui):
    '''
    Stops background retrieval
    '''
    if gui.stop_button['state'] == 'disabled':
        return
    SENSOR.stop_data_retr()
    gui.stop_state()


def get_logger(log_file='sensor.txt'):
    '''
    Returns a configured logger object
    '''
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(log_file)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return logger    
    
    
if __name__ == '__main__':
    LOGGER = get_logger(log_file='sensor.txt')
    REFRESH_RATE_MS = 250
    TIMEOUT_MS = 250
    COM_PORT_NR = '/dev/ttyACM1'
    ROOT = tk.Tk()
    GUI = heatmap_gui_builder.HeatmapGui(ROOT)
    SENSOR = Sensor(GUI, REFRESH_RATE_MS / 1000)
    ROOT.resizable(width=False, height=False)
    
    GUI.start_button.bind('<Button-1>',
                          lambda event, sensor=SENSOR, gui=GUI: start_retrieval(event, SENSOR, GUI))
    GUI.stop_button.bind('<Button-1>',
                         lambda event, sensor=SENSOR, gui=GUI: stop_retrieval(event, SENSOR, GUI))
    
    ROOT.mainloop()
