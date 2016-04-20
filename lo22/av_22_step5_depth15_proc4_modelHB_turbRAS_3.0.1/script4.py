#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [800, 600]

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'OpenFOAMReader'
avfoam = OpenFOAMReader(FileName='av.foam')
avfoam.CaseType = 'Reconstructed Case'
avfoam.Createcelltopointfiltereddata = 1
avfoam.Adddimensionalunitstoarraynames = 0
avfoam.MeshRegions = ['internalMesh']
avfoam.CellArrays = ['U', 'alpha.water', 'epsilon', 'k', 'nu1', 'nuTilda', 'nut', 'p', 'p_rgh', 'region']
avfoam.PointArrays = []
avfoam.LagrangianArrays = []
avfoam.Cachemesh = 1
avfoam.Decomposepolyhedra = 1
avfoam.ListtimestepsaccordingtocontrolDict = 0
avfoam.LagrangianpositionsareinOF13binaryformat = 0
avfoam.Readzones = 0

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on avfoam
avfoam.MeshRegions = ['internalMesh', 'sides', 'slope', 'atmosphere']

# show data in view
avfoamDisplay = Show(avfoam, renderView1)
# trace defaults for the display properties.
avfoamDisplay.CubeAxesVisibility = 0
avfoamDisplay.Representation = 'Surface'
avfoamDisplay.AmbientColor = [1.0, 1.0, 1.0]
avfoamDisplay.ColorArrayName = [None, '']
avfoamDisplay.DiffuseColor = [1.0, 1.0, 1.0]
avfoamDisplay.LookupTable = None
avfoamDisplay.MapScalars = 1
avfoamDisplay.InterpolateScalarsBeforeMapping = 1
avfoamDisplay.Opacity = 1.0
avfoamDisplay.PointSize = 2.0
avfoamDisplay.LineWidth = 1.0
avfoamDisplay.Interpolation = 'Gouraud'
avfoamDisplay.Specular = 0.0
avfoamDisplay.SpecularColor = [1.0, 1.0, 1.0]
avfoamDisplay.SpecularPower = 100.0
avfoamDisplay.Ambient = 0.0
avfoamDisplay.Diffuse = 1.0
avfoamDisplay.EdgeColor = [0.0, 0.0, 0.5]
avfoamDisplay.BackfaceRepresentation = 'Follow Frontface'
avfoamDisplay.BackfaceAmbientColor = [1.0, 1.0, 1.0]
avfoamDisplay.BackfaceDiffuseColor = [1.0, 1.0, 1.0]
avfoamDisplay.BackfaceOpacity = 1.0
avfoamDisplay.Position = [0.0, 0.0, 0.0]
avfoamDisplay.Scale = [1.0, 1.0, 1.0]
avfoamDisplay.Orientation = [0.0, 0.0, 0.0]
avfoamDisplay.Origin = [0.0, 0.0, 0.0]
avfoamDisplay.Pickable = 1
avfoamDisplay.Texture = None
avfoamDisplay.Triangulate = 0
avfoamDisplay.NonlinearSubdivisionLevel = 1
avfoamDisplay.CubeAxesColor = [1.0, 1.0, 1.0]
avfoamDisplay.CubeAxesCornerOffset = 0.0
avfoamDisplay.CubeAxesFlyMode = 'Closest Triad'
avfoamDisplay.CubeAxesInertia = 1
avfoamDisplay.CubeAxesTickLocation = 'Inside'
avfoamDisplay.CubeAxesXAxisMinorTickVisibility = 1
avfoamDisplay.CubeAxesXAxisTickVisibility = 1
avfoamDisplay.CubeAxesXAxisVisibility = 1
avfoamDisplay.CubeAxesXGridLines = 0
avfoamDisplay.CubeAxesXTitle = 'X-Axis'
avfoamDisplay.CubeAxesUseDefaultXTitle = 1
avfoamDisplay.CubeAxesYAxisMinorTickVisibility = 1
avfoamDisplay.CubeAxesYAxisTickVisibility = 1
avfoamDisplay.CubeAxesYAxisVisibility = 1
avfoamDisplay.CubeAxesYGridLines = 0
avfoamDisplay.CubeAxesYTitle = 'Y-Axis'
avfoamDisplay.CubeAxesUseDefaultYTitle = 1
avfoamDisplay.CubeAxesZAxisMinorTickVisibility = 1
avfoamDisplay.CubeAxesZAxisTickVisibility = 1
avfoamDisplay.CubeAxesZAxisVisibility = 1
avfoamDisplay.CubeAxesZGridLines = 0
avfoamDisplay.CubeAxesZTitle = 'Z-Axis'
avfoamDisplay.CubeAxesUseDefaultZTitle = 1
avfoamDisplay.CubeAxesGridLineLocation = 'All Faces'
avfoamDisplay.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
avfoamDisplay.CustomBoundsActive = [0, 0, 0]
avfoamDisplay.OriginalBoundsRangeActive = [0, 0, 0]
avfoamDisplay.CustomRange = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
avfoamDisplay.CustomRangeActive = [0, 0, 0]
avfoamDisplay.UseAxesOrigin = 0
avfoamDisplay.AxesOrigin = [0.0, 0.0, 0.0]
avfoamDisplay.CubeAxesXLabelFormat = '%-#6.3g'
avfoamDisplay.CubeAxesYLabelFormat = '%-#6.3g'
avfoamDisplay.CubeAxesZLabelFormat = '%-#6.3g'
avfoamDisplay.StickyAxes = 0
avfoamDisplay.CenterStickyAxes = 0
avfoamDisplay.SelectionCellLabelBold = 0
avfoamDisplay.SelectionCellLabelColor = [0.0, 1.0, 0.0]
avfoamDisplay.SelectionCellLabelFontFamily = 'Arial'
avfoamDisplay.SelectionCellLabelFontSize = 18
avfoamDisplay.SelectionCellLabelItalic = 0
avfoamDisplay.SelectionCellLabelJustification = 'Left'
avfoamDisplay.SelectionCellLabelOpacity = 1.0
avfoamDisplay.SelectionCellLabelShadow = 0
avfoamDisplay.SelectionPointLabelBold = 0
avfoamDisplay.SelectionPointLabelColor = [1.0, 1.0, 0.0]
avfoamDisplay.SelectionPointLabelFontFamily = 'Arial'
avfoamDisplay.SelectionPointLabelFontSize = 18
avfoamDisplay.SelectionPointLabelItalic = 0
avfoamDisplay.SelectionPointLabelJustification = 'Left'
avfoamDisplay.SelectionPointLabelOpacity = 1.0
avfoamDisplay.SelectionPointLabelShadow = 0

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(avfoamDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
avfoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.LockDataRange = 0
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.ShowCategoricalColorsinDataRangeOnly = 0
vtkBlockColorsLUT.RescaleOnVisibilityChange = 0
vtkBlockColorsLUT.EnableOpacityMapping = 0
vtkBlockColorsLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 0.5, 0.865003, 0.865003, 0.865003, 1.0, 0.705882, 0.0156863, 0.14902]
vtkBlockColorsLUT.UseLogScale = 0
vtkBlockColorsLUT.ColorSpace = 'Diverging'
vtkBlockColorsLUT.UseBelowRangeColor = 0
vtkBlockColorsLUT.BelowRangeColor = [0.0, 0.0, 0.0]
vtkBlockColorsLUT.UseAboveRangeColor = 0
vtkBlockColorsLUT.AboveRangeColor = [1.0, 1.0, 1.0]
vtkBlockColorsLUT.NanColor = [1.0, 1.0, 0.0]
vtkBlockColorsLUT.Discretize = 1
vtkBlockColorsLUT.NumberOfTableValues = 256
vtkBlockColorsLUT.ScalarRangeInitialized = 0.0
vtkBlockColorsLUT.HSVWrap = 0
vtkBlockColorsLUT.VectorComponent = 0
vtkBlockColorsLUT.VectorMode = 'Magnitude'
vtkBlockColorsLUT.AllowDuplicateScalars = 1
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['0', '1', '2', '3']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')
vtkBlockColorsPWF.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
vtkBlockColorsPWF.AllowDuplicateScalars = 1
vtkBlockColorsPWF.ScalarRangeInitialized = 0

