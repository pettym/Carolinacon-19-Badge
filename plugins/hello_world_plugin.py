#!/usr/bin/env python3

""" Targeting Kicad 6.0 """

import pcbnew

import matplotlib.pyplot as plt

from math import sin, cos, dist, tau
from numpy import pi, linspace, arange
from scipy.signal import decimate, lfilter, iirfilter, butter, freqz


def point(x, y, scale=None):
    _class = pcbnew.wxPointMils    
    x, y = int(x), int(y)    
    return _class(x,y)


##def lowpass_filter(data, order=8, critical_freq=0.1):
def lowpass_filter(data, order=8, critical_freq=0.007):
    b, a = iirfilter(order, critical_freq, analog=False, btype='lowpass')
    return lfilter(b, a, data)

def calc_spiral_point(t, mult=1):
    x = (mult * t) * cos(t)
    y = (mult * t) * sin(t)
    return (x,y)


def spiral(iterator, mult=1, filter_data=False, decimation=0, minimum_step=0):
    data = [ calc_spiral_point(i, mult) for i in iterator ]

    if filter_data or decimation:
        x, y = zip(*data)
        
        if filter_data:   x, y = lowpass_filter(x), lowpass_filter(y)
        if decimation: x, y = decimate(x, int(decimation)), decimate(y, int(decimation))

        data = list(zip(x,y))

    if minimum_step:
        output = [ data[0] ]
        points = zip(data[:-1], data[1:])
        for start, stop in points:
            if dist(output[-1], stop) > minimum_step:
                output.append(stop)
        data = output
    
    start_points, stop_points = data[:-1], data[1:]
    return list(zip(start_points, stop_points))
        
    


class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "hello world plugin"
        self.category = "testing"
        self.description = "testing plugins"
        self.show_toolbar_button = False
##        self.icon_file_name = 

    @staticmethod
    def draw(track, board):
        track.SetLayer(pcbnew.F_Cu)
        track.SetStart(pcbnew.wxPoint(0, 0))
        track.SetEnd(pcbnew.wxPoint( int(5e6), int(5e6) ))
        track.SetWidth( int(2e5) )
        board.Add(track)

    @staticmethod
    def make_track(start_point, stop_point, width_mm=0.25):
        board = pcbnew.GetBoard()
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(start_point)
        track.SetEnd(stop_point)
        track.SetWidth( int(width_mm * 10 ** 6) )
        board.Add(track)


    #graph_space = arange(0, 20, 0.01)
    graph_space = linspace(0, 4*tau, 200) 
    mult = 3

    filter_data = False
    decimation = 4
    minimum_step = 6
    

    def Run(self):
        print("Running")
        board = pcbnew.GetBoard()

        graph_space = self.graph_space
        mult = self.mult

        points_in_spiral = spiral(graph_space,
                                  mult = mult,
                                  filter_data = self.filter_data,
                                  decimation = self.decimation,
                                  minimum_step = self.minimum_step,
                                  )
        print(f'{len(points_in_spiral)=}')
        
        turns = 0
        for start, stop in points_in_spiral:
            
            self.make_track(point(*start), point(*stop), width_mm=0.2)

            start_x, stop_x = start[0], stop[0]
            if start_x < 0 and stop_x > 0:
                turns += 1
        print(f'{turns=}')

                       

SimplePlugin().register()


if __name__ == '__main__':

    board = pcbnew.GetBoard()
    track = pcbnew.PCB_TRACK(board)

    data = [ calc_spiral_point(i) for i in SimplePlugin.graph_space ]
    x,y = zip(*data)

    x = list(range(1000))
    y = [ int(i>500) for i in x ]

    y = lowpass_filter(y)

    plt.plot(x,y)
    plt.show()

##    for start, stop in spiral(SimplePlugin.graph_space, mult=2):
##        print(f'{start=}\t{stop=}')











