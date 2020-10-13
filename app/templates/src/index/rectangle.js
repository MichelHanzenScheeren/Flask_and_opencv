const htmlXY = {
  x1: document.getElementById('x1'),
  y1: document.getElementById('y1'),
  x2: document.getElementById('x2'),
  y2: document.getElementById('y2'),
}
const rect = {};
let drag = false;

(function initRectangle() {
  var desenho = document.getElementById('frameImg');
  desenho.addEventListener('mousedown', mouseDown, false);
  desenho.addEventListener('mouseup', mouseUp, false);
  desenho.addEventListener('mousemove', mouseMove, false);
  desenho.addEventListener('mouseleave', mouseLeave, false);
  document.getElementById('refreshRectangleButton').onclick = refreshRectangle;
  document.getElementById('clearRectangleButton').onclick = clearRectangle;
}) ();

function mouseDown(e) {
  drag = true;
  rect.startX = e.pageX - this.offsetLeft;
  rect.startY = e.pageY - this.offsetTop;
  htmlXY.x1.value = rect.startX;
  htmlXY.y1.value = rect.startY;
}

function mouseMove(e) {
  if (drag) {
    rect.w = (e.pageX - this.offsetLeft) - rect.startX;
    rect.h = (e.pageY - this.offsetTop) - rect.startY;
    htmlXY.x2.value = rect.startX + rect.w;
    htmlXY.y2.value = rect.startY + rect.h;
  }
}

function mouseUp() {
  if(drag) {
    drag = false;
    draw();
    clearAuxValues();
  }
}

function mouseLeave(e) {
  drag = false;
  clearAuxValues();
}

function clearAuxValues() {
  rect.startX = 0;
  rect.startY = 0;
  rect.w = 0;
  rect.h = 0;
}

function draw() {
  try {
    parseIntValues();
    let invalid_values = rect.w == NaN || rect.h == NaN;
    let invalid_width = (rect.startX - (rect.startX + rect.w)) == 0;
    let invalid_height = (rect.startY - (rect.startY + rect.h)) == 0;
    if(invalid_values || invalid_width || invalid_height) {
      invalidRectangle();
    } else {
      let url = '{{url_for("get_measures")}}';
      let finalX = rect.startX + rect.w;
      let finalY = rect.startY + rect.h;
      axios.post(`${url}/${rect.startX}/${rect.startY}/${finalX}/${finalY}`);
  }
  } catch (error) {
    showErrorMessage(error);
  }
}

function parseIntValues() {
  rect.startX = parseInt(rect.startX);
  rect.startY = parseInt(rect.startY);
  rect.w = parseInt(rect.w);
  rect.h = parseInt(rect.h);
}

function clearRectangle(){
  try {
    axios.post('{{ url_for("clear_rectangle") }}');
    document.getElementById('uploadImageLabel').innerHTML = 'Escolher imagem local';
    htmlXY.x1.value = 0;
    htmlXY.x2.value = 0;
    htmlXY.y1.value = 0;
    htmlXY.y2.value = 0;
  } catch (error) {
    showErrorMessage(error);
  }
}

function refreshRectangle(){
  try {
    let x1 = parseInt(htmlXY.x1.value);
    let y1 = parseInt(htmlXY.y1.value);
    let x2 = parseInt(htmlXY.x2.value);
    let y2 = parseInt(htmlXY.y2.value);
    let x_is_int = htmlXY.x1.value == x1 && htmlXY.x2.value == x2;
    let y_is_int = htmlXY.y1.value == y1 && htmlXY.y2.value == y2;
    let not_empty_area = ((x1 - x2) != 0) && ((y1 - y2) != 0);
    let gretter_than_zero = x1 >= 0 && y1 >= 0 && x2 >= 0 && y2 >= 0;
    if(x_is_int && y_is_int && not_empty_area && gretter_than_zero) {
      axios.post(`{{url_for("get_measures")}}/${x1}/${y1}/${x2}/${y2}`);
    } else {
      invalidRectangle();
    }
  } catch (error) {
    showErrorMessage(error);
  }
}

function invalidRectangle() {
  let title = 'Retângulo inválido &#128533;';
  let body = 'Verifique os valores inseridos e tente novamente...';
  showMessage(title, body, undefined, true);
}

