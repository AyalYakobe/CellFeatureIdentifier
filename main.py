from sys import path
from interface import render
from mesh import mesh_plotter
path.append('.\\Connection')




if __name__ == '__main__':
    render()
    mesh_plotter.plotter.app.exec_()