# hide color bar/color legend
avfoamDisplay.SetScalarBarVisibility(renderView1, False)

# turn off scalar coloring
ColorBy(avfoamDisplay, None)

# Properties modified on avfoamDisplay
avfoamDisplay.Opacity = 0.23

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XTitle = 'X'
renderView1.AxesGrid.YTitle = 'Y'
renderView1.AxesGrid.ZTitle = 'Z'
renderView1.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.GridColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

animationScene1.GoToNext()

# create a new 'Iso Volume'
isoVolume1 = IsoVolume(Input=avfoam)
isoVolume1.InputScalars = ['POINTS', 'p']
isoVolume1.ThresholdRange = [-11432.69921875, 31981.17578125]

# Properties modified on isoVolume1
isoVolume1.InputScalars = ['POINTS', 'alpha.water']
isoVolume1.ThresholdRange = [0.1, 1.0]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.LockDataRange = 0
pLUT.InterpretValuesAsCategories = 0
pLUT.ShowCategoricalColorsinDataRangeOnly = 0
pLUT.RescaleOnVisibilityChange = 0
pLUT.EnableOpacityMapping = 0
pLUT.RGBPoints = [-11432.69921875, 0.231373, 0.298039, 0.752941, 5565.8505859375, 0.865003, 0.865003, 0.865003, 22564.400390625, 0.705882, 0.0156863, 0.14902]
pLUT.UseLogScale = 0
pLUT.ColorSpace = 'Diverging'
pLUT.UseBelowRangeColor = 0
pLUT.BelowRangeColor = [0.0, 0.0, 0.0]
pLUT.UseAboveRangeColor = 0
pLUT.AboveRangeColor = [1.0, 1.0, 1.0]
pLUT.NanColor = [1.0, 1.0, 0.0]
pLUT.Discretize = 1
pLUT.NumberOfTableValues = 256
pLUT.ScalarRangeInitialized = 1.0
pLUT.HSVWrap = 0
pLUT.VectorComponent = 0
pLUT.VectorMode = 'Magnitude'
pLUT.AllowDuplicateScalars = 1
pLUT.Annotations = []
pLUT.ActiveAnnotatedValues = []
pLUT.IndexedColors = []

