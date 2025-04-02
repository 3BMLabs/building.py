from geometry.rect import Rect



from PIL import Image, ImageDraw

from geometry.curve import Arc, Polygon
from abstract.vector import Point
from construction.profile import IShapeParallelFlangeProfile

PC = IShapeParallelFlangeProfile("test",200,200,10,15,15).curve

widthpix = 1000 #[pix]
heightpix = 1000 #[pix]
scalefactor = SF = 3

img = Image.new("RGB", (widthpix,heightpix))
img1 = ImageDraw.Draw(img)

bounds = Rect.by_points(Polygon.by_joined_curves(PC))

dx = 50
xmin = bounds[0] - dx
ymin = bounds[2] - dx

for i in PC.curves:
    if i.__class__.__name__ == "Arc":
        AC = Arc(Point(i.start.x,i.start.y,0),Point(i.mid.x,i.mid.y,0),Point(i.end.x,i.end.y,0))
        lines = Arc.segmented_arc(AC,15)
        for i in lines:
            x0 = (i.start.x - xmin) * SF
            y0 = (i.start.y - ymin) * SF
            x1 = (i.end.x - xmin) * SF
            y1 = (i.end.y - ymin) * SF
            coords = [(x0,y0),(x1,y1)]
            img1.line(coords, fill="blue", width=2)
    elif i.__class__.__name__ == "Line":
        coords = [((i.start.x-xmin)*SF,(i.start.y-ymin)*SF),((i.end.x-xmin)*SF,(i.end.y-ymin)*SF)]
        img1.line(coords, fill="blue", width=2)
    else:
        print("unknown curve is used")

img.show()