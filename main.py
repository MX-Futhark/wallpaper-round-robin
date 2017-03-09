import argparse
from wprr import wallpaper_generator

parser = argparse.ArgumentParser()
parser.add_argument(
	"-m", "--method", default="round_robin", choices=["round_robin", "one_to_one", "gallery"],
	help="""
		The wallpaper generation method. 
		round_robin: each new wallpaper changes by one image, screen by screen; 
		one_to_one: chooses a new image from each input directory to make the wallpaper; 
		gallery: multiscreen image slideshow using the images of only one input directory.
	""")
parser.add_argument(
	"-s", "--screens", default='[]',
	help="""
		A python list of lists describing the screens for which the wallpapers must be generated. 
		If not set, it defaults to the screens of the computer on which this script is run. 
		The following syntax is as follows: [[topleft_x, topleft_y, bottomright_x, bottomright_y], [...], ...
	""")
parser.add_argument(
	"-o", "--output", default="output",
	help="Where to put the resulting wallpapers.")
parser.add_argument(
	"-i", "--inputs", nargs='+', required='true',
	help="""
		The directories containing the input images. 
		Must contain one element for --method=gallery 
		and as many elements as there are screens for the other methods. 
		The order must correspond to the orders of the screens ordered from left to right, top to bottom.
	""")
parser.add_argument(
	"-n", "--name", default='{:09d}',
	help="The python3-like format of the name of the generated wallpapers. Takes an integer.")
parser.add_argument(
	"-f", "--format", default='png',
	help="The format of the generated wallpapers.")
parser.add_argument(
	"-q", "--quality", default='85', type=int,
	help="The quality of the generated in percent if --format=jpg.")
args = parser.parse_args()


if __name__ == '__main__':
	wallpaper_generator.WallpaperGenerator(args).apply()