# show data in view
isoVolume1Display = Show(isoVolume1, renderView1)
# trace defaults for the display properties.
isoVolume1Display.CubeAxesVisibility = 0
isoVolume1Display.Representation = 'Surface'
isoVolume1Display.AmbientColor = [1.0, 1.0, 1.0]
isoVolume1Display.ColorArrayName = ['POINTS', 'p']
isoVolume1Display.DiffuseColor = [1.0, 1.0, 1.0]
isoVolume1Display.LookupTable = pLUT
isoVolume1Display.MapScalars = 1
isoVolume1Display.InterpolateScalarsBeforeMapping = 1
isoVolume1Display.Opacity = 1.0
isoVolume1Display.PointSize = 2.0
isoVolume1Display.LineWidth = 1.0
isoVolume1Display.Interpolation = 'Gouraud'
isoVolume1Display.Specular = 0.0
isoVolume1Display.SpecularColor = [1.0, 1.0, 1.0]
isoVolume1Display.SpecularPower = 100.0
isoVolume1Display.Ambient = 0.0
isoVolume1Display.Diffuse = 1.0
isoVolume1Display.EdgeColor = [0.0, 0.0, 0.5]
isoVolume1Display.BackfaceRepresentation = 'Follow Frontface'
isoVolume1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
isoVolume1Display.BackfaceDiffuseColor = [1.0, 1.0, 1.0]
isoVolume1Display.BackfaceOpacity = 1.0
isoVolume1Display.Position = [0.0, 0.0, 0.0]
isoVolume1Display.Scale = [1.0, 1.0, 1.0]
isoVolume1Display.Orientation = [0.0, 0.0, 0.0]
isoVolume1Display.Origin = [0.0, 0.0, 0.0]
isoVolume1Display.Pickable = 1
isoVolume1Display.Texture = None
isoVolume1Display.Triangulate = 0
isoVolume1Display.NonlinearSubdivisionLevel = 1
isoVolume1Display.CubeAxesColor = [1.0, 1.0, 1.0]
isoVolume1Display.CubeAxesCornerOffset = 0.0
isoVolume1Display.CubeAxesFlyMode = 'Closest Triad'
isoVolume1Display.CubeAxesInertia = 1
isoVolume1Display.CubeAxesTickLocation = 'Inside'
isoVolume1Display.CubeAxesXAxisMinorTickVisibility = 1
isoVolume1Display.CubeAxesXAxisTickVisibility = 1
isoVolume1Display.CubeAxesXAxisVisibility = 1
isoVolume1Display.CubeAxesXGridLines = 0
isoVolume1Display.CubeAxesXTitle = 'X-Axis'
isoVolume1Display.CubeAxesUseDefaultXTitle = 1
isoVolume1Display.CubeAxesYAxisMinorTickVisibility = 1
isoVolume1Display.CubeAxesYAxisTickVisibility = 1
isoVolume1Display.CubeAxesYAxisVisibility = 1
isoVolume1Display.CubeAxesYGridLines = 0
isoVolume1Display.CubeAxesYTitle = 'Y-Axis'
isoVolume1Display.CubeAxesUseDefaultYTitle = 1
isoVolume1Display.CubeAxesZAxisMinorTickVisibility = 1
isoVolume1Display.CubeAxesZAxisTickVisibility = 1
isoVolume1Display.CubeAxesZAxisVisibility = 1
isoVolume1Display.CubeAxesZGridLines = 0
isoVolume1Display.CubeAxesZTitle = 'Z-Axis'
isoVolume1Display.CubeAxesUseDefaultZTitle = 1
isoVolume1Display.CubeAxesGridLineLocation = 'All Faces'
isoVolume1Display.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
isoVolume1Display.CustomBoundsActive = [0, 0, 0]
isoVolume1Display.OriginalBoundsRangeActive = [0, 0, 0]
isoVolume1Display.CustomRange = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
isoVolume1Display.CustomRangeActive = [0, 0, 0]
isoVolume1Display.UseAxesOrigin = 0
isoVolume1Display.AxesOrigin = [0.0, 0.0, 0.0]
isoVolume1Display.CubeAxesXLabelFormat = '%-#6.3g'
isoVolume1Display.CubeAxesYLabelFormat = '%-#6.3g'
isoVolume1Display.CubeAxesZLabelFormat = '%-#6.3g'
isoVolume1Display.StickyAxes = 0
isoVolume1Display.CenterStickyAxes = 0
isoVolume1Display.SelectionCellLabelBold = 0
isoVolume1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
isoVolume1Display.SelectionCellLabelFontFamily = 'Arial'
isoVolume1Display.SelectionCellLabelFontSize = 18
isoVolume1Display.SelectionCellLabelItalic = 0
isoVolume1Display.SelectionCellLabelJustification = 'Left'
isoVolume1Display.SelectionCellLabelOpacity = 1.0
isoVolume1Display.SelectionCellLabelShadow = 0
isoVolume1Display.SelectionPointLabelBold = 0
isoVolume1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
isoVolume1Display.SelectionPointLabelFontFamily = 'Arial'
isoVolume1Display.SelectionPointLabelFontSize = 18
isoVolume1Display.SelectionPointLabelItalic = 0
isoVolume1Display.SelectionPointLabelJustification = 'Left'
isoVolume1Display.SelectionPointLabelOpacity = 1.0
isoVolume1Display.SelectionPointLabelShadow = 0
isoVolume1Display.ScalarOpacityUnitDistance = 30.910651385408922
isoVolume1Display.SelectMapper = 'Projected tetra'

