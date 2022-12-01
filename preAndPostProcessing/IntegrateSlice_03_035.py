# trace generated using paraview version 5.10.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
foamfoam = OpenFOAMReader(registrationName='foam.foam', FileName='./foam.foam')
foamfoam.SkipZeroTime = 1
foamfoam.CaseType = 'Reconstructed Case'
foamfoam.LabelSize = '32-bit'
foamfoam.ScalarSize = '64-bit (DP)'
foamfoam.Createcelltopointfiltereddata = 1
foamfoam.Adddimensionalunitstoarraynames = 0
foamfoam.MeshRegions = ['internalMesh']
foamfoam.CellArrays = ['U', 'alpha.entrained', 'alpha.gas', 'alpha.liquid', 'alpha.soil', 'alphas', 'cg', 'magGradAlpha.entrained', 'magGradAlpha.gas', 'magGradAlpha.liquid', 'magGradAlpha.soil', 'nu.entrained', 'nu.liquid', 'nu.soil', 'p', 'p_rgh', 'specificStrainRate.entrained', 'specificStrainRate.gas', 'specificStrainRate.liquid', 'specificStrainRate.soil']
foamfoam.PointArrays = []
foamfoam.LagrangianArrays = []
foamfoam.Cachemesh = 1
foamfoam.Decomposepolyhedra = 1
foamfoam.ListtimestepsaccordingtocontrolDict = 0
foamfoam.Lagrangianpositionswithoutextradata = 1
foamfoam.Readzones = 0
foamfoam.Copydatatocellzones = 0

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
foamfoamDisplay = Show(foamfoam, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
pLUT.InterpretValuesAsCategories = 0
pLUT.AnnotationsInitialized = 0
pLUT.ShowCategoricalColorsinDataRangeOnly = 0
pLUT.RescaleOnVisibilityChange = 0
pLUT.EnableOpacityMapping = 0
pLUT.RGBPoints = [-124.08985900878906, 0.231373, 0.298039, 0.752941, 836.5134201049805, 0.865003, 0.865003, 0.865003, 1797.11669921875, 0.705882, 0.0156863, 0.14902]
pLUT.UseLogScale = 0
pLUT.UseOpacityControlPointsFreehandDrawing = 0
pLUT.ShowDataHistogram = 0
pLUT.AutomaticDataHistogramComputation = 0
pLUT.DataHistogramNumberOfBins = 10
pLUT.ColorSpace = 'Diverging'
pLUT.UseBelowRangeColor = 0
pLUT.BelowRangeColor = [0.0, 0.0, 0.0]
pLUT.UseAboveRangeColor = 0
pLUT.AboveRangeColor = [0.5, 0.5, 0.5]
pLUT.NanColor = [1.0, 1.0, 0.0]
pLUT.NanOpacity = 1.0
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
pLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [-124.08985900878906, 0.0, 0.5, 0.0, 1797.11669921875, 1.0, 0.5, 0.0]
pPWF.AllowDuplicateScalars = 1
pPWF.UseLogScale = 0
pPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
foamfoamDisplay.Selection = None
foamfoamDisplay.Representation = 'Surface'
foamfoamDisplay.ColorArrayName = ['POINTS', 'p']
foamfoamDisplay.LookupTable = pLUT
foamfoamDisplay.MapScalars = 1
foamfoamDisplay.MultiComponentsMapping = 0
foamfoamDisplay.InterpolateScalarsBeforeMapping = 1
foamfoamDisplay.Opacity = 1.0
foamfoamDisplay.PointSize = 2.0
foamfoamDisplay.LineWidth = 1.0
foamfoamDisplay.RenderLinesAsTubes = 0
foamfoamDisplay.RenderPointsAsSpheres = 0
foamfoamDisplay.Interpolation = 'Gouraud'
foamfoamDisplay.Specular = 0.0
foamfoamDisplay.SpecularColor = [1.0, 1.0, 1.0]
foamfoamDisplay.SpecularPower = 100.0
foamfoamDisplay.Luminosity = 0.0
foamfoamDisplay.Ambient = 0.0
foamfoamDisplay.Diffuse = 1.0
foamfoamDisplay.Roughness = 0.3
foamfoamDisplay.Metallic = 0.0
foamfoamDisplay.EdgeTint = [1.0, 1.0, 1.0]
foamfoamDisplay.Anisotropy = 0.0
foamfoamDisplay.AnisotropyRotation = 0.0
foamfoamDisplay.BaseIOR = 1.5
foamfoamDisplay.CoatStrength = 0.0
foamfoamDisplay.CoatIOR = 2.0
foamfoamDisplay.CoatRoughness = 0.0
foamfoamDisplay.CoatColor = [1.0, 1.0, 1.0]
foamfoamDisplay.SelectTCoordArray = 'None'
foamfoamDisplay.SelectNormalArray = 'None'
foamfoamDisplay.SelectTangentArray = 'None'
foamfoamDisplay.Texture = None
foamfoamDisplay.RepeatTextures = 1
foamfoamDisplay.InterpolateTextures = 0
foamfoamDisplay.SeamlessU = 0
foamfoamDisplay.SeamlessV = 0
foamfoamDisplay.UseMipmapTextures = 0
foamfoamDisplay.ShowTexturesOnBackface = 1
foamfoamDisplay.BaseColorTexture = None
foamfoamDisplay.NormalTexture = None
foamfoamDisplay.NormalScale = 1.0
foamfoamDisplay.CoatNormalTexture = None
foamfoamDisplay.CoatNormalScale = 1.0
foamfoamDisplay.MaterialTexture = None
foamfoamDisplay.OcclusionStrength = 1.0
foamfoamDisplay.AnisotropyTexture = None
foamfoamDisplay.EmissiveTexture = None
foamfoamDisplay.EmissiveFactor = [1.0, 1.0, 1.0]
foamfoamDisplay.FlipTextures = 0
foamfoamDisplay.BackfaceRepresentation = 'Follow Frontface'
foamfoamDisplay.BackfaceAmbientColor = [1.0, 1.0, 1.0]
foamfoamDisplay.BackfaceOpacity = 1.0
foamfoamDisplay.Position = [0.0, 0.0, 0.0]
foamfoamDisplay.Scale = [1.0, 1.0, 1.0]
foamfoamDisplay.Orientation = [0.0, 0.0, 0.0]
foamfoamDisplay.Origin = [0.0, 0.0, 0.0]
foamfoamDisplay.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
foamfoamDisplay.Pickable = 1
foamfoamDisplay.Triangulate = 0
foamfoamDisplay.UseShaderReplacements = 0
foamfoamDisplay.ShaderReplacements = ''
foamfoamDisplay.NonlinearSubdivisionLevel = 1
foamfoamDisplay.UseDataPartitions = 0
foamfoamDisplay.OSPRayUseScaleArray = 'All Approximate'
foamfoamDisplay.OSPRayScaleArray = 'p'
foamfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
foamfoamDisplay.OSPRayMaterial = 'None'
foamfoamDisplay.BlockSelectors = ['/']
foamfoamDisplay.BlockColors = []
foamfoamDisplay.BlockOpacities = []
foamfoamDisplay.Orient = 0
foamfoamDisplay.OrientationMode = 'Direction'
foamfoamDisplay.SelectOrientationVectors = 'U'
foamfoamDisplay.Scaling = 0
foamfoamDisplay.ScaleMode = 'No Data Scaling Off'
foamfoamDisplay.ScaleFactor = 0.11000000014901162
foamfoamDisplay.SelectScaleArray = 'p'
foamfoamDisplay.GlyphType = 'Arrow'
foamfoamDisplay.UseGlyphTable = 0
foamfoamDisplay.GlyphTableIndexArray = 'p'
foamfoamDisplay.UseCompositeGlyphTable = 0
foamfoamDisplay.UseGlyphCullingAndLOD = 0
foamfoamDisplay.LODValues = []
foamfoamDisplay.ColorByLODIndex = 0
foamfoamDisplay.GaussianRadius = 0.005500000007450581
foamfoamDisplay.ShaderPreset = 'Sphere'
foamfoamDisplay.CustomTriangleScale = 3
foamfoamDisplay.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
foamfoamDisplay.Emissive = 0
foamfoamDisplay.ScaleByArray = 0
foamfoamDisplay.SetScaleArray = ['POINTS', 'p']
foamfoamDisplay.ScaleArrayComponent = ''
foamfoamDisplay.UseScaleFunction = 1
foamfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
foamfoamDisplay.OpacityByArray = 0
foamfoamDisplay.OpacityArray = ['POINTS', 'p']
foamfoamDisplay.OpacityArrayComponent = ''
foamfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
foamfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
foamfoamDisplay.SelectionCellLabelBold = 0
foamfoamDisplay.SelectionCellLabelColor = [0.0, 1.0, 0.0]
foamfoamDisplay.SelectionCellLabelFontFamily = 'Arial'
foamfoamDisplay.SelectionCellLabelFontFile = ''
foamfoamDisplay.SelectionCellLabelFontSize = 18
foamfoamDisplay.SelectionCellLabelItalic = 0
foamfoamDisplay.SelectionCellLabelJustification = 'Left'
foamfoamDisplay.SelectionCellLabelOpacity = 1.0
foamfoamDisplay.SelectionCellLabelShadow = 0
foamfoamDisplay.SelectionPointLabelBold = 0
foamfoamDisplay.SelectionPointLabelColor = [1.0, 1.0, 0.0]
foamfoamDisplay.SelectionPointLabelFontFamily = 'Arial'
foamfoamDisplay.SelectionPointLabelFontFile = ''
foamfoamDisplay.SelectionPointLabelFontSize = 18
foamfoamDisplay.SelectionPointLabelItalic = 0
foamfoamDisplay.SelectionPointLabelJustification = 'Left'
foamfoamDisplay.SelectionPointLabelOpacity = 1.0
foamfoamDisplay.SelectionPointLabelShadow = 0
foamfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
foamfoamDisplay.ScalarOpacityFunction = pPWF
foamfoamDisplay.ScalarOpacityUnitDistance = 0.04878865861255562
foamfoamDisplay.UseSeparateOpacityArray = 0
foamfoamDisplay.OpacityArrayName = ['POINTS', 'p']
foamfoamDisplay.OpacityComponent = ''
foamfoamDisplay.SelectMapper = 'Projected tetra'
foamfoamDisplay.SamplingDimensions = [128, 128, 128]
foamfoamDisplay.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
foamfoamDisplay.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
foamfoamDisplay.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
foamfoamDisplay.GlyphType.TipResolution = 6
foamfoamDisplay.GlyphType.TipRadius = 0.1
foamfoamDisplay.GlyphType.TipLength = 0.35
foamfoamDisplay.GlyphType.ShaftResolution = 6
foamfoamDisplay.GlyphType.ShaftRadius = 0.03
foamfoamDisplay.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
foamfoamDisplay.ScaleTransferFunction.Points = [-124.08985900878906, 0.0, 0.5, 0.0, 1797.11669921875, 1.0, 0.5, 0.0]
foamfoamDisplay.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
foamfoamDisplay.OpacityTransferFunction.Points = [-124.08985900878906, 0.0, 0.5, 0.0, 1797.11669921875, 1.0, 0.5, 0.0]
foamfoamDisplay.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
foamfoamDisplay.DataAxesGrid.XTitle = 'X Axis'
foamfoamDisplay.DataAxesGrid.YTitle = 'Y Axis'
foamfoamDisplay.DataAxesGrid.ZTitle = 'Z Axis'
foamfoamDisplay.DataAxesGrid.XTitleFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.XTitleFontFile = ''
foamfoamDisplay.DataAxesGrid.XTitleBold = 0
foamfoamDisplay.DataAxesGrid.XTitleItalic = 0
foamfoamDisplay.DataAxesGrid.XTitleFontSize = 12
foamfoamDisplay.DataAxesGrid.XTitleShadow = 0
foamfoamDisplay.DataAxesGrid.XTitleOpacity = 1.0
foamfoamDisplay.DataAxesGrid.YTitleFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.YTitleFontFile = ''
foamfoamDisplay.DataAxesGrid.YTitleBold = 0
foamfoamDisplay.DataAxesGrid.YTitleItalic = 0
foamfoamDisplay.DataAxesGrid.YTitleFontSize = 12
foamfoamDisplay.DataAxesGrid.YTitleShadow = 0
foamfoamDisplay.DataAxesGrid.YTitleOpacity = 1.0
foamfoamDisplay.DataAxesGrid.ZTitleFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.ZTitleFontFile = ''
foamfoamDisplay.DataAxesGrid.ZTitleBold = 0
foamfoamDisplay.DataAxesGrid.ZTitleItalic = 0
foamfoamDisplay.DataAxesGrid.ZTitleFontSize = 12
foamfoamDisplay.DataAxesGrid.ZTitleShadow = 0
foamfoamDisplay.DataAxesGrid.ZTitleOpacity = 1.0
foamfoamDisplay.DataAxesGrid.FacesToRender = 63
foamfoamDisplay.DataAxesGrid.CullBackface = 0
foamfoamDisplay.DataAxesGrid.CullFrontface = 1
foamfoamDisplay.DataAxesGrid.ShowGrid = 0
foamfoamDisplay.DataAxesGrid.ShowEdges = 1
foamfoamDisplay.DataAxesGrid.ShowTicks = 1
foamfoamDisplay.DataAxesGrid.LabelUniqueEdgesOnly = 1
foamfoamDisplay.DataAxesGrid.AxesToLabel = 63
foamfoamDisplay.DataAxesGrid.XLabelFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.XLabelFontFile = ''
foamfoamDisplay.DataAxesGrid.XLabelBold = 0
foamfoamDisplay.DataAxesGrid.XLabelItalic = 0
foamfoamDisplay.DataAxesGrid.XLabelFontSize = 12
foamfoamDisplay.DataAxesGrid.XLabelShadow = 0
foamfoamDisplay.DataAxesGrid.XLabelOpacity = 1.0
foamfoamDisplay.DataAxesGrid.YLabelFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.YLabelFontFile = ''
foamfoamDisplay.DataAxesGrid.YLabelBold = 0
foamfoamDisplay.DataAxesGrid.YLabelItalic = 0
foamfoamDisplay.DataAxesGrid.YLabelFontSize = 12
foamfoamDisplay.DataAxesGrid.YLabelShadow = 0
foamfoamDisplay.DataAxesGrid.YLabelOpacity = 1.0
foamfoamDisplay.DataAxesGrid.ZLabelFontFamily = 'Arial'
foamfoamDisplay.DataAxesGrid.ZLabelFontFile = ''
foamfoamDisplay.DataAxesGrid.ZLabelBold = 0
foamfoamDisplay.DataAxesGrid.ZLabelItalic = 0
foamfoamDisplay.DataAxesGrid.ZLabelFontSize = 12
foamfoamDisplay.DataAxesGrid.ZLabelShadow = 0
foamfoamDisplay.DataAxesGrid.ZLabelOpacity = 1.0
foamfoamDisplay.DataAxesGrid.XAxisNotation = 'Mixed'
foamfoamDisplay.DataAxesGrid.XAxisPrecision = 2
foamfoamDisplay.DataAxesGrid.XAxisUseCustomLabels = 0
foamfoamDisplay.DataAxesGrid.XAxisLabels = []
foamfoamDisplay.DataAxesGrid.YAxisNotation = 'Mixed'
foamfoamDisplay.DataAxesGrid.YAxisPrecision = 2
foamfoamDisplay.DataAxesGrid.YAxisUseCustomLabels = 0
foamfoamDisplay.DataAxesGrid.YAxisLabels = []
foamfoamDisplay.DataAxesGrid.ZAxisNotation = 'Mixed'
foamfoamDisplay.DataAxesGrid.ZAxisPrecision = 2
foamfoamDisplay.DataAxesGrid.ZAxisUseCustomLabels = 0
foamfoamDisplay.DataAxesGrid.ZAxisLabels = []
foamfoamDisplay.DataAxesGrid.UseCustomBounds = 0
foamfoamDisplay.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
foamfoamDisplay.PolarAxes.Visibility = 0
foamfoamDisplay.PolarAxes.Translation = [0.0, 0.0, 0.0]
foamfoamDisplay.PolarAxes.Scale = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.Orientation = [0.0, 0.0, 0.0]
foamfoamDisplay.PolarAxes.EnableCustomBounds = [0, 0, 0]
foamfoamDisplay.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
foamfoamDisplay.PolarAxes.EnableCustomRange = 0
foamfoamDisplay.PolarAxes.CustomRange = [0.0, 1.0]
foamfoamDisplay.PolarAxes.PolarAxisVisibility = 1
foamfoamDisplay.PolarAxes.RadialAxesVisibility = 1
foamfoamDisplay.PolarAxes.DrawRadialGridlines = 1
foamfoamDisplay.PolarAxes.PolarArcsVisibility = 1
foamfoamDisplay.PolarAxes.DrawPolarArcsGridlines = 1
foamfoamDisplay.PolarAxes.NumberOfRadialAxes = 0
foamfoamDisplay.PolarAxes.AutoSubdividePolarAxis = 1
foamfoamDisplay.PolarAxes.NumberOfPolarAxis = 0
foamfoamDisplay.PolarAxes.MinimumRadius = 0.0
foamfoamDisplay.PolarAxes.MinimumAngle = 0.0
foamfoamDisplay.PolarAxes.MaximumAngle = 90.0
foamfoamDisplay.PolarAxes.RadialAxesOriginToPolarAxis = 1
foamfoamDisplay.PolarAxes.Ratio = 1.0
foamfoamDisplay.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
foamfoamDisplay.PolarAxes.PolarAxisTitleVisibility = 1
foamfoamDisplay.PolarAxes.PolarAxisTitle = 'Radial Distance'
foamfoamDisplay.PolarAxes.PolarAxisTitleLocation = 'Bottom'
foamfoamDisplay.PolarAxes.PolarLabelVisibility = 1
foamfoamDisplay.PolarAxes.PolarLabelFormat = '%-#6.3g'
foamfoamDisplay.PolarAxes.PolarLabelExponentLocation = 'Labels'
foamfoamDisplay.PolarAxes.RadialLabelVisibility = 1
foamfoamDisplay.PolarAxes.RadialLabelFormat = '%-#3.1f'
foamfoamDisplay.PolarAxes.RadialLabelLocation = 'Bottom'
foamfoamDisplay.PolarAxes.RadialUnitsVisibility = 1
foamfoamDisplay.PolarAxes.ScreenSize = 10.0
foamfoamDisplay.PolarAxes.PolarAxisTitleOpacity = 1.0
foamfoamDisplay.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
foamfoamDisplay.PolarAxes.PolarAxisTitleFontFile = ''
foamfoamDisplay.PolarAxes.PolarAxisTitleBold = 0
foamfoamDisplay.PolarAxes.PolarAxisTitleItalic = 0
foamfoamDisplay.PolarAxes.PolarAxisTitleShadow = 0
foamfoamDisplay.PolarAxes.PolarAxisTitleFontSize = 12
foamfoamDisplay.PolarAxes.PolarAxisLabelOpacity = 1.0
foamfoamDisplay.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
foamfoamDisplay.PolarAxes.PolarAxisLabelFontFile = ''
foamfoamDisplay.PolarAxes.PolarAxisLabelBold = 0
foamfoamDisplay.PolarAxes.PolarAxisLabelItalic = 0
foamfoamDisplay.PolarAxes.PolarAxisLabelShadow = 0
foamfoamDisplay.PolarAxes.PolarAxisLabelFontSize = 12
foamfoamDisplay.PolarAxes.LastRadialAxisTextOpacity = 1.0
foamfoamDisplay.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
foamfoamDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
foamfoamDisplay.PolarAxes.LastRadialAxisTextBold = 0
foamfoamDisplay.PolarAxes.LastRadialAxisTextItalic = 0
foamfoamDisplay.PolarAxes.LastRadialAxisTextShadow = 0
foamfoamDisplay.PolarAxes.LastRadialAxisTextFontSize = 12
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextBold = 0
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextItalic = 0
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextShadow = 0
foamfoamDisplay.PolarAxes.SecondaryRadialAxesTextFontSize = 12
foamfoamDisplay.PolarAxes.EnableDistanceLOD = 1
foamfoamDisplay.PolarAxes.DistanceLODThreshold = 0.7
foamfoamDisplay.PolarAxes.EnableViewAngleLOD = 1
foamfoamDisplay.PolarAxes.ViewAngleLODThreshold = 0.7
foamfoamDisplay.PolarAxes.SmallestVisiblePolarAngle = 0.5
foamfoamDisplay.PolarAxes.PolarTicksVisibility = 1
foamfoamDisplay.PolarAxes.ArcTicksOriginToPolarAxis = 1
foamfoamDisplay.PolarAxes.TickLocation = 'Both'
foamfoamDisplay.PolarAxes.AxisTickVisibility = 1
foamfoamDisplay.PolarAxes.AxisMinorTickVisibility = 0
foamfoamDisplay.PolarAxes.ArcTickVisibility = 1
foamfoamDisplay.PolarAxes.ArcMinorTickVisibility = 0
foamfoamDisplay.PolarAxes.DeltaAngleMajor = 10.0
foamfoamDisplay.PolarAxes.DeltaAngleMinor = 5.0
foamfoamDisplay.PolarAxes.PolarAxisMajorTickSize = 0.0
foamfoamDisplay.PolarAxes.PolarAxisTickRatioSize = 0.3
foamfoamDisplay.PolarAxes.PolarAxisMajorTickThickness = 1.0
foamfoamDisplay.PolarAxes.PolarAxisTickRatioThickness = 0.5
foamfoamDisplay.PolarAxes.LastRadialAxisMajorTickSize = 0.0
foamfoamDisplay.PolarAxes.LastRadialAxisTickRatioSize = 0.3
foamfoamDisplay.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
foamfoamDisplay.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
foamfoamDisplay.PolarAxes.ArcMajorTickSize = 0.0
foamfoamDisplay.PolarAxes.ArcTickRatioSize = 0.3
foamfoamDisplay.PolarAxes.ArcMajorTickThickness = 1.0
foamfoamDisplay.PolarAxes.ArcTickRatioThickness = 0.5
foamfoamDisplay.PolarAxes.Use2DMode = 0
foamfoamDisplay.PolarAxes.UseLogAxis = 0

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
foamfoamDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera(False)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=foamfoam)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['POINTS', 'p']
clip1.Value = 836.5134201049805
clip1.Invert = 1
clip1.Crinkleclip = 0
clip1.Exact = 0

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [0.44999999925494194, 0.02500000037252903, 0.15000000596046448]
clip1.ClipType.Normal = [1.0, 0.0, 0.0]
clip1.ClipType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [0.44999999925494194, 0.02500000037252903, 0.15000000596046448]
clip1.HyperTreeGridClipper.Normal = [1.0, 0.0, 0.0]
clip1.HyperTreeGridClipper.Offset = 0.0

