import ee
import geemap
#census data
ee.Authenticate()
ee.Initialize(project='ee-yvonnelxxxx')
Map = geemap.Map()
states = ee.FeatureCollection('TIGER/2018/States')
visParams = {
    'min': 500000000.0,
    'max': 5e+11,
    'palette': ['red','blue']
}
image = ee.Image().float().paint(states, 'ALAND')
Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/States')

roi = ee.Geometry.Polygon([
    [[-125.848, 51.384], [-125.848, 24.396], [-67.283, 24.396], [-67.283, 51.384]]
])
image = image.visualize(min=500000000.0, max=5e+11, palette=['red', 'blue'])
task = ee.batch.Export.image.toDrive(
    image,
    description='US_Map_File',
    scale=2500,
    region=roi,
    maxPixels=1e11
)
task.start()