import random
import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import tkinter as tk
import geometry.shape_fitter as sf
from abstract.vector import Vector

root = tk.Tk()
canvas_width = 2000
canvas_height = 900
root.geometry(f"{canvas_width}x{canvas_height}")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

def keydown(e):
	canvas.delete('all')
	if e.char == 'a':
	
		parent_lengths = [random.randrange(100, 2000, 100) for i in range(10)]
		child_lengths = [random.randrange(100, 1000, 100) for i in range(15)]

		#sf.fit_boxes_2d([Coords(20,20)],[Coords(10,20),Coords(10,10), Coords(10,10)], 0)

		cost_function = lambda left_over_length:1 if left_over_length < 10 else left_over_length / 10


		result: list[tuple[int,float]|None] = sf.fit_lengths_1d(parent_lengths,child_lengths, 3, 10)

		mincost = 0
		cost = 0

		yoff = 0
		vert_size = (canvas_height - 100) / len(parent_lengths)
		used = [False] * len(result)
		#render parent rectangles
		for parent_length in parent_lengths:
			canvas.create_rectangle(0,yoff, parent_length, yoff + vert_size, fill='red')
			yoff += vert_size

		for (fit, child_length) in zip(result, child_lengths):
			mincost += child_length
			if fit != None:
				if not used[fit[0]]:
					used[fit[0]] = True
					cost += parent_lengths[fit[0]]
				child_y_off = fit[0] * vert_size
				canvas.create_rectangle(fit[1],child_y_off, fit[1] + child_length, child_y_off + vert_size, fill='blue')
			else:
				canvas.create_rectangle(0,yoff, child_length, yoff + vert_size, fill='orange')
				yoff += vert_size


		canvas.create_text(0, yoff ,fill="black",font="Times 20 italic bold", text=f"minimum cost: {mincost}\tcost (including cutting cost): {cost}\tloss: {((cost / mincost) - 1) * 100}%", anchor="nw")
	else:
		#2d
		parent_sizes = [Vector( random.randrange(100, 1000, 100), random.randrange(100,1000,1)) for i in range(10)]
		child_sizes = [Vector( random.randrange(100, 400, 100), random.randrange(100,400,1)) for i in range(10)]
		result = sf.fit_boxes_2d(parent_sizes, child_sizes, 10)

		mincost = 0
		cost = 0
		yoff = 0
		used = [False] * len(result)
		#render parent rectangles
		for parent_size in parent_sizes:
			canvas.create_rectangle(0,yoff, parent_size.x, yoff + parent_size.y, fill='red')
			yoff += parent_size.y

		for (fit, child_size) in zip(result, child_sizes):
			mincost += child_size
			if fit != None:
				if not used[fit[0]]:
					used[fit[0]] = True
					cost += parent_lengths[fit[0]]
				child_y_off = fit[0] * vert_size
				canvas.create_rectangle(fit[1],child_y_off, fit[1] + child_length, child_y_off + vert_size, fill='blue')
			else:
				canvas.create_rectangle(0,yoff, child, yoff + vert_size, fill='orange')
				yoff += vert_size
		

#frame = tk.Frame(root, width=100, height=100)
canvas.bind("<KeyPress>", keydown)

canvas.pack()
canvas.focus_set()

#canvas.move(a, 20, 20)
root.mainloop()


