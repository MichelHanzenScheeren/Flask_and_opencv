from threading import Lock
from app.models.image_pack import ImagePack

PADRONIZED_HEIGHT = 480
PADRONIZED_WIDTH = 640
PADRONIZED_SIZE = (PADRONIZED_HEIGHT, PADRONIZED_WIDTH) # resolução que não precisa de redimensionamento
MAX_IMAGE_WIDTH = 720 # tamano máximo (idealizado) para a imagem na tela

class VideoCapture:
  def __init__(self):
    self._is_working = True
    self.video_capture = None
    self.lock_video = Lock()
    self.proporcional_size = PADRONIZED_SIZE
    print(self.proporcional_size)
    

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
      if h <= PADRONIZED_HEIGHT and w <= PADRONIZED_WIDTH:
        self.proporcional_size = (int(h), int(w))
      else:
        proportion = MAX_IMAGE_WIDTH / w
        self.proporcional_size = (int(h * proportion), int(w * proportion))


  def set_working_state(self, condition = True):
    with self.lock_video:
      self._is_working = condition
  

  def video_status(self):
    h, w = self.proporcional_size
    _ = self.capture_frame() # Necessário para verificação do funcionamento
    success = self.is_working()
    return {'style': f'height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;',
        'success': success}
  

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
    ok_width = self.video_capture.get(3) <= PADRONIZED_WIDTH
    ok_height = self.video_capture.get(4) <= PADRONIZED_HEIGHT
    if(ok_width and ok_height):
      return frame
    return ImagePack.resize_image(frame, self.proporcional_size)
  

  def change(self, new_port):
    try:
      return self._change_video(new_port)
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
