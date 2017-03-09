import ctypes, platform

# taken from http://code.activestate.com/recipes/460509-get-the-actual-and-usable-sizes-of-all-the-screen/

class RECT(ctypes.Structure):

	_fields_ = [
		('left', ctypes.c_long),
		('top', ctypes.c_long),
		('right', ctypes.c_long),
		('bottom', ctypes.c_long)]

	def dump(self):
		return list(map(int, (self.left, self.top, self.right, self.bottom)))


#TODO: pydoc
def get_screens():
	"""Finds and returns the positions of the current screens."""

	if platform.system() != "Windows":
		raise Exception("get_screens is not supported on OSes other than Windows.")

	user = ctypes.windll.user32

	resolutions = []
	CBFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)

	def cb(hscreen, hdcscreen, lprcscreen, dwData):
		r = lprcscreen.contents
		resolutions.append(r.dump())
		return 1

	cbfunc = CBFUNC(cb)
	temp = user.EnumDisplayMonitors(0, 0, cbfunc, 0)

	return resolutions
