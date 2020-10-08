from flask import Response, render_template, redirect, url_for, request


def configure_routes(app, webcam, analyze):
  @app.route('/get_differentiator', methods=['POST'])
  def get_differentiator():
    analyze.clear()
    return analyze.calculate_differentiator(webcam.get_differentiator_image)
  

  @app.route('/get_differentiator_image', methods=['POST'])
  def get_differentiator_image():
    return Response(analyze.results.get_differentiator_image())


  @app.route('/start_analysis', methods=['POST'])
  def start_analysis():
    try:
      form = request.form
      time, qtd, description = form['time'], form['qtd'], form['description']
      analyze.start_analyze(time, qtd, description, webcam.get_differentiator_image)
      webcam.clear()
      return redirect(url_for('results'))
    except:
      return redirect(url_for('error'))


  @app.route('/results')
  def results():
    try:
      return render_template('results.html', results = analyze.results, page='results')
    except:
      return redirect(url_for('error'))
  

  @app.route('/get_all_images', methods=['POST'])
  def get_all_images():
    zip_file = analyze.results.get_all_images()
    headers = {'content-type': 'application/zip', 'format': 'base64', 'file-name': 'imagens.zip'}
    return Response(zip_file, headers = headers)
  

  @app.route('/get_xlsx_results', methods=['POST'])
  def get_xlsx_results():
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    headers = {'content-type': content_type, 'format': 'base64', 'file-name': 'resultados.xlsx'}
    return Response(analyze.results.get_xlsx_results(), headers = headers)