# Properties modified on clip1.ClipType
clip1.ClipType.Origin = [0.3, 0.02500000037252903, 0.15000000596046448]

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Selection = None
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['POINTS', 'p']
clip1Display.LookupTable = pLUT
clip1Display.MapScalars = 1
clip1Display.MultiComponentsMapping = 0
clip1Display.InterpolateScalarsBeforeMapping = 1
clip1Display.Opacity = 1.0
clip1Display.PointSize = 2.0
clip1Display.LineWidth = 1.0
clip1Display.RenderLinesAsTubes = 0
clip1Display.RenderPointsAsSpheres = 0
clip1Display.Interpolation = 'Gouraud'
clip1Display.Specular = 0.0
clip1Display.SpecularColor = [1.0, 1.0, 1.0]
clip1Display.SpecularPower = 100.0
clip1Display.Luminosity = 0.0
clip1Display.Ambient = 0.0
clip1Display.Diffuse = 1.0
clip1Display.Roughness = 0.3
clip1Display.Metallic = 0.0
clip1Display.EdgeTint = [1.0, 1.0, 1.0]
clip1Display.Anisotropy = 0.0
clip1Display.AnisotropyRotation = 0.0
clip1Display.BaseIOR = 1.5
clip1Display.CoatStrength = 0.0
clip1Display.CoatIOR = 2.0
clip1Display.CoatRoughness = 0.0
clip1Display.CoatColor = [1.0, 1.0, 1.0]
clip1Display.SelectTCoordArray = 'None'
clip1Display.SelectNormalArray = 'None'
clip1Display.SelectTangentArray = 'None'
clip1Display.Texture = None
clip1Display.RepeatTextures = 1
clip1Display.InterpolateTextures = 0
clip1Display.SeamlessU = 0
clip1Display.SeamlessV = 0
clip1Display.UseMipmapTextures = 0
clip1Display.ShowTexturesOnBackface = 1
clip1Display.BaseColorTexture = None
clip1Display.NormalTexture = None
clip1Display.NormalScale = 1.0
clip1Display.CoatNormalTexture = None
clip1Display.CoatNormalScale = 1.0
clip1Display.MaterialTexture = None
clip1Display.OcclusionStrength = 1.0
clip1Display.AnisotropyTexture = None
clip1Display.EmissiveTexture = None
clip1Display.EmissiveFactor = [1.0, 1.0, 1.0]
clip1Display.FlipTextures = 0
clip1Display.BackfaceRepresentation = 'Follow Frontface'
clip1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
clip1Display.BackfaceOpacity = 1.0
clip1Display.Position = [0.0, 0.0, 0.0]
clip1Display.Scale = [1.0, 1.0, 1.0]
clip1Display.Orientation = [0.0, 0.0, 0.0]
clip1Display.Origin = [0.0, 0.0, 0.0]
clip1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
clip1Display.Pickable = 1
clip1Display.Triangulate = 0
clip1Display.UseShaderReplacements = 0
clip1Display.ShaderReplacements = ''
clip1Display.NonlinearSubdivisionLevel = 1
clip1Display.UseDataPartitions = 0
clip1Display.OSPRayUseScaleArray = 'All Approximate'
clip1Display.OSPRayScaleArray = 'p'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.OSPRayMaterial = 'None'
clip1Display.BlockSelectors = ['/']
clip1Display.BlockColors = []
clip1Display.BlockOpacities = []
clip1Display.Orient = 0
clip1Display.OrientationMode = 'Direction'
clip1Display.SelectOrientationVectors = 'U'
clip1Display.Scaling = 0
clip1Display.ScaleMode = 'No Data Scaling Off'
clip1Display.ScaleFactor = 0.030000001192092896
clip1Display.SelectScaleArray = 'p'
clip1Display.GlyphType = 'Arrow'
clip1Display.UseGlyphTable = 0
clip1Display.GlyphTableIndexArray = 'p'
clip1Display.UseCompositeGlyphTable = 0
clip1Display.UseGlyphCullingAndLOD = 0
clip1Display.LODValues = []
clip1Display.ColorByLODIndex = 0
clip1Display.GaussianRadius = 0.0015000000596046448
clip1Display.ShaderPreset = 'Sphere'
clip1Display.CustomTriangleScale = 3
clip1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
clip1Display.Emissive = 0
clip1Display.ScaleByArray = 0
clip1Display.SetScaleArray = ['POINTS', 'p']
clip1Display.ScaleArrayComponent = ''
clip1Display.UseScaleFunction = 1
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityByArray = 0
clip1Display.OpacityArray = ['POINTS', 'p']
clip1Display.OpacityArrayComponent = ''
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.SelectionCellLabelBold = 0
clip1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
clip1Display.SelectionCellLabelFontFamily = 'Arial'
clip1Display.SelectionCellLabelFontFile = ''
clip1Display.SelectionCellLabelFontSize = 18
clip1Display.SelectionCellLabelItalic = 0
clip1Display.SelectionCellLabelJustification = 'Left'
clip1Display.SelectionCellLabelOpacity = 1.0
clip1Display.SelectionCellLabelShadow = 0
clip1Display.SelectionPointLabelBold = 0
clip1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
clip1Display.SelectionPointLabelFontFamily = 'Arial'
clip1Display.SelectionPointLabelFontFile = ''
clip1Display.SelectionPointLabelFontSize = 18
clip1Display.SelectionPointLabelItalic = 0
clip1Display.SelectionPointLabelJustification = 'Left'
clip1Display.SelectionPointLabelOpacity = 1.0
clip1Display.SelectionPointLabelShadow = 0
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = pPWF
clip1Display.ScalarOpacityUnitDistance = 0.028631322913142923
clip1Display.UseSeparateOpacityArray = 0
clip1Display.OpacityArrayName = ['POINTS', 'p']
clip1Display.OpacityComponent = ''
clip1Display.SelectMapper = 'Projected tetra'
clip1Display.SamplingDimensions = [128, 128, 128]
clip1Display.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
clip1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
clip1Display.GlyphType.TipResolution = 6
clip1Display.GlyphType.TipRadius = 0.1
clip1Display.GlyphType.TipLength = 0.35
clip1Display.GlyphType.ShaftResolution = 6
clip1Display.GlyphType.ShaftRadius = 0.03
clip1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip1Display.ScaleTransferFunction.Points = [-124.08985900878906, 0.0, 0.5, 0.0, 1583.58837890625, 1.0, 0.5, 0.0]
clip1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip1Display.OpacityTransferFunction.Points = [-124.08985900878906, 0.0, 0.5, 0.0, 1583.58837890625, 1.0, 0.5, 0.0]
clip1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip1Display.DataAxesGrid.XTitle = 'X Axis'
clip1Display.DataAxesGrid.YTitle = 'Y Axis'
clip1Display.DataAxesGrid.ZTitle = 'Z Axis'
clip1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.XTitleFontFile = ''
clip1Display.DataAxesGrid.XTitleBold = 0
clip1Display.DataAxesGrid.XTitleItalic = 0
clip1Display.DataAxesGrid.XTitleFontSize = 12
clip1Display.DataAxesGrid.XTitleShadow = 0
clip1Display.DataAxesGrid.XTitleOpacity = 1.0
clip1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.YTitleFontFile = ''
clip1Display.DataAxesGrid.YTitleBold = 0
clip1Display.DataAxesGrid.YTitleItalic = 0
clip1Display.DataAxesGrid.YTitleFontSize = 12
clip1Display.DataAxesGrid.YTitleShadow = 0
clip1Display.DataAxesGrid.YTitleOpacity = 1.0
clip1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.ZTitleFontFile = ''
clip1Display.DataAxesGrid.ZTitleBold = 0
clip1Display.DataAxesGrid.ZTitleItalic = 0
clip1Display.DataAxesGrid.ZTitleFontSize = 12
clip1Display.DataAxesGrid.ZTitleShadow = 0
clip1Display.DataAxesGrid.ZTitleOpacity = 1.0
clip1Display.DataAxesGrid.FacesToRender = 63
clip1Display.DataAxesGrid.CullBackface = 0
clip1Display.DataAxesGrid.CullFrontface = 1
clip1Display.DataAxesGrid.ShowGrid = 0
clip1Display.DataAxesGrid.ShowEdges = 1
clip1Display.DataAxesGrid.ShowTicks = 1
clip1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
clip1Display.DataAxesGrid.AxesToLabel = 63
clip1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.XLabelFontFile = ''
clip1Display.DataAxesGrid.XLabelBold = 0
clip1Display.DataAxesGrid.XLabelItalic = 0
clip1Display.DataAxesGrid.XLabelFontSize = 12
clip1Display.DataAxesGrid.XLabelShadow = 0
clip1Display.DataAxesGrid.XLabelOpacity = 1.0
clip1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.YLabelFontFile = ''
clip1Display.DataAxesGrid.YLabelBold = 0
clip1Display.DataAxesGrid.YLabelItalic = 0
clip1Display.DataAxesGrid.YLabelFontSize = 12
clip1Display.DataAxesGrid.YLabelShadow = 0
clip1Display.DataAxesGrid.YLabelOpacity = 1.0
clip1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.ZLabelFontFile = ''
clip1Display.DataAxesGrid.ZLabelBold = 0
clip1Display.DataAxesGrid.ZLabelItalic = 0
clip1Display.DataAxesGrid.ZLabelFontSize = 12
clip1Display.DataAxesGrid.ZLabelShadow = 0
clip1Display.DataAxesGrid.ZLabelOpacity = 1.0
clip1Display.DataAxesGrid.XAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.XAxisPrecision = 2
clip1Display.DataAxesGrid.XAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.XAxisLabels = []
clip1Display.DataAxesGrid.YAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.YAxisPrecision = 2
clip1Display.DataAxesGrid.YAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.YAxisLabels = []
clip1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.ZAxisPrecision = 2
clip1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.ZAxisLabels = []
clip1Display.DataAxesGrid.UseCustomBounds = 0
clip1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip1Display.PolarAxes.Visibility = 0
clip1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
clip1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
clip1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
clip1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
clip1Display.PolarAxes.EnableCustomRange = 0
clip1Display.PolarAxes.CustomRange = [0.0, 1.0]
clip1Display.PolarAxes.PolarAxisVisibility = 1
clip1Display.PolarAxes.RadialAxesVisibility = 1
clip1Display.PolarAxes.DrawRadialGridlines = 1
clip1Display.PolarAxes.PolarArcsVisibility = 1
clip1Display.PolarAxes.DrawPolarArcsGridlines = 1
clip1Display.PolarAxes.NumberOfRadialAxes = 0
clip1Display.PolarAxes.AutoSubdividePolarAxis = 1
clip1Display.PolarAxes.NumberOfPolarAxis = 0
clip1Display.PolarAxes.MinimumRadius = 0.0
clip1Display.PolarAxes.MinimumAngle = 0.0
clip1Display.PolarAxes.MaximumAngle = 90.0
clip1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
clip1Display.PolarAxes.Ratio = 1.0
clip1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.PolarAxisTitleVisibility = 1
clip1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
clip1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
clip1Display.PolarAxes.PolarLabelVisibility = 1
clip1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
clip1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
clip1Display.PolarAxes.RadialLabelVisibility = 1
clip1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
clip1Display.PolarAxes.RadialLabelLocation = 'Bottom'
clip1Display.PolarAxes.RadialUnitsVisibility = 1
clip1Display.PolarAxes.ScreenSize = 10.0
clip1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
clip1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
clip1Display.PolarAxes.PolarAxisTitleFontFile = ''
clip1Display.PolarAxes.PolarAxisTitleBold = 0
clip1Display.PolarAxes.PolarAxisTitleItalic = 0
clip1Display.PolarAxes.PolarAxisTitleShadow = 0
clip1Display.PolarAxes.PolarAxisTitleFontSize = 12
clip1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
clip1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
clip1Display.PolarAxes.PolarAxisLabelFontFile = ''
clip1Display.PolarAxes.PolarAxisLabelBold = 0
clip1Display.PolarAxes.PolarAxisLabelItalic = 0
clip1Display.PolarAxes.PolarAxisLabelShadow = 0
clip1Display.PolarAxes.PolarAxisLabelFontSize = 12
clip1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
clip1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
clip1Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip1Display.PolarAxes.LastRadialAxisTextBold = 0
clip1Display.PolarAxes.LastRadialAxisTextItalic = 0
clip1Display.PolarAxes.LastRadialAxisTextShadow = 0
clip1Display.PolarAxes.LastRadialAxisTextFontSize = 12
clip1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
clip1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
clip1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
clip1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
clip1Display.PolarAxes.EnableDistanceLOD = 1
clip1Display.PolarAxes.DistanceLODThreshold = 0.7
clip1Display.PolarAxes.EnableViewAngleLOD = 1
clip1Display.PolarAxes.ViewAngleLODThreshold = 0.7
clip1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
clip1Display.PolarAxes.PolarTicksVisibility = 1
clip1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
clip1Display.PolarAxes.TickLocation = 'Both'
clip1Display.PolarAxes.AxisTickVisibility = 1
clip1Display.PolarAxes.AxisMinorTickVisibility = 0
clip1Display.PolarAxes.ArcTickVisibility = 1
clip1Display.PolarAxes.ArcMinorTickVisibility = 0
clip1Display.PolarAxes.DeltaAngleMajor = 10.0
clip1Display.PolarAxes.DeltaAngleMinor = 5.0
clip1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
clip1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
clip1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
clip1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
clip1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
clip1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
clip1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
clip1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
clip1Display.PolarAxes.ArcMajorTickSize = 0.0
clip1Display.PolarAxes.ArcTickRatioSize = 0.3
clip1Display.PolarAxes.ArcMajorTickThickness = 1.0
clip1Display.PolarAxes.ArcTickRatioThickness = 0.5
clip1Display.PolarAxes.Use2DMode = 0
clip1Display.PolarAxes.UseLogAxis = 0

