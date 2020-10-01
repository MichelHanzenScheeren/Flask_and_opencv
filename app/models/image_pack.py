import cv2.cv2 as cv2
import numpy


class ImagePack():
	@staticmethod
	def new_stream(port):
		return cv2.VideoCapture(port)
	

	@staticmethod
	def is_valid_webcam(test_port):
		video = ImagePack.new_stream(test_port)
		return not (video is None or not video.isOpened())
				

	@staticmethod
	def draw_rectangle(frame, initial_xy, final_xy):
		red_color = (0, 0, 255) # formato bgr (no lugar de rgb)
		cv2.rectangle(frame, initial_xy, final_xy, red_color, thickness = 1)


	@staticmethod
	def convert_to_bytes(image):
		return ImagePack.encode_to_jpg(image).tobytes()


	@staticmethod
	def encode_to_jpg(image):
		return cv2.imencode('.jpg', image)[1]
	

	@staticmethod
	def convert_to_frame(image):
		numpy_img = numpy.fromstring(image.read(), numpy.uint8)
		cv2_image = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
		return cv2_image
	

	@staticmethod
	def resize_image(image, dimensions):
		h, w = dimensions
		return cv2.resize(image, (w, h))
	

	@staticmethod
	def force_max_resolution(video):
		video.set(cv2.CAP_PROP_FRAME_WIDTH, 10000) # forçar resolução máxima 
		video.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000) # forçar resolução máxima 
		print(f'MAX_RESOLUTION: {int(video.get(3))} X {int(video.get(4))}')
		return (video.get(4), video.get(3))
	

	@staticmethod
	def black_image(size):
		h, w = size
		return numpy.zeros((h, w, 3), numpy.uint8)
	

	@staticmethod
	def validate_image(image):
		return isinstance(image, numpy.ndarray)
