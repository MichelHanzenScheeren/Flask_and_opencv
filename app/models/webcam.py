import time
from app.models.rectangle import Rectangle
from app.models.video_capture import VideoCapture
from app.models.image_pack import ImagePack
from app.models.frame import Frame


class Webcam():
  def __init__(self):
    self.current_port = 0
    self.rectangle = Rectangle()
    self.video_capture = VideoCapture()
    self.captured_frame = Frame()
    self.uploaded_frame = Frame()
  

  def init_webcam(self):
    self.video_capture.start_video(self.current_port)
  

  def video_status(self):
    h, w, success = self.video_capture.video_status()
    return {'style': f'height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;',
        'success': success, 'current': self.current_port}
  

  def webcans_list(self):
    list_webcans = []
    for index in range(100):
      if index == self.current_port:
        continue
      if not ImagePack.is_valid_webcam(index):
        break
      list_webcans.append(index)
    list_webcans.insert(self.current_port, self.current_port)
    return list_webcans


  def change_current_webcam(self, index):
    if self.is_invalid_index(index):
      return ''
    self.webcam_port = index
    return self.video_capture.change(index)
  

  def is_invalid_index(self, index):
    return index is None or (type(index) is not int) or index < 0


  def generate_images(self):
    try:
      yield from self._generate_images()
    except Exception as exception:
      print(exception)
  

  def _generate_images(self):
    FRAME_RATE, previous = 0.1, 0
    while True:
      img = self.get_image()
      if (time.time() - previous) > (FRAME_RATE):
        previous = time.time()
        yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
  

  def get_image(self):
    try:
      if(self.uploaded_frame.is_valid()):
        copy = self.uploaded_frame.get_copy()
      else:
        copy = self.get_webcam_image()
      return self.draw_and_convert_frame(copy)
    except:
      black = ImagePack.black_image(self.video_capture.proporcional_size)
      return ImagePack.convert_to_bytes(black)
  

  def get_webcam_image(self):
    frame = self.video_capture.capture_frame()
    self.captured_frame.set_frame(frame.copy())
    return frame
  

  def draw_and_convert_frame(self, copy):
    drawed_image = self.rectangle.draw_rectangle(copy)
    return ImagePack.convert_to_bytes(drawed_image)


  def get_differentiator_image(self):
    if(self.uploaded_frame.is_valid()):
      return self.crop_uploaded_image()
    return self.get_drawed_image()
  

  def crop_uploaded_image(self):
    copy = self.uploaded_frame.get_copy()
    self.uploaded_frame.clear()
    return self.rectangle.crop_image(copy)


  def get_drawed_image(self):
    copy = self.captured_frame.get_copy()
    return self.rectangle.crop_image(copy)
  

  def save_uploaded_image(self, image):
    try:
      self._save_uploaded_image(image)
    except:
      return ''
  

  def _save_uploaded_image(self, image):
    if image is None:
      return
    frame = ImagePack.convert_to_frame(image)
    dimensions = self.video_capture.proporcional_size
    new_image = ImagePack.resize_image(frame, dimensions)
    self.uploaded_frame.set_frame(new_image)
  

  def clear_rectangle_and_uploaded_image(self):
    self.rectangle.initial_points_of_rectangle()
    self.uploaded_frame.clear()
  

  def clear(self):
    self.turn_off_webcam()
    self.clear_rectangle_and_uploaded_image()
  

  def turn_off_webcam(self):
    self.video_capture.turn_off()


  def __del__(self):
    self.turn_off_webcam()