# show color bar/color legend
isoVolume1Display.SetScalarBarVisibility(renderView1, True)

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [-11432.69921875, 0.0, 0.5, 0.0, 22564.400390625, 1.0, 0.5, 0.0]
pPWF.AllowDuplicateScalars = 1
pPWF.ScalarRangeInitialized = 1

# hide color bar/color legend
isoVolume1Display.SetScalarBarVisibility(renderView1, False)

# set scalar coloring
ColorBy(isoVolume1Display, ('POINTS', 'U'))

# rescale color and/or opacity maps used to include current data range
isoVolume1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
isoVolume1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')
uLUT.LockDataRange = 0
uLUT.InterpretValuesAsCategories = 0
uLUT.ShowCategoricalColorsinDataRangeOnly = 0
uLUT.RescaleOnVisibilityChange = 0
uLUT.EnableOpacityMapping = 0
uLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 6.430339145828138, 0.865003, 0.865003, 0.865003, 12.860678291656276, 0.705882, 0.0156863, 0.14902]
uLUT.UseLogScale = 0
uLUT.ColorSpace = 'Diverging'
uLUT.UseBelowRangeColor = 0
uLUT.BelowRangeColor = [0.0, 0.0, 0.0]
uLUT.UseAboveRangeColor = 0
uLUT.AboveRangeColor = [1.0, 1.0, 1.0]
uLUT.NanColor = [1.0, 1.0, 0.0]
uLUT.Discretize = 1
uLUT.NumberOfTableValues = 256
uLUT.ScalarRangeInitialized = 1.0
uLUT.HSVWrap = 0
uLUT.VectorComponent = 0
uLUT.VectorMode = 'Magnitude'
uLUT.AllowDuplicateScalars = 1
uLUT.Annotations = []
uLUT.ActiveAnnotatedValues = []
uLUT.IndexedColors = []

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')
uPWF.Points = [0.0, 0.0, 0.5, 0.0, 12.860678291656276, 1.0, 0.5, 0.0]
uPWF.AllowDuplicateScalars = 1
uPWF.ScalarRangeInitialized = 1