# hide data in view
Hide(foamfoam, renderView1)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on clip1.ClipType
clip1.ClipType.Normal = [-1.0, 0.0, 0.0]

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=clip1)
clip2.ClipType = 'Plane'
clip2.HyperTreeGridClipper = 'Plane'
clip2.Scalars = ['POINTS', 'p']
clip2.Value = 897.651868224144
clip2.Invert = 1
clip2.Crinkleclip = 0
clip2.Exact = 0

# init the 'Plane' selected for 'ClipType'
clip2.ClipType.Origin = [0.5750000029802322, 0.02500000037252903, 0.15000000596046448]
clip2.ClipType.Normal = [1.0, 0.0, 0.0]
clip2.ClipType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip2.HyperTreeGridClipper.Origin = [0.5750000029802322, 0.02500000037252903, 0.15000000596046448]
clip2.HyperTreeGridClipper.Normal = [1.0, 0.0, 0.0]
clip2.HyperTreeGridClipper.Offset = 0.0

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = [0.35, 0.02500000037252903, 0.15000000596046448]

# show data in view
clip2Display = Show(clip2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip2Display.Selection = None
clip2Display.Representation = 'Surface'
clip2Display.ColorArrayName = ['POINTS', 'p']
clip2Display.LookupTable = pLUT
clip2Display.MapScalars = 1
clip2Display.MultiComponentsMapping = 0
clip2Display.InterpolateScalarsBeforeMapping = 1
clip2Display.Opacity = 1.0
clip2Display.PointSize = 2.0
clip2Display.LineWidth = 1.0
clip2Display.RenderLinesAsTubes = 0
clip2Display.RenderPointsAsSpheres = 0
clip2Display.Interpolation = 'Gouraud'
clip2Display.Specular = 0.0
clip2Display.SpecularColor = [1.0, 1.0, 1.0]
clip2Display.SpecularPower = 100.0
clip2Display.Luminosity = 0.0
clip2Display.Ambient = 0.0
clip2Display.Diffuse = 1.0
clip2Display.Roughness = 0.3
clip2Display.Metallic = 0.0
clip2Display.EdgeTint = [1.0, 1.0, 1.0]
clip2Display.Anisotropy = 0.0
clip2Display.AnisotropyRotation = 0.0
clip2Display.BaseIOR = 1.5
clip2Display.CoatStrength = 0.0
clip2Display.CoatIOR = 2.0
clip2Display.CoatRoughness = 0.0
clip2Display.CoatColor = [1.0, 1.0, 1.0]
clip2Display.SelectTCoordArray = 'None'
clip2Display.SelectNormalArray = 'None'
clip2Display.SelectTangentArray = 'None'
clip2Display.Texture = None
clip2Display.RepeatTextures = 1
clip2Display.InterpolateTextures = 0
clip2Display.SeamlessU = 0
clip2Display.SeamlessV = 0
clip2Display.UseMipmapTextures = 0
clip2Display.ShowTexturesOnBackface = 1
clip2Display.BaseColorTexture = None
clip2Display.NormalTexture = None
clip2Display.NormalScale = 1.0
clip2Display.CoatNormalTexture = None
clip2Display.CoatNormalScale = 1.0
clip2Display.MaterialTexture = None
clip2Display.OcclusionStrength = 1.0
clip2Display.AnisotropyTexture = None
clip2Display.EmissiveTexture = None
clip2Display.EmissiveFactor = [1.0, 1.0, 1.0]
clip2Display.FlipTextures = 0
clip2Display.BackfaceRepresentation = 'Follow Frontface'
clip2Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
clip2Display.BackfaceOpacity = 1.0
clip2Display.Position = [0.0, 0.0, 0.0]
clip2Display.Scale = [1.0, 1.0, 1.0]
clip2Display.Orientation = [0.0, 0.0, 0.0]
clip2Display.Origin = [0.0, 0.0, 0.0]
clip2Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
clip2Display.Pickable = 1
clip2Display.Triangulate = 0
clip2Display.UseShaderReplacements = 0
clip2Display.ShaderReplacements = ''
clip2Display.NonlinearSubdivisionLevel = 1
clip2Display.UseDataPartitions = 0
clip2Display.OSPRayUseScaleArray = 'All Approximate'
clip2Display.OSPRayScaleArray = 'p'
clip2Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip2Display.OSPRayMaterial = 'None'
clip2Display.BlockSelectors = ['/']
clip2Display.BlockColors = []
clip2Display.BlockOpacities = []
clip2Display.Orient = 0
clip2Display.OrientationMode = 'Direction'
clip2Display.SelectOrientationVectors = 'U'
clip2Display.Scaling = 0
clip2Display.ScaleMode = 'No Data Scaling Off'
clip2Display.ScaleFactor = 0.030000001192092896
clip2Display.SelectScaleArray = 'p'
clip2Display.GlyphType = 'Arrow'
clip2Display.UseGlyphTable = 0
clip2Display.GlyphTableIndexArray = 'p'
clip2Display.UseCompositeGlyphTable = 0
clip2Display.UseGlyphCullingAndLOD = 0
clip2Display.LODValues = []
clip2Display.ColorByLODIndex = 0
clip2Display.GaussianRadius = 0.0015000000596046448
clip2Display.ShaderPreset = 'Sphere'
clip2Display.CustomTriangleScale = 3
clip2Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
clip2Display.Emissive = 0
clip2Display.ScaleByArray = 0
clip2Display.SetScaleArray = ['POINTS', 'p']
clip2Display.ScaleArrayComponent = ''
clip2Display.UseScaleFunction = 1
clip2Display.ScaleTransferFunction = 'PiecewiseFunction'
clip2Display.OpacityByArray = 0
clip2Display.OpacityArray = ['POINTS', 'p']
clip2Display.OpacityArrayComponent = ''
clip2Display.OpacityTransferFunction = 'PiecewiseFunction'
clip2Display.DataAxesGrid = 'GridAxesRepresentation'
clip2Display.SelectionCellLabelBold = 0
clip2Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
clip2Display.SelectionCellLabelFontFamily = 'Arial'
clip2Display.SelectionCellLabelFontFile = ''
clip2Display.SelectionCellLabelFontSize = 18
clip2Display.SelectionCellLabelItalic = 0
clip2Display.SelectionCellLabelJustification = 'Left'
clip2Display.SelectionCellLabelOpacity = 1.0
clip2Display.SelectionCellLabelShadow = 0
clip2Display.SelectionPointLabelBold = 0
clip2Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
clip2Display.SelectionPointLabelFontFamily = 'Arial'
clip2Display.SelectionPointLabelFontFile = ''
clip2Display.SelectionPointLabelFontSize = 18
clip2Display.SelectionPointLabelItalic = 0
clip2Display.SelectionPointLabelJustification = 'Left'
clip2Display.SelectionPointLabelOpacity = 1.0
clip2Display.SelectionPointLabelShadow = 0
clip2Display.PolarAxes = 'PolarAxesRepresentation'
clip2Display.ScalarOpacityFunction = pPWF
clip2Display.ScalarOpacityUnitDistance = 0.035400862234615485
clip2Display.UseSeparateOpacityArray = 0
clip2Display.OpacityArrayName = ['POINTS', 'p']
clip2Display.OpacityComponent = ''
clip2Display.SelectMapper = 'Projected tetra'
clip2Display.SamplingDimensions = [128, 128, 128]
clip2Display.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
clip2Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip2Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
clip2Display.GlyphType.TipResolution = 6
clip2Display.GlyphType.TipRadius = 0.1
clip2Display.GlyphType.TipLength = 0.35
clip2Display.GlyphType.ShaftResolution = 6
clip2Display.GlyphType.ShaftRadius = 0.03
clip2Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip2Display.ScaleTransferFunction.Points = [-1.8129627704620361, 0.0, 0.5, 0.0, 1251.8614501953125, 1.0, 0.5, 0.0]
clip2Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip2Display.OpacityTransferFunction.Points = [-1.8129627704620361, 0.0, 0.5, 0.0, 1251.8614501953125, 1.0, 0.5, 0.0]
clip2Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip2Display.DataAxesGrid.XTitle = 'X Axis'
clip2Display.DataAxesGrid.YTitle = 'Y Axis'
clip2Display.DataAxesGrid.ZTitle = 'Z Axis'
clip2Display.DataAxesGrid.XTitleFontFamily = 'Arial'
clip2Display.DataAxesGrid.XTitleFontFile = ''
clip2Display.DataAxesGrid.XTitleBold = 0
clip2Display.DataAxesGrid.XTitleItalic = 0
clip2Display.DataAxesGrid.XTitleFontSize = 12
clip2Display.DataAxesGrid.XTitleShadow = 0
clip2Display.DataAxesGrid.XTitleOpacity = 1.0
clip2Display.DataAxesGrid.YTitleFontFamily = 'Arial'
clip2Display.DataAxesGrid.YTitleFontFile = ''
clip2Display.DataAxesGrid.YTitleBold = 0
clip2Display.DataAxesGrid.YTitleItalic = 0
clip2Display.DataAxesGrid.YTitleFontSize = 12
clip2Display.DataAxesGrid.YTitleShadow = 0
clip2Display.DataAxesGrid.YTitleOpacity = 1.0
clip2Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
clip2Display.DataAxesGrid.ZTitleFontFile = ''
clip2Display.DataAxesGrid.ZTitleBold = 0
clip2Display.DataAxesGrid.ZTitleItalic = 0
clip2Display.DataAxesGrid.ZTitleFontSize = 12
clip2Display.DataAxesGrid.ZTitleShadow = 0
clip2Display.DataAxesGrid.ZTitleOpacity = 1.0
clip2Display.DataAxesGrid.FacesToRender = 63
clip2Display.DataAxesGrid.CullBackface = 0
clip2Display.DataAxesGrid.CullFrontface = 1
clip2Display.DataAxesGrid.ShowGrid = 0
clip2Display.DataAxesGrid.ShowEdges = 1
clip2Display.DataAxesGrid.ShowTicks = 1
clip2Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
clip2Display.DataAxesGrid.AxesToLabel = 63
clip2Display.DataAxesGrid.XLabelFontFamily = 'Arial'
clip2Display.DataAxesGrid.XLabelFontFile = ''
clip2Display.DataAxesGrid.XLabelBold = 0
clip2Display.DataAxesGrid.XLabelItalic = 0
clip2Display.DataAxesGrid.XLabelFontSize = 12
clip2Display.DataAxesGrid.XLabelShadow = 0
clip2Display.DataAxesGrid.XLabelOpacity = 1.0
clip2Display.DataAxesGrid.YLabelFontFamily = 'Arial'
clip2Display.DataAxesGrid.YLabelFontFile = ''
clip2Display.DataAxesGrid.YLabelBold = 0
clip2Display.DataAxesGrid.YLabelItalic = 0
clip2Display.DataAxesGrid.YLabelFontSize = 12
clip2Display.DataAxesGrid.YLabelShadow = 0
clip2Display.DataAxesGrid.YLabelOpacity = 1.0
clip2Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
clip2Display.DataAxesGrid.ZLabelFontFile = ''
clip2Display.DataAxesGrid.ZLabelBold = 0
clip2Display.DataAxesGrid.ZLabelItalic = 0
clip2Display.DataAxesGrid.ZLabelFontSize = 12
clip2Display.DataAxesGrid.ZLabelShadow = 0
clip2Display.DataAxesGrid.ZLabelOpacity = 1.0
clip2Display.DataAxesGrid.XAxisNotation = 'Mixed'
clip2Display.DataAxesGrid.XAxisPrecision = 2
clip2Display.DataAxesGrid.XAxisUseCustomLabels = 0
clip2Display.DataAxesGrid.XAxisLabels = []
clip2Display.DataAxesGrid.YAxisNotation = 'Mixed'
clip2Display.DataAxesGrid.YAxisPrecision = 2
clip2Display.DataAxesGrid.YAxisUseCustomLabels = 0
clip2Display.DataAxesGrid.YAxisLabels = []
clip2Display.DataAxesGrid.ZAxisNotation = 'Mixed'
clip2Display.DataAxesGrid.ZAxisPrecision = 2
clip2Display.DataAxesGrid.ZAxisUseCustomLabels = 0
clip2Display.DataAxesGrid.ZAxisLabels = []
clip2Display.DataAxesGrid.UseCustomBounds = 0
clip2Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip2Display.PolarAxes.Visibility = 0
clip2Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
clip2Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
clip2Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
clip2Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
clip2Display.PolarAxes.EnableCustomRange = 0
clip2Display.PolarAxes.CustomRange = [0.0, 1.0]
clip2Display.PolarAxes.PolarAxisVisibility = 1
clip2Display.PolarAxes.RadialAxesVisibility = 1
clip2Display.PolarAxes.DrawRadialGridlines = 1
clip2Display.PolarAxes.PolarArcsVisibility = 1
clip2Display.PolarAxes.DrawPolarArcsGridlines = 1
clip2Display.PolarAxes.NumberOfRadialAxes = 0
clip2Display.PolarAxes.AutoSubdividePolarAxis = 1
clip2Display.PolarAxes.NumberOfPolarAxis = 0
clip2Display.PolarAxes.MinimumRadius = 0.0
clip2Display.PolarAxes.MinimumAngle = 0.0
clip2Display.PolarAxes.MaximumAngle = 90.0
clip2Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
clip2Display.PolarAxes.Ratio = 1.0
clip2Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
clip2Display.PolarAxes.PolarAxisTitleVisibility = 1
clip2Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
clip2Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
clip2Display.PolarAxes.PolarLabelVisibility = 1
clip2Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
clip2Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
clip2Display.PolarAxes.RadialLabelVisibility = 1
clip2Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
clip2Display.PolarAxes.RadialLabelLocation = 'Bottom'
clip2Display.PolarAxes.RadialUnitsVisibility = 1
clip2Display.PolarAxes.ScreenSize = 10.0
clip2Display.PolarAxes.PolarAxisTitleOpacity = 1.0
clip2Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
clip2Display.PolarAxes.PolarAxisTitleFontFile = ''
clip2Display.PolarAxes.PolarAxisTitleBold = 0
clip2Display.PolarAxes.PolarAxisTitleItalic = 0
clip2Display.PolarAxes.PolarAxisTitleShadow = 0
clip2Display.PolarAxes.PolarAxisTitleFontSize = 12
clip2Display.PolarAxes.PolarAxisLabelOpacity = 1.0
clip2Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
clip2Display.PolarAxes.PolarAxisLabelFontFile = ''
clip2Display.PolarAxes.PolarAxisLabelBold = 0
clip2Display.PolarAxes.PolarAxisLabelItalic = 0
clip2Display.PolarAxes.PolarAxisLabelShadow = 0
clip2Display.PolarAxes.PolarAxisLabelFontSize = 12
clip2Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
clip2Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
clip2Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip2Display.PolarAxes.LastRadialAxisTextBold = 0
clip2Display.PolarAxes.LastRadialAxisTextItalic = 0
clip2Display.PolarAxes.LastRadialAxisTextShadow = 0
clip2Display.PolarAxes.LastRadialAxisTextFontSize = 12
clip2Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
clip2Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
clip2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
clip2Display.PolarAxes.SecondaryRadialAxesTextBold = 0
clip2Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
clip2Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
clip2Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
clip2Display.PolarAxes.EnableDistanceLOD = 1
clip2Display.PolarAxes.DistanceLODThreshold = 0.7
clip2Display.PolarAxes.EnableViewAngleLOD = 1
clip2Display.PolarAxes.ViewAngleLODThreshold = 0.7
clip2Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
clip2Display.PolarAxes.PolarTicksVisibility = 1
clip2Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
clip2Display.PolarAxes.TickLocation = 'Both'
clip2Display.PolarAxes.AxisTickVisibility = 1
clip2Display.PolarAxes.AxisMinorTickVisibility = 0
clip2Display.PolarAxes.ArcTickVisibility = 1
clip2Display.PolarAxes.ArcMinorTickVisibility = 0
clip2Display.PolarAxes.DeltaAngleMajor = 10.0
clip2Display.PolarAxes.DeltaAngleMinor = 5.0
clip2Display.PolarAxes.PolarAxisMajorTickSize = 0.0
clip2Display.PolarAxes.PolarAxisTickRatioSize = 0.3
clip2Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
clip2Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
clip2Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
clip2Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
clip2Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
clip2Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
clip2Display.PolarAxes.ArcMajorTickSize = 0.0
clip2Display.PolarAxes.ArcTickRatioSize = 0.3
clip2Display.PolarAxes.ArcMajorTickThickness = 1.0
clip2Display.PolarAxes.ArcTickRatioThickness = 0.5
clip2Display.PolarAxes.Use2DMode = 0
clip2Display.PolarAxes.UseLogAxis = 0

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=clip2)
integrateVariables1.DivideCellDataByVolume = 0

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.UseCache = 0
spreadSheetView1.ViewSize = [400, 400]
spreadSheetView1.CellFontSize = 9
spreadSheetView1.HeaderFontSize = 9
spreadSheetView1.SelectionOnly = 0
spreadSheetView1.GenerateCellConnectivity = 0
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.InvertOrder = 0
spreadSheetView1.BlockSize = 1024
spreadSheetView1.HiddenColumnLabels = ['Block Number']
spreadSheetView1.FieldAssociation = 'Point Data'

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
integrateVariables1Display.Assembly = 'Hierarchy'
integrateVariables1Display.BlockVisibilities = []

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# Properties modified on integrateVariables1Display
integrateVariables1Display.Assembly = ''

