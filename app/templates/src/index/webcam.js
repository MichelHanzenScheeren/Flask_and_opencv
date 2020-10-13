
window.addEventListener('pageshow', function(_) {
  try {
    const entries = performance.getEntriesByType("navigation");
    if(entries.map(nav => nav.type)[0] == "back_forward") {
      location.reload();
    }
  } catch (_) {}
}); // Atualizar pagina quando voltar dos resultados (para ativar webcam)

(() => {
  defineImageStyle('{{ video_status["style"] }}');
  validateWebcam();
  addEventToChangeWebcam();
}) () // Função auto-executada

function defineImageStyle(style) {
  document.getElementById('frameImg').style = style;
  leftDivHeigth = document.getElementById('div-items-left').offsetHeight ;
  document.getElementById('div-items-rigth').style.minHeight = `${leftDivHeigth}px`;
}

function validateWebcam() {
  let got_image = ('{{ video_status["success"] }}');
  if(got_image == 'False') {
    messageInvalidWebcam();
  }
} // validação inicial de funcionamento da webcam

function messageInvalidWebcam() {
  title = 'Problemas para configurar sua webcam &#128533;'
  body = `Infelizmente, não conseguimos obter imagens da sua webcam. 
      Por favor, verifique se a mesma está instalada e disponível para uso...`
  complement = `<button type="button" class="btn btn-lg btn-block btn-dark" onclick="location.reload();">
      Tentar novamente </button>`
  showMessage(title, body, complement);
}

function addEventToChangeWebcam() {
  document.getElementById('selectCurrentWebcam').setAttribute('onchange', 'changeCurrentWebcam()');
}

async function changeCurrentWebcam () {
  try {
    let select = document.getElementById('selectCurrentWebcam');
    let response = await axios.post(`{{url_for("change_current_webcam")}}/${select.value}`);
    console.log(response);
    if(response == '' || response.data['success'] == false) {
      messageInvalidWebcam();
    } else {
      defineImageStyle(response.data['style']);
      $('#my-toast').remove();
    }
  } catch (error) {
    showErrorMessage(error);
  }
}