# rescale color and/or opacity maps used to exactly fit the current data range
isoVolume1Display.RescaleTransferFunctionToDataRange(False)

# Properties modified on isoVolume1Display
isoVolume1Display.Opacity = 0.7

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
uLUT.ApplyPreset('Blue to Red Rainbow', True)

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)
#uLUTColorBar.Position = [0.85, 0.05]
uLUTColorBar.Position = [0.85, 0.55]
uLUTColorBar.Position2 = [0.12, 0.43]
uLUTColorBar.AutoOrient = 1
uLUTColorBar.Orientation = 'Vertical'
uLUTColorBar.Title = 'U'
uLUTColorBar.ComponentTitle = 'Magnitude'
uLUTColorBar.TitleJustification = 'Centered'
uLUTColorBar.TitleColor = [1.0, 1.0, 1.0]
uLUTColorBar.TitleOpacity = 1.0
uLUTColorBar.TitleFontFamily = 'Arial'
uLUTColorBar.TitleBold = 0
uLUTColorBar.TitleItalic = 0
uLUTColorBar.TitleShadow = 0
uLUTColorBar.TitleFontSize = 7
uLUTColorBar.LabelColor = [1.0, 1.0, 1.0]
uLUTColorBar.LabelOpacity = 1.0
uLUTColorBar.LabelFontFamily = 'Arial'
uLUTColorBar.LabelBold = 0
uLUTColorBar.LabelItalic = 0
uLUTColorBar.LabelShadow = 0
uLUTColorBar.LabelFontSize = 7
uLUTColorBar.AutomaticLabelFormat = 1
uLUTColorBar.LabelFormat = '%-#6.3g'
uLUTColorBar.NumberOfLabels = 5
uLUTColorBar.DrawTickMarks = 1
uLUTColorBar.DrawSubTickMarks = 1
uLUTColorBar.DrawTickLabels = 1
uLUTColorBar.AddRangeLabels = 1
uLUTColorBar.RangeLabelFormat = '%4.3e'
uLUTColorBar.DrawAnnotations = 1
uLUTColorBar.AddRangeAnnotations = 0
uLUTColorBar.AutomaticAnnotations = 0
uLUTColorBar.DrawNanAnnotation = 0
uLUTColorBar.NanAnnotation = 'NaN'
uLUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
uLUTColorBar.AspectRatio = 20.0

