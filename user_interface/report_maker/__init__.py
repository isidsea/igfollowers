# Out of the relative import
# This import happens bacause the software cannot find the relative part
from lib.reporting.cross_followers import Engine as CFEngine
from lib.engine.aggregator         import Engine as AggregatorEngine

from ..lib.state_manager import StateManager
from multiprocessing	 import Process
import urwid
import asyncio
import time

class UI(object):
	def __init__(self):
		self.state_manager = StateManager()
		self.state_manager.add_state(key="loading", value=None)

		self.async_loop = asyncio.get_event_loop()
		self.palette 	= [
			("reversed", "standout", ""),
		]

	def loading(self, number_of_dots=0):
		number_of_dots    = 0 if number_of_dots >= 5 else number_of_dots
		text 		      = "Loading{}".format(".".join(["" for a in range(number_of_dots)]))
		txt_loading       = urwid.Text(text)
		loading_container = urwid.Filler(txt_loading, "middle")
		container         = self.state_manager.get_global_var("dialog")
		container.contents.update({"body":(loading_container, None)})

		loading = self.state_manager.get_state(key="loading")
		if loading or loading is None:
			self.async_loop.call_later(0.1, self.loading, number_of_dots + 1)
		else:
			txt_loading.set_text("Finished!")
	#end def

	def _do_make_cf(self):
		self.state_manager.update_state(key="loading", value=True)
		# For cross followers engine, we need to aggregate the user first before making a report
		aggregator = AggregatorEngine()
		aggregator.aggregate_user()

		cf_engine = CFEngine()
		cf_engine.generate()
		self.state_manager.update_state(key="loading", value=False)

	def _make_cf(self, button):
		p = Process(target=self._do_make_cf)
		p.start()			
		self.loading()

	def _quit(self, button):
		raise urwid.ExitMainLoop()

	def show(self):
		txt_header = urwid.Text("Report Maker")
		header 	   = urwid.Pile([urwid.Divider(), txt_header, urwid.Divider()])

		btn_make_cf = urwid.Button("Cross Follower", on_press=self._make_cf)
		btn_quit	= urwid.Button("Quit", on_press=self._quit)
		btn_make_cf = urwid.AttrMap(btn_make_cf, None, focus_map="reversed")
		btn_quit	= urwid.AttrMap(btn_quit, None, focus_map="reversed")		
		menu        = [btn_make_cf, btn_quit]
		body	    = urwid.ListBox(urwid.SimpleFocusListWalker(menu))

		dialog = urwid.Frame(
			header = header,
			  body = body,
			footer = None
		)

		# Make dialog as a global variable, because we need to use this dialog to make a modification
		self.state_manager.add_global_var(key="dialog", value=dialog)

		app = urwid.Overlay(
			top_w = dialog,
			bottom_w = urwid.SolidFill(" "),
			width = ("relative",15),
			height = ("relative",20),
			align = "center",
			valign = "middle"
		)
		main_loop = urwid.MainLoop(
			app,
			event_loop = urwid.AsyncioEventLoop(loop=self.async_loop),
			palette = self.palette
		)
		main_loop.run()