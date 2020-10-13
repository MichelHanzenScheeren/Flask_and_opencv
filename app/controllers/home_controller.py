from flask import Response, render_template, redirect, url_for, request


def configure_routes(app, webcam):
  @app.route('/')
  @app.route('/index')
  @app.route('/home')
  def index():
    try:
      webcam.init_webcam()
      return render_template('index.html', page='index', 
          video_status=webcam.video_status_and_port(), webcans_list=webcam.webcans_list())
    except Exception as exception:
      print(exception)
      return redirect(url_for('error'))
  

  @app.route('/play_webcam')
  def play_webcam():
    return Response(webcam.generate_images(), mimetype='multipart/x-mixed-replace; boundary=frame')


  @app.route('/upload_image', methods = ['POST'])
  def upload_image():
    webcam.save_uploaded_image(request.files["file"])
    return ''


  @app.route('/get_measures', methods = ['POST'])
  @app.route('/get_measures/<int:x1>/<int:y1>/<int:x2>/<int:y2>', methods = ['POST'])
  def get_measures(x1=None, y1=None, x2=None, y2=None):
    webcam.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
    return ''


  @app.route('/clear_rectangle', methods=['POST'])
  def clear_rectangle():
    webcam.clear_rectangle_and_uploaded_image()
    return ''
  

  @app.route('/change_current_webcam', methods = ['POST'])
  @app.route('/change_current_webcam/<int:index_webcam>', methods = ['POST'])
  def change_current_webcam(index_webcam=None):
    return webcam.change_current_webcam(index_webcam)
  
