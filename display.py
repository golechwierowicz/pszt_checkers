#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairocffi as cairo
import math
import threading
from rules import Checker, EDGE_SIZE


class BoardWindow(Gtk.Window):
	def __init__(self, q):
		super(BoardWindow, self).__init__()

		self.q = q
		self.board_state = False
		self.init_ui()

		t = threading.Thread(target=self.wait_for_update, args=[])
		t.start()

	def wait_for_update(self):
		while True:
			self.board_state = self.q.get()
			self.queue_draw()

	def init_ui(self):
		self.drawing_area = Gtk.DrawingArea()
		self.drawing_area.connect("draw", self.on_draw)
		self.drawing_area.connect("button-press-event", self.click_callback)
		self.add(self.drawing_area)

		self.set_title("Checkers")
		self.connect("delete-event", Gtk.main_quit)


		self.show_all()

	def click_callback(self, widget, event):
		print("foo")

	def on_draw(self, wid, cr):
		offset_x = 40
		offset_y = 40
		dot_size = 100

		def square(x, y):
			cr.set_source_rgba(0, 0, 0, 1)
			cr.set_line_width(dot_size)

			cr.set_line_cap(cairo.LINE_CAP_BUTT)
			cr.move_to(offset_x + x*dot_size +0, offset_y + y*dot_size + (dot_size/2))
			cr.line_to(offset_x + x*dot_size +dot_size, offset_y + y*dot_size + (dot_size/2))
			cr.stroke()

		def circle(x, y, col, type):
			cr.set_line_width(1)
			cr.set_source_rgba(0.1, 0.5, col, 1)
			cr.arc(offset_x + x*dot_size +dot_size/2, offset_y + y*dot_size + dot_size/2, dot_size/2, 0, 2*math.pi)
			cr.stroke_preserve()
			cr.fill()
			if(type == 1):
				cr.set_line_width(dot_size/10)
				cr.set_source_rgba(1.0, 1.0, 1.0, 1)
				cr.arc(offset_x + x*dot_size +dot_size/2, offset_y + y*dot_size + dot_size/2, dot_size/2.1, 0, 2*math.pi)
				cr.stroke()

		for x in range(0,EDGE_SIZE):
			for y in range(0, EDGE_SIZE):
				if (x + y) % 2 == 0:
					square(y, x)

		if self.board_state:
			for x in range(0, EDGE_SIZE):
				for y in range(0, EDGE_SIZE):
					if(type(self.board_state[x][y]) is Checker):
						circle(y, x, self.board_state[x][y].color, self.board_state[x][y].type)



class DisplayHelper:

	def __init__(self, q):
		self.q = q

	def main(self, q):
		self.app = BoardWindow(q)
		Gtk.main()

	def run(self):
		t = threading.Thread(target=self.main, args = (self.q,))
		t.daemon = True
		t.start()