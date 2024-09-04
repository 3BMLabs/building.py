import random
import sys, os, math
from pathlib import Path
import copy



sys.path.append(str(Path(__file__).resolve().parents[1]))
import tkinter as tk
import geometry.shape_fitter as sf
from abstract.vector import Vector
from geometry.coords import Coords
from abstract.rect import Rect

root = tk.Tk()
canvas_width = 2000
canvas_height = 900
root.geometry(f"{canvas_width}x{canvas_height}")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg= "black")
canvas.pack()

show_padding = True
show_leftovers = False
padding = 10
allowed_error = 3
parent_count = 90
child_count = 1000

def keydown(e):
	canvas.delete('all')
	global show_padding
	global show_leftovers
 
	if e.char == 'p':
		show_padding = not show_padding
	if e.char == 'l':
		show_leftovers = not show_leftovers
 
	if e.char == 'a':
		parent_lengths = [random.randrange(100, 2000, 10) for i in range(parent_count)]
		child_lengths = [random.randrange(100, 1000, 10) for i in range(child_count)]

		#sf.fit_boxes_2d([Coords(20,20)],[Coords(10,20),Coords(10,10), Coords(10,10)], 0)


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
		#2d
		parent_sizes = [Vector( random.randrange(10, 200, 10), random.randrange(10,200,5)) for i in range(parent_count)]
		child_sizes = [Vector( random.randrange(10, 50, 10), random.randrange(10,50,5)) for i in range(child_count)]
		fit_result = sf.fit_boxes_2d(parent_sizes, child_sizes, padding, allowed_error)
		child_offsets:list[tuple[int,Coords]] = fit_result.fitted_boxes

		for (off, size) in zip(child_offsets, child_sizes):
			if off == None:
				#this child didn't fit anywhere. therefore it should be fitted on screen with the parents
				parent_sizes.append(size)
		
		vert_size = (canvas_height - 100) / len(parent_sizes)

		mincost = 0
		cost = 0
		yoff = 0
		used = [False] * len(child_offsets)
  
		parent_offsets = sf.fit_boxes_2d([Coords(canvas_width, canvas_height)], parent_sizes, 50, 100).fitted_boxes
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
					child_rect = Rect(child_off, child_size)
					padded_rect = child_rect.expanded(padding)
					if show_padding:
						canvas.create_rectangle(padded_rect.x,padded_rect.y, padded_rect.x + padded_rect.size.x, padded_rect.y + padded_rect.size.y, fill='green')
					canvas.create_rectangle(child_rect.x,child_rect.y, child_rect.x + child_rect.size.x, child_rect.y + child_rect.size.y, fill='blue')
		if show_leftovers:
			for leftover_box in fit_result.leftovers:
				if parent_offsets[leftover_box[0]] != None:
					rect = leftover_box[1]
					#modify the reference to the leftover_box. that's okay
					border_width = 2
					rect.p0 += parent_offsets[leftover_box[0]][1]
					rect = rect.expanded(border_width * -0.5)
					#color="#" + ("%06x"%random.randint(0,16777215))
					color = "white"
					canvas.create_rectangle(rect.x,rect.y, rect.x + rect.width, rect.y + rect.length, outline=color, width=border_width)

					#else:
					#	grandparent_off = 
					#	canvas.create_rectangle(0,0, child_size[0], child_size[1], fill='orange')
		canvas.create_text(0, yoff ,fill="white",font="Times 20 italic bold", text=f"minimum cost: {mincost}\tcost (including cutting cost): {cost}\tloss: {((cost / mincost) - 1) * 100}%", anchor="nw")
		

#frame = tk.Frame(root, width=100, height=100)
canvas.bind("<KeyPress>", keydown)

canvas.pack()
canvas.focus_set()

#canvas.move(a, 20, 20)
root.mainloop()


