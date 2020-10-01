from threading import Lock
from app.models.image_pack import ImagePack


class VideoCapture:
  def __init__(self):
    self._is_working = True
    self.video_capture = None
    self.lock_video = Lock()
    self.proporcional_size = [480, 640]
  

  def start_video(self, port):
    if not self.is_valid() or not self.is_working():
      self.start_video_stream(port)
      self.define_resolution()
      self.set_working_state(True)
  

  def is_valid(self):
    with self.lock_video:
      return self.video_capture and self.video_capture.isOpened()
  

  def is_working(self):
    with self.lock_video:
      return self._is_working
  

  def start_video_stream(self, port):
    with self.lock_video:
      self.video_capture = ImagePack.new_stream(port)


  def define_resolution(self):
    with self.lock_video:
      h, w = ImagePack.force_max_resolution(self.video_capture)
      if h <= 480 and w <= 640:
        return
      proportion = 720 / w
      self.proporcional_size = (int(h * proportion), int(w * proportion))


  def set_working_state(self, condition = True):
    with self.lock_video:
      self._is_working = condition
  

  def video_status(self):
    h, w = self.proporcional_size
    _ = self.capture_frame() # Necessário para verificação do funcionamento
    success = self.is_working()
    return (h, w, success)
  

  def capture_frame(self):
    if(self.is_working() and self.is_valid()):
      return self._do_capture()
    return ImagePack.black_image(self.proporcional_size)
  

  def _do_capture(self):
    with self.lock_video:
      success, frame = self.video_capture.read()
    self.set_working_state(success)
    if success:
      return self._resize_capture(frame) 
    else:
      return ImagePack.black_image(self.proporcional_size)
  

  def _resize_capture(self, frame):
    if(self.video_capture.get(3) <= 640 and self.video_capture.get(4) <= 480):
      return frame
    return ImagePack.resize_image(frame, self.proporcional_size)


  def change(self, new_port):
    try:
      _change_video(new_port)
    except:
      return ''
  

  def _change_video(self, new_port):
    with self.lock_video:
      to_free = self.video_capture
      self.video_capture = None
    self.start_video(new_port)
    to_free.release()
    return self.video_status()
  

  def turn_off(self):
    with self.lock_video:
      if self.video_capture:
        self.video_capture.release()
        self.video_capture = None
