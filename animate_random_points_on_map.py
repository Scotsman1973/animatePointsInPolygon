import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
from shapely.geometry import shape
import fiona

with fiona.open(r"C:\Mythings\Data\Unst_data\ActivityArea.shp", 'r') as shapefile:
    for record in shapefile:
        polygon = shape(record['geometry'])

fig, ax = plt.subplots()
fontsize = 12

gdf_polygon = gpd.GeoDataFrame(index=[0],crs='epsg:28355', geometry=[polygon])
gdf_polygon.plot(ax=ax, edgecolor='black')

ims = []
count = []
pointsAsSamples = []

def update_fig(i):
    
    minx, miny, maxx, maxy = polygon.bounds
    #add number and how many points were excavated previously
    pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    if polygon.contains(pnt):
        pointsAsSamples.append(pnt)

    gdf_points = gpd.GeoDataFrame({'geometry': pointsAsSamples})#random point data used to create a geodataframe
    gdf_points = gdf_points.set_crs("EPSG:28355")
    #checks if there's more than zero records in the list, if so deleate the first record,
    if len(pointsAsSamples) > 0:
        del pointsAsSamples[0]
    geos = gdf_points['geometry']
    
    artist = gpd.plotting.plot_point_collection(ax, geos)
    ims.append(artist)
    
    ax.set_title('Random points')
    ax.set_axis_off()
    fig = ax.get_figure()
    return ims

anim = FuncAnimation(fig, update_fig, interval=400, frames=200 )

#this next line creates a temporary path line, without having to adjust the user defined environment variables
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\Andrew Prentice\AppData\Local\Programs\Python\Python310\Lib\ffmpeg\bin\ffmpeg.exe'
FFwriter=animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# saving to m4 using ffmpeg writer 
anim.save(r'C:\Mythings\PhD\ECM\randomPoints2.mp4', writer=FFwriter)

plt.show()