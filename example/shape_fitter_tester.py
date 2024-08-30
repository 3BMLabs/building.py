import random
import sys, os, math
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))
import tkinter as tk
import geometry.shape_fitter as sf
from abstract.vector import Vector
from geometry.coords import Coords

root = tk.Tk()
canvas_width = 2000
canvas_height = 900
root.geometry(f"{canvas_width}x{canvas_height}")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

def keydown(e):
	canvas.delete('all')
 
	padding = 3
	allowed_error = 10
	if e.char == 'a':
		parent_counts = 8
		child_counts = 10
		parent_lengths = [random.randrange(100, 2000, 10) for i in range(parent_counts)]
		child_lengths = [random.randrange(100, 1000, 10) for i in range(child_counts)]

		#sf.fit_boxes_2d([Coords(20,20)],[Coords(10,20),Coords(10,10), Coords(10,10)], 0)

		cost_function = lambda left_over_length:1 if left_over_length < 10 else left_over_length / 10


		child_offsets: list[tuple[int,float]|None] = sf.fit_lengths_1d(parent_lengths,child_lengths, padding, allowed_error)

		mincost = 0
		cost = 0

		yoff = 0
		vert_size = (canvas_height - 100) / len(parent_lengths)
		used = [False] * len(child_offsets)
		#render parent rectangles
		for parent_length in parent_lengths:
			canvas.create_rectangle(0,yoff, parent_length, yoff + vert_size, fill='red')
			yoff += vert_size

		for (child_off, child_length) in zip(child_offsets, child_lengths):
			mincost += child_length
			if child_off != None:
				if not used[child_off[0]]:
					used[child_off[0]] = True
					cost += parent_lengths[child_off[0]]
				child_y_off = child_off[0] * vert_size
				canvas.create_rectangle(child_off[1],child_y_off, child_off[1] + child_length, child_y_off + vert_size, fill='blue')
			else:
				canvas.create_rectangle(0,yoff, child_length, yoff + vert_size, fill='orange')
				yoff += vert_size


		canvas.create_text(0, yoff ,fill="black",font="Times 20 italic bold", text=f"minimum cost: {mincost}\tcost (including cutting cost): {cost}\tloss: {((cost / mincost) - 1) * 100}%", anchor="nw")
	else:
		parent_count = 20
		child_count = 100
		#2d
		parent_sizes = [Vector( random.randrange(10, 200, 10), random.randrange(10,200,5)) for i in range(parent_count)]
		child_sizes = [Vector( random.randrange(10, 50, 10), random.randrange(10,50,5)) for i in range(child_count)]
		child_offsets:list[tuple[int,Coords]] = sf.fit_boxes_2d(parent_sizes, child_sizes, 10)

		for (off, size) in zip(child_offsets, child_sizes):
			if off == None:
				parent_sizes.append(size)
		
		vert_size = (canvas_height - 100) / len(parent_sizes)

		mincost = 0
		cost = 0
		yoff = 0
		used = [False] * len(child_offsets)
  
		parent_offsets = sf.fit_boxes_2d([Coords(canvas_width, canvas_height)], parent_sizes, padding)
		grandparent_array_off = 0
		#render parent rectangles
		for (parent_offset,parent_size) in zip(parent_offsets, parent_sizes):
			if parent_offset != None:
				canvas.create_rectangle(parent_offset[1].x,parent_offset[1].y, parent_offset[1].x+parent_size.x, parent_offset[1].y + parent_size.y, fill=('red' if grandparent_array_off < parent_count else 'orange'))
			grandparent_array_off += 1

		for (child_off, child_size) in zip(child_offsets, child_sizes):
			mincost += child_size.volume()
			if child_off != None:
				if parent_offsets[child_off[0]] != None:
					if not used[child_off[0]]:
						used[child_off[0]] = True
						cost += parent_sizes[child_off[0]].volume()
					child_off = parent_offsets[child_off[0]][1] + child_off[1]
					canvas.create_rectangle(child_off.x,child_off.y, child_off.x + child_size.x, child_off.y + child_size.y, fill='blue')
			#else:
			#	grandparent_off = 
			#	canvas.create_rectangle(0,0, child_size[0], child_size[1], fill='orange')
		

#frame = tk.Frame(root, width=100, height=100)
canvas.bind("<KeyPress>", keydown)

canvas.pack()
canvas.focus_set()

#canvas.move(a, 20, 20)
root.mainloop()


