#!/usr/bin/env python3

""" Targeting Kicad 6.0 """

import pcbnew

import matplotlib.pyplot as plt

from math import sin, cos, dist, tau
from numpy import pi, concatenate, linspace, arange
from scipy.signal import decimate, lfilter, iirfilter, butter, freqz


def point(x, y, scale=None):
    _class = pcbnew.wxPointMils    
    x, y = int(x), int(y)    
    return _class(x,y)


def calc_spiral_point(t, mult=1):
    x = (mult * t) * cos(t)
    y = (mult * t) * sin(t)
    return (x,y)


def spiral(iterator, mult=1, minimum_step=0, decimation=0):
    data = [ calc_spiral_point(i, mult) for i in iterator ]

    # TODO: Low Pass filter here?

##    if decimation:
##        x, y = zip(*data)
##        x, y = decimate([x,y], int(decimation), n=4, ftype='fir')
##        data = list(zip(x,y))

    if minimum_step:
        output = [ data[0] ]
        points = zip(data[:-1], data[1:])
        for start, stop in points:
            if dist(output[-1], stop) > minimum_step:
                output.append(stop)
        data = output

    if decimation:
        x, y = zip(*data)
        x, y = decimate([x,y], int(decimation), n=4, ftype='fir')
        data = list(zip(x,y))
    
    start_points, stop_points = data[:-1], data[1:]
    return list(zip(start_points, stop_points))
        
    


class NFCAntennaPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "NFC Antenna Plugin"
        self.category = "NFC Antenna Plugin"
        self.description = "NFC Antenna Plugin"
        self.show_toolbar_button = False

    @staticmethod
    def draw_track(start_point, stop_point, width_mm=0.25):
        board = pcbnew.GetBoard()
        track = pcbnew.PCB_TRACK(board)

        #track.SetLayer(pcbnew.F_Cu)
        
        track.SetStart(start_point)
        track.SetEnd(stop_point)
        track.SetWidth( int(width_mm * 10 ** 6) )
        board.Add(track)
    
    def generate_antenna(self, turn_count=7, mult=3, initial_turn=30, decimation=0, minimum_step=4, track_width=0.2):
       
        point_space =  linspace(
            initial_turn * tau,
            (initial_turn+turn_count)*tau,
            turn_count*2000
            )

        points_in_spiral = spiral(
            point_space,
            mult = mult,
            decimation = decimation,
            minimum_step = minimum_step,
        )
        
        print(f'{len(points_in_spiral)=}')
        
        for start, stop in points_in_spiral:            
            self.draw_track(point(*start), point(*stop), width_mm=track_width)


    def Run(self):
        self.generate_antenna(
            mult=3,
            decimation=2,
            minimum_step=12
            )
                       

NFCAntennaPlugin().register()


if __name__ == '__main__':

    board = pcbnew.GetBoard()
    track = pcbnew.PCB_TRACK(board)

    x = list(range(1000))
    y = [ int(i>500) for i in x ]

    x,y = decimate((x,y), q=2, n=4, ftype='fir')

    plt.plot(x,y)
    plt.show()

##    for start, stop in spiral(SimplePlugin.graph_space, mult=2):
##        print(f'{start=}\t{stop=}')











