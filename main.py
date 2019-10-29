#!/usr/bin/env python

import glob
import os
import shutil
import json
import vtk
from stl2gltf import stl_to_gltf

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

    if filetype == "glb":
      writer = vtk.vtkSTLWriter()
      writer.SetInputConnection(cleaned.GetOutputPort())
      writer.SetFileTypeToBinary()
      writer.SetFileName(output_name)
      writer.Write()


infiletype = config["infiletype"]
outfiletype = config["outfiletype"]
for file in glob.glob(config["surfdir"] + '/*'+infiletype):
    print(file)
    base_name = os.path.basename(file)[:-3]
    if outfiletype == "glb":
        output_name = base_name + 'stl'
        glb_name = base_name + 'glb'
        decimate_mesh(file, 'surfaces/'+output_name, config['reduction'], outfiletype)
        stl_to_gltf('surfaces/'+output_name, 'surfaces/'+glb_name, True)
        os.remove('surfaces/'+output_name)
    else:
        output_name = output_name + outfiletype
        decimate_mesh(file, 'surfaces/'+output_name, config['reduction'], outfiletype)
    
        