# Properties modified on uLUTColorBar
uLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
uLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# set active source
SetActiveSource(avfoam)

# create a new 'Iso Volume'
isoVolume2 = IsoVolume(Input=avfoam)
isoVolume2.InputScalars = ['POINTS', 'p']
isoVolume2.ThresholdRange = [-11432.69921875, 31981.17578125]

# Properties modified on isoVolume2
isoVolume2.InputScalars = ['POINTS', 'region']
isoVolume2.ThresholdRange = [0.5, 1.0]

# show data in view
isoVolume2Display = Show(isoVolume2, renderView1)
# trace defaults for the display properties.
isoVolume2Display.CubeAxesVisibility = 0
isoVolume2Display.Representation = 'Surface'
isoVolume2Display.AmbientColor = [1.0, 1.0, 1.0]
isoVolume2Display.ColorArrayName = ['POINTS', 'p']
isoVolume2Display.DiffuseColor = [1.0, 1.0, 1.0]
isoVolume2Display.LookupTable = pLUT
isoVolume2Display.MapScalars = 1
isoVolume2Display.InterpolateScalarsBeforeMapping = 1
isoVolume2Display.Opacity = 1.0
isoVolume2Display.PointSize = 2.0
isoVolume2Display.LineWidth = 1.0
isoVolume2Display.Interpolation = 'Gouraud'
isoVolume2Display.Specular = 0.0
isoVolume2Display.SpecularColor = [1.0, 1.0, 1.0]
isoVolume2Display.SpecularPower = 100.0
isoVolume2Display.Ambient = 0.0
isoVolume2Display.Diffuse = 1.0
isoVolume2Display.EdgeColor = [0.0, 0.0, 0.5]
isoVolume2Display.BackfaceRepresentation = 'Follow Frontface'
isoVolume2Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
isoVolume2Display.BackfaceDiffuseColor = [1.0, 1.0, 1.0]
isoVolume2Display.BackfaceOpacity = 1.0
isoVolume2Display.Position = [0.0, 0.0, 0.0]
isoVolume2Display.Scale = [1.0, 1.0, 1.0]
isoVolume2Display.Orientation = [0.0, 0.0, 0.0]
isoVolume2Display.Origin = [0.0, 0.0, 0.0]
isoVolume2Display.Pickable = 1
isoVolume2Display.Texture = None
isoVolume2Display.Triangulate = 0
isoVolume2Display.NonlinearSubdivisionLevel = 1
isoVolume2Display.CubeAxesColor = [1.0, 1.0, 1.0]
isoVolume2Display.CubeAxesCornerOffset = 0.0
isoVolume2Display.CubeAxesFlyMode = 'Closest Triad'
isoVolume2Display.CubeAxesInertia = 1
isoVolume2Display.CubeAxesTickLocation = 'Inside'
isoVolume2Display.CubeAxesXAxisMinorTickVisibility = 1
isoVolume2Display.CubeAxesXAxisTickVisibility = 1
isoVolume2Display.CubeAxesXAxisVisibility = 1
isoVolume2Display.CubeAxesXGridLines = 0
isoVolume2Display.CubeAxesXTitle = 'X-Axis'
isoVolume2Display.CubeAxesUseDefaultXTitle = 1
isoVolume2Display.CubeAxesYAxisMinorTickVisibility = 1
isoVolume2Display.CubeAxesYAxisTickVisibility = 1
isoVolume2Display.CubeAxesYAxisVisibility = 1
isoVolume2Display.CubeAxesYGridLines = 0
isoVolume2Display.CubeAxesYTitle = 'Y-Axis'
isoVolume2Display.CubeAxesUseDefaultYTitle = 1
isoVolume2Display.CubeAxesZAxisMinorTickVisibility = 1
isoVolume2Display.CubeAxesZAxisTickVisibility = 1
isoVolume2Display.CubeAxesZAxisVisibility = 1
isoVolume2Display.CubeAxesZGridLines = 0
isoVolume2Display.CubeAxesZTitle = 'Z-Axis'
isoVolume2Display.CubeAxesUseDefaultZTitle = 1
isoVolume2Display.CubeAxesGridLineLocation = 'All Faces'
isoVolume2Display.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
isoVolume2Display.CustomBoundsActive = [0, 0, 0]
isoVolume2Display.OriginalBoundsRangeActive = [0, 0, 0]
isoVolume2Display.CustomRange = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
isoVolume2Display.CustomRangeActive = [0, 0, 0]
isoVolume2Display.UseAxesOrigin = 0
isoVolume2Display.AxesOrigin = [0.0, 0.0, 0.0]
isoVolume2Display.CubeAxesXLabelFormat = '%-#6.3g'
isoVolume2Display.CubeAxesYLabelFormat = '%-#6.3g'
isoVolume2Display.CubeAxesZLabelFormat = '%-#6.3g'
isoVolume2Display.StickyAxes = 0
isoVolume2Display.CenterStickyAxes = 0
isoVolume2Display.SelectionCellLabelBold = 0
isoVolume2Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
isoVolume2Display.SelectionCellLabelFontFamily = 'Arial'
isoVolume2Display.SelectionCellLabelFontSize = 18
isoVolume2Display.SelectionCellLabelItalic = 0
isoVolume2Display.SelectionCellLabelJustification = 'Left'
isoVolume2Display.SelectionCellLabelOpacity = 1.0
isoVolume2Display.SelectionCellLabelShadow = 0
isoVolume2Display.SelectionPointLabelBold = 0
isoVolume2Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
isoVolume2Display.SelectionPointLabelFontFamily = 'Arial'
isoVolume2Display.SelectionPointLabelFontSize = 18
isoVolume2Display.SelectionPointLabelItalic = 0
isoVolume2Display.SelectionPointLabelJustification = 'Left'
isoVolume2Display.SelectionPointLabelOpacity = 1.0
isoVolume2Display.SelectionPointLabelShadow = 0
isoVolume2Display.ScalarOpacityUnitDistance = 31.0233695029871
isoVolume2Display.SelectMapper = 'Projected tetra'

