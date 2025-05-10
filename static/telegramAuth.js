// Espera o WebApp do Telegram estar pronto e faz a validação no seu backend
function initTelegramAuth(onSuccess, onError) {
    // Informa que o WebApp está pronto para uso
    Telegram.WebApp.ready();
  
    // Dados que o Telegram injetou
    const initData = Telegram.WebApp.initData;               // string completa
    const hash     = Telegram.WebApp.initDataUnsafe.hash;    // hash fornecido
  
    // Chama seu endpoint de validação
    fetch('/validate_webapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ init_data: initData, hash })
    })
    .then(res => {
      if (!res.ok) throw new Error('Não autorizado');
      return res.json();
    })
    .then(payload => {
      if (payload.valid) {
        onSuccess();
      } else {
        throw new Error('Hash inválido');
      }
    })
    .catch(err => {
      console.error(err);
      if (typeof onError === 'function') {
        onError(err);
      } else {
        document.body.innerHTML = '<h1 style="color:red;text-align:center;margin-top:40vh;">⚠️ Acesso negado.</h1>';
      }
    });
  }
  