from shapely import affinity
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

polygon = Polygon([(55.7777367,13.0162430),(-10.5371666,73.8334503),(-20.4613228,63.0121956),(45.8535805,2.19499207)])
polygon1 = Polygon([(433.974976,188.822174),(150.104111,449.159851),(-110.245483,165.275848),(173.625397,-95.0617065)])
polygon2 = Polygon([(55.8769798,13.1244564),(-10.4379253,73.9416656),(-20.5605659,62.9039841),(45.7543411,2.08678055)])
polygon_s = affinity.scale(polygon, xfact=1.01, yfact=1.01, origin='center')
print(polygon_s)
polygon.union(polygon1)
#plt.plot(*(polygon1.union(polygon)).exterior.xy)
plt.plot(*polygon.exterior.xy)
plt.plot(*polygon2.exterior.xy)
plt.show()