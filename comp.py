import vtk

dir_= r"CT"


#Step 1 read dataset
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()


# dataset info in output.txt


file1= open("output.txt","w")
dim=str(reader.GetOutput().GetDimensions())
file1.write("dimension"+"".join(dim))

pixel= str(reader.GetOutput().GetScalarRange())
file1.write("\npixel intensity"+"".join(pixel))

vtkImageData= str(reader.GetOutput())
file1.write("\nvtkImageData"+"".join(vtkImageData))

file1.close()

#Step 2 Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-1024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.5 ,0.2, 0.1)
colorFunc.AddRGBPoint(100, 0.9, 0.6 ,0.3)
colorFunc.AddRGBPoint(180, 1.0 ,0.8, 0.9)
colorFunc.AddRGBPoint(260, 0.6, 0.1 ,0.0)
colorFunc.AddRGBPoint(3071, 0.7, 0.8, 1.0)

# Step 3  Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(179, 0.1)
alphaChannelFunc.AddPoint(280, 0.4)
alphaChannelFunc.AddPoint(3071, 0.7)

# Instantiate necessary classes and create VTK pipeline

rw = vtk.vtkRenderWindow()
rw.SetSize(800,800)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(rw)

fv = [0.0, 0.0, 0.33, 0.99]
sv= [0.33, 0.0, 0.66, 0.99]
tv = [0.66, 0.0, 0.99, 0.99]
# step 4 && step 7

fr = vtk.vtkRenderer()

rw.AddRenderer(fr)
fr.SetViewport(fv)
#fr.SetBackground(.6, .5, .4)



sr= vtk.vtkRenderer()
rw.AddRenderer(sr)
sr.SetViewport(sv)
#sr.SetBackground(.0, .0, .0)
sr.SetActiveCamera(fr.GetActiveCamera())


tr = vtk.vtkRenderer()
rw.AddRenderer(tr)
tr.SetViewport(tv)
#tr.SetBackground(.7, .6, .4)
tr.SetActiveCamera(fr.GetActiveCamera())
## step 5
# define volume
volume1 = vtk.vtkVolume()
# Define volume mapper

volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume1.SetMapper(volumeMapper)
volume1.SetProperty(volumeProperty)  

# step 6

iso = vtk.vtkMarchingCubes()
iso.SetInputConnection(reader.GetOutputPort())
iso.ComputeGradientsOn()
iso.ComputeScalarsOff()
iso.SetValue(0, 270)

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(iso.GetOutputPort())
isoMapper.ScalarVisibilityOff()

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(1.,1.,1.)



# Add the volume to the renderer



fr.AddVolume(volume1)

sr.AddActor(isoActor)


tr.AddVolume(volume1)
tr.AddActor(isoActor)


fr.ResetCamera()



iren.Initialize()
rw.Render()
       

iren.Start()        