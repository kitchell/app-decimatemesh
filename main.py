#!/usr/bin/env python

import glob
import os
import shutil
import json
import vtk

with open('config.json') as config_json:
    config = json.load(config_json)

pwd = os.getcwd()
os.mkdir(pwd + "/surfaces")
#os.chdir(pwd + "/surfaces")
try:
    shutil.copyfile(config["surfdir"]+"/color.json", pwd + "/surfaces/color.json")
except:
    print('no color.json file')


def decimate_mesh(file_name, output_name, reduction, filetype="vtk"):
   
    # Read the surface from file
    if file_name[-3:] == 'vtk':
        object = vtk.vtkPolyDataReader()
    if file_name[-3:] == 'ply':
        object = vtk.vtkPLYReader()
    if file_name[-3:] == 'stl':
        object = vtk.vtkSTLReader()
    object.SetFileName(file_name)
    
    deci = vtk.vtkDecimatePro()
    deci.SetInputConnection(object.GetOutputPort())
    deci.SetTargetReduction(reduction)
    deci.PreserveTopologyOn()
    deci.Update()

    cleaned = vtk.vtkCleanPolyData()
    cleaned.SetInputConnection(deci.GetOutputPort())
    cleaned.Update()

    if filetype == "stl":
      writer = vtk.vtkSTLWriter()
      writer.SetInputConnection(cleaned.GetOutputPort())
      writer.SetFileTypeToASCII()
      writer.SetFileName(output_name)
      writer.Write()
      
    if filetype == "ply":
      writer = vtk.vtkPLYWriter()
      writer.SetInputConnection(cleaned.GetOutputPort())
      writer.SetFileTypeToASCII()
      writer.SetFileName(output_name)
      writer.Write()
      
    if filetype == "vtk":
      writer = vtk.vtkPolyDataWriter()
      #writer = vtk.vtkDataSetWriter()
      writer.SetInputConnection(cleaned.GetOutputPort())
      writer.SetFileName(output_name)
      writer.Write()



filetype = config["filetype"]
for file in glob.glob(config["surfdir"] + '/*'+filetype):
    print(file)
    output_name = os.path.basename(file)[:-3]
    output_name = output_name + filetype
    decimate_mesh(file, 'surfaces/'+output_name, config['reduction'], filetype)