# show color bar/color legend
isoVolume2Display.SetScalarBarVisibility(renderView1, True)

# hide color bar/color legend
isoVolume2Display.SetScalarBarVisibility(renderView1, False)

# set scalar coloring
ColorBy(isoVolume2Display, ('POINTS', 'region'))

# rescale color and/or opacity maps used to include current data range
isoVolume2Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
isoVolume2Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'region'
regionLUT = GetColorTransferFunction('region')
regionLUT.LockDataRange = 0
regionLUT.InterpretValuesAsCategories = 0
regionLUT.ShowCategoricalColorsinDataRangeOnly = 0
regionLUT.RescaleOnVisibilityChange = 0
regionLUT.EnableOpacityMapping = 0
regionLUT.RGBPoints = [0.5, 0.231373, 0.298039, 0.752941, 0.75, 0.865003, 0.865003, 0.865003, 1.0, 0.705882, 0.0156863, 0.14902]
regionLUT.UseLogScale = 0
regionLUT.ColorSpace = 'Diverging'
regionLUT.UseBelowRangeColor = 0
regionLUT.BelowRangeColor = [0.0, 0.0, 0.0]
regionLUT.UseAboveRangeColor = 0
regionLUT.AboveRangeColor = [1.0, 1.0, 1.0]
regionLUT.NanColor = [1.0, 1.0, 0.0]
regionLUT.Discretize = 1
regionLUT.NumberOfTableValues = 256
regionLUT.ScalarRangeInitialized = 1.0
regionLUT.HSVWrap = 0
regionLUT.VectorComponent = 0
regionLUT.VectorMode = 'Magnitude'
regionLUT.AllowDuplicateScalars = 1
regionLUT.Annotations = []
regionLUT.ActiveAnnotatedValues = []
regionLUT.IndexedColors = []