# update the view to ensure updated data information
spreadSheetView1.Update()

# save data
SaveData('./data/IntegrateSlice_03_035.csv', proxy=integrateVariables1, WriteTimeSteps=1,
    Filenamesuffix='_%d',
    ChooseArraysToWrite=0,
    PointDataArrays=['U', 'alpha.entrained', 'alpha.gas', 'alpha.liquid', 'alpha.soil', 'alphas', 'cg', 'magGradAlpha.entrained', 'magGradAlpha.gas', 'magGradAlpha.liquid', 'magGradAlpha.soil', 'nu.entrained', 'nu.liquid', 'nu.soil', 'p', 'p_rgh', 'specificStrainRate.entrained', 'specificStrainRate.gas', 'specificStrainRate.liquid', 'specificStrainRate.soil', 'U', 'Volume', 'alpha.entrained', 'alpha.gas', 'alpha.liquid', 'alpha.soil', 'alphas', 'cg', 'magGradAlpha.entrained', 'magGradAlpha.gas', 'magGradAlpha.liquid', 'magGradAlpha.soil', 'nu.entrained', 'nu.liquid', 'nu.soil', 'p', 'p_rgh', 'specificStrainRate.entrained', 'specificStrainRate.gas', 'specificStrainRate.liquid', 'specificStrainRate.soil'],
    CellDataArrays=['U', 'alpha.entrained', 'alpha.gas', 'alpha.liquid', 'alpha.soil', 'alphas', 'cg', 'magGradAlpha.entrained', 'magGradAlpha.gas', 'magGradAlpha.liquid', 'magGradAlpha.soil', 'nu.entrained', 'nu.liquid', 'nu.soil', 'p', 'p_rgh', 'specificStrainRate.entrained', 'specificStrainRate.gas', 'specificStrainRate.liquid', 'specificStrainRate.soil', 'U', 'Volume', 'alpha.entrained', 'alpha.gas', 'alpha.liquid', 'alpha.soil', 'alphas', 'cg', 'magGradAlpha.entrained', 'magGradAlpha.gas', 'magGradAlpha.liquid', 'magGradAlpha.soil', 'nu.entrained', 'nu.liquid', 'nu.soil', 'p', 'p_rgh', 'specificStrainRate.entrained', 'specificStrainRate.gas', 'specificStrainRate.liquid', 'specificStrainRate.soil'],
    FieldDataArrays=['CasePath'],
    VertexDataArrays=[],
    EdgeDataArrays=[],
    RowDataArrays=[],
    Precision=5,
    UseScientificNotation=0,
    FieldAssociation='Point Data',
    AddMetaData=1,
    AddTime=1)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1410, 1324)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.44999999925494194, -2.179766702946633, 0.15000000596046448]
renderView1.CameraFocalPoint = [0.44999999925494194, 0.02500000037252903, 0.15000000596046448]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.5706356128268982

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
