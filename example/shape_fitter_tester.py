import operator
import random
import sys, os, math
from pathlib import Path
import copy


sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.matrix import Matrix
import tkinter as tk
import geometry.shape_fitter as sf
from abstract.vector import Vector
from geometry.coords import Coords
from abstract.rect import Rect
from geometry.point import Point
from geometry.curve import Line, Polygon
from shape_fitter_test_data import test_data

root = tk.Tk()
geo_width = 2000
geo_height = 900
canvas_width = geo_width
canvas_height = geo_height
root.geometry(f"{int(geo_width)}x{int(geo_height)}")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg= "black")
canvas.pack()

show_padding = True
show_leftovers = False
padding = 10
allowed_error = 3
parent_count = 5
child_count = 1000
ctest = Coords(x = 3)
ctest2 = Coords(4,3,2)
ctest3 = Coords([3,5])
test_angle = Line(Coords(1,2), Coords(1,4)).angle

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
	elif e.char == 's':
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
  
		parent_offsets = sf.fit_boxes_2d([Coords(geo_width, geo_height)], parent_sizes, 50, 100).fitted_boxes
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
	else:
		available_parent_invoicing_widths = [2450, 2500, 2730, 2950, 3100, 3200, 3300, 3400, 3500]
		min_length = 8500
		max_length = 16500
		parent_sizes = [Vector(random.uniform(min_length, max_length), random.choice(available_parent_invoicing_widths)) for i in range(parent_count)]
		
		#child_polygons = [Polygon.rectangular(Rect(0,0,200,200)), Polygon(Point(0,0), Point(200, 0), Point(0,200)), Polygon(Point(200,0), Point(200, 200), Point(0,200)), Polygon(Point(0,0), Point(50,0), Point(70,50), Point(0, 50)), Polygon(Point(0,0), Point(70,0), Point(70,50), Point(20, 50))]

		#get first 30 polygons from test data
		child_polygons = random.sample(test_data, 30)
		#adjust the test data to make it valid
  
		for poly in child_polygons:
			#first of all, move each polygon so the mimimum corner is at 0,0,0
			poly -= poly.bounds.p0
			poly.closed = True
   
		fit_result = sf.fit_polygons_2d(parent_sizes, child_polygons, allowed_error)
  
		scale_factor = 30
  
		parent_offsets = sf.fit_boxes_2d([Coords(canvas_width * scale_factor, canvas_height * scale_factor)], parent_sizes, 50, 100).fitted_boxes
		
		area_to_screen = Matrix.scale(2, 1.0 / scale_factor)
		
		
  
		for (parent_offset,parent_size) in zip(parent_offsets, parent_sizes):
			if parent_offset != None:
				final_rect = Rect(parent_offset[1].x,parent_offset[1].y, parent_offset[1].x+parent_size.x, parent_offset[1].y + parent_size.y)
				final_rect = area_to_screen * final_rect
				canvas.create_rectangle(final_rect.x, final_rect.y, final_rect.p1.x, final_rect.p1.y, fill='red', outline='purple')

		#for group, box in zip(fit_result.grouped_polygons, fit_result.box_result.fitted_boxes):
		#	if box != None:
		#		if parent_offsets[box[0]] != None:
		#			parent_off = parent_offsets[box[0]][1]
		#			group_off = parent_off + box[1]
		#			final_rect = Rect(group_off, group.bounds.size)
		#			final_rect = area_to_screen * final_rect
		#			canvas.create_rectangle(final_rect.x, final_rect.y, final_rect.p1.x, final_rect.p1.y, outline= 'green') # fill='green'
    #
		#for(child_off, child_poly) in zip(fit_result.fitted_children, child_polygons):
		#	if child_off != None:
		#		parent_off = parent_offsets[child_off[0]]
		#		if parent_off != None:
		#			child_poly.translate(parent_off[1] + child_off[1])
		#			final_poly = area_to_screen * child_poly
		#			
		#			canvas.create_polygon(final_poly, outline='pink', fill='magenta')
  
		

#frame = tk.Frame(root, width=100, height=100)
canvas.bind("<KeyPress>", keydown)

canvas.pack()
canvas.focus_set()

#canvas.move(a, 20, 20)
root.mainloop()


