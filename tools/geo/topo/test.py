import shapely
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon

print(Point(0,0).distance(Point(1,1)))#距离
donut = Point(0, 0).buffer(2.0).difference(Point(0, 0).buffer(1.0))
print(donut)
print(donut.centroid.wkt)# 质点
print(donut.representative_point().wkt) # 内点，计算量小

ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
int = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)][::-1]
polygon = Polygon(ext, [int])

print(polygon.is_valid)



from shapely.geometry import Point
from shapely.strtree import STRtree
polygons=[]
for i in range(0,50):
    for j in range(0,50):
        polygon=Point([i,j]).buffer(1.0)
        polygon.__setattr__('id',str(i)+str(j))
        polygons.append(polygon)
tree=STRtree(polygons)
result=tree.query(Point(1,1))
for r in result:
    print(r.__getattribute__('id'))



print('----------------------')
from shapely import wkt
from shapely.ops import polygonize
polygon=wkt.loads('POLYGON ((220 350, 400 440, 635 249, 380 80, 174 164, 179 265, 220 350))')
polyline=wkt.loads('LINESTRING (570 400, 392 315, 299 215, 430 140, 530 240, 450 360, 460 480)')
polyline2=wkt.loads('LINESTRING (560 400, 200 400)')
boundary=polygon.boundary
polyline=polyline.union(boundary).union(polyline2)
lineList = []
for i in range(0,len(polyline.geoms)):
    lineList.append(polyline.geoms[i])

clipPolygon=polygonize(lineList)
buffer=polygon.buffer(1)
for c in clipPolygon:
    if buffer.contains(c):
        print(c)