# get opacity transfer function/opacity map for 'region'
regionPWF = GetOpacityTransferFunction('region')
regionPWF.Points = [0.5, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
regionPWF.AllowDuplicateScalars = 1
regionPWF.ScalarRangeInitialized = 1

# hide color bar/color legend
isoVolume2Display.SetScalarBarVisibility(renderView1, False)

# rescale color and/or opacity maps used to exactly fit the current data range
isoVolume2Display.RescaleTransferFunctionToDataRange(False)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
regionLUT.ApplyPreset('X Ray', True)

# Properties modified on isoVolume2Display
isoVolume2Display.Opacity = 0.3

# set active source
SetActiveSource(avfoam)

# create a new 'Annotate Time Filter'
annotateTimeFilter1 = AnnotateTimeFilter(Input=avfoam)
annotateTimeFilter1.Format = 'Time: %f'
annotateTimeFilter1.Shift = 0.0
annotateTimeFilter1.Scale = 1.0

# show data in view
annotateTimeFilter1Display = Show(annotateTimeFilter1, renderView1)
# trace defaults for the display properties.
annotateTimeFilter1Display.Interactivity = 1
annotateTimeFilter1Display.Color = [1.0, 1.0, 1.0]
annotateTimeFilter1Display.Opacity = 1.0
annotateTimeFilter1Display.FontFamily = 'Arial'
annotateTimeFilter1Display.Bold = 0
annotateTimeFilter1Display.Italic = 0
annotateTimeFilter1Display.Shadow = 0
annotateTimeFilter1Display.FontSize = 18
annotateTimeFilter1Display.Justification = 'Left'
annotateTimeFilter1Display.WindowLocation = 'AnyLocation'
annotateTimeFilter1Display.Position = [0.05, 0.05]

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.Color = [0.0, 0.0, 0.0]

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.FontSize = 1

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.FontSize = 12

# current camera placement for renderView1
#renderView1.CameraPosition = [-891.2343515938251, -1776.270816494927, 2608.103593825671]
#renderView1.CameraFocalPoint = [565.0, 640.0, 597.7865447998047]
#renderView1.CameraViewUp = [0.17225673494737004, 0.5665951267288095, 0.8057900344583793]
#renderView1.CameraParallelScale = 896.5888378797637

# save screenshot
#SaveScreenshot('pics/11.png', magnification=2, quality=100, view=renderView1)

# current camera placement for renderView1
renderView1.CameraPosition = [-891.2343515938251, -1776.270816494927, 2608.103593825671]
renderView1.CameraFocalPoint = [565.0, 640.0, 597.7865447998047]
renderView1.CameraViewUp = [0.17225673494737004, 0.5665951267288095, 0.8057900344583793]
renderView1.CameraParallelScale = 896.5888378797637

i=0
while i<len(avfoam.TimestepValues):
	# save screenshot
	SaveScreenshot('pics/'+str(i)+'.png', magnification=1, quality=100, view=renderView1)
	animationScene1.GoToNext()
	i=i+1

animationScene1.GoToFirst()

# current camera placement for renderView1
renderView1.CameraPosition = [-891.2343515938251, -1776.270816494927, 2608.103593825671]
renderView1.CameraFocalPoint = [565.0, 640.0, 597.7865447998047]
renderView1.CameraViewUp = [0.17225673494737004, 0.5665951267288095, 0.8057900344583793]
renderView1.CameraParallelScale = 896.5888378797637

# current camera placement for renderView1
renderView1.CameraPosition = [-891.2343515938251, -1776.270816494927, 2608.103593825671]
renderView1.CameraFocalPoint = [565.0, 640.0, 597.7865447998047]
renderView1.CameraViewUp = [0.17225673494737004, 0.5665951267288095, 0.8057900344583793]
renderView1.CameraParallelScale = 896.5888378797637

# save animation images/movie
WriteAnimation('pics/movie.ogv', Magnification=1, FrameRate=15.0, Compression=True)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-891.2343515938251, -1776.270816494927, 2608.103593825671]
renderView1.CameraFocalPoint = [565.0, 640.0, 597.7865447998047]
renderView1.CameraViewUp = [0.17225673494737004, 0.5665951267288095, 0.8057900344583793]
renderView1.CameraParallelScale = 896.5888378797637

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
