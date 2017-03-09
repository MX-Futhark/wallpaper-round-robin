from wprr import screenutils
import sys, os
from PIL import Image, ImageOps

class WallpaperGenerator:
	"""Class to generate wallpapers based on a given configuration."""

	valid_extensions = ['.png', '.jpg', '.jpeg']

	def __init__(self, args):
		"""Constructor based on the configuration obtained through parsing arguments."""

		self.__dict__.update(args.__dict__)

		self.screens = eval(args.screens) or screenutils.get_screens()

		if self.method == "gallery":
			if len(self.inputs) != 1:
				raise Exception("--method=gallery accepts only one input directory.")
		else:
			if len(self.inputs) != len(self.screens):
				raise Exception((
					"There must be as many input directories as there are screens "
					"for --method=round_robin or --method=one_to_one."
				))

		# sort from left to right, top to bottom
		self.screens.sort(key=lambda k: (k[1], k[0]))

		self.w_min, self.h_min, self.w_max, self.h_max = sys.maxsize, sys.maxsize, 0, 0
		for m in self.screens:
			self.w_min = min(self.w_min, m[0])
			self.h_min = min(self.h_min, m[1])
			self.w_max = max(self.w_max, m[2])
			self.h_max = max(self.h_max, m[3])

		self.bounds = [self.w_min , self.h_min, self.w_max, self.h_max]
		self.target_size = self.__rectangle_to_size(self.bounds)

		self.img_dirs = []
		for dir in args.inputs:
			files = os.listdir("./{}".format(dir))
			images = filter(lambda n: n.lower().endswith(tuple(WallpaperGenerator.valid_extensions)), files)
			self.img_dirs.append(list(images))


	def __rectangle_to_size(self, rect):
		return (rect[2] - rect[0], rect[3] - rect[1])


	def __rectangle_to_offset(self, rect):
		return (rect[0] - self.w_min, rect[1] - self.h_min)


	def __paste_to_result(self, res_img, img_path, screen):
		size = self.__rectangle_to_size(screen)
		img = ImageOps.fit(Image.open(img_path), size, Image.ANTIALIAS)
		res_img.paste(img, self.__rectangle_to_offset(screen))


	def __save_img(self, img, index):

		if not os.path.exists(self.output):
			os.makedirs(self.output)

		# TODO: handle path building properly
		img.save(
			os.path.abspath(("{}/" + self.name + ".{}").format(self.output, index, self.format)),
			quality=self.quality, optimize=True
		)


	def __make_wallpaper(self, target_img, method, image_indices):

		def get_img_in_one_dir(image_index):
			return self.img_dirs[0][(image_indices[0] + image_index) % len(self.img_dirs[0])]

		def get_img_in_all_dirs(dir_index):
			return self.img_dirs[dir_index][image_indices[dir_index]]

		make_gallery = method == "gallery"

		for i in range(0, len(self.screens)):
			dir_name = self.inputs[0 if make_gallery else i]
			img_file_name = get_img_in_one_dir(i) if make_gallery else get_img_in_all_dirs(i)
			path = os.path.abspath("{}/{}".format(dir_name, img_file_name))
			self.__paste_to_result(target_img, path, self.screens[i])


	def round_robin(self):
		"""Applies the round_robin generation method."""

		current_image_indices = [0] * len(self.screens)
		counter = 0
		increment_dir_index = 0

		while True:
			wallpaper = Image.new('RGB', self.target_size)

			self.__make_wallpaper(wallpaper, "round_robin", current_image_indices)
			self.__save_img(wallpaper, counter)
			counter += 1

			current_image_indices[increment_dir_index] = (current_image_indices[increment_dir_index] + 1) % len(self.img_dirs[increment_dir_index])
			increment_dir_index = (increment_dir_index + 1) % len(current_image_indices)

			if current_image_indices == [0, 0] and increment_dir_index == 0:
				break


	def gallery(self):
		"""Applies the gallery generation method."""

		current_image_index = 0
		img_dir = self.img_dirs[0]

		while True:
			wallpaper = Image.new('RGB', self.target_size)

			self.__make_wallpaper(wallpaper, "gallery", [current_image_index])
			self.__save_img(wallpaper, current_image_index)

			current_image_index = (current_image_index + 1) % len(img_dir)

			if current_image_index == 0:
				break;


	def one_to_one(self):
		"""Applies the one_to_one generation method."""

		current_image_indices = [0] * len(self.screens)
		counter = 0

		while True:
			wallpaper = Image.new('RGB', self.target_size)

			self.__make_wallpaper(wallpaper, "one_to_one", current_image_indices)
			self.__save_img(wallpaper, counter)
			counter += 1

			for i in range(0, len(current_image_indices)):
				current_image_indices[i] = (current_image_indices[i] + 1) % len(self.img_dirs[i])

			if current_image_indices == [0, 0]:
				break


	def apply(self):
		"""Applies the generation method given in argument."""
		getattr(self, self.method)()
