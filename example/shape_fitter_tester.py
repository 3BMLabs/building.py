import random
import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import tkinter as tk
import geometry.shape_fitter as sf
root = tk.Tk()
root.geometry("2000x900")
canvas = tk.Canvas(root, width=2000, height=900)
canvas.pack()

parent_lengths = [random.randrange(100, 2000, 1) for i in range(20)]
child_lengths = [random.randrange(50, 1000, 1) for i in range(20)]

#sf.fit_boxes_2d([Coords(20,20)],[Coords(10,20),Coords(10,10), Coords(10,10)], 0)

cost_function = lambda left_over_length:1 if left_over_length < 10 else left_over_length / 10


result: list[tuple[int,float]|None] = sf.fit_lengths_1d(parent_lengths,child_lengths, 3, 10)

yoff = 0
vert_size = 20
#render parent rectangles
for parent_length in parent_lengths:
    rect = canvas.create_rectangle(0,yoff, parent_length, yoff + vert_size, fill='red')
    yoff += vert_size

for (fit, child_length) in zip(result, child_lengths):
	if fit != None:
		child_y_off = fit[0] * vert_size
		rect = canvas.create_rectangle(fit[1],child_y_off, fit[1] + child_length, child_y_off + vert_size, fill='blue')
	else:
		rect = canvas.create_rectangle(0,yoff, child_length, yoff + vert_size, fill='orange')
		yoff += vert_size

#canvas.move(a, 20, 20)
root.mainloop()


