const formElement = document.querySelector(".form");
const modalWrapper = document.createElement("div");
modalWrapper.id = "modal-wrapper";
modalWrapper.style.display = "none";
modalWrapper.style.position = "fixed";
modalWrapper.style.zIndex = "1000";
modalWrapper.style.left = "0";
modalWrapper.style.top = "0";
modalWrapper.style.width = "100%";
modalWrapper.style.height = "100%";
modalWrapper.style.overflow = "auto";
modalWrapper.style.backgroundColor = "rgba(0,0,0,0.6)";
modalWrapper.style.paddingTop = "50px";

const modalContent = document.createElement("div");
modalContent.style.backgroundColor = "#fff";
modalContent.style.margin = "auto";
modalContent.style.padding = "20px";
modalContent.style.borderRadius = "10px";
modalContent.style.width = "300px";
modalContent.style.position = "relative";
modalContent.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";

modalContent.appendChild(formElement);
modalWrapper.appendChild(modalContent);
document.body.appendChild(modalWrapper);

const closeButton = document.querySelector(".close-button");
const alertaButtons = document.querySelectorAll(".button-carrinho");

// Função para criar a notificação toast no canto inferior direito
function createToastNotification() {
  const notification = document.createElement("div");
  notification.className = "notifications-container";
  notification.style.position = "fixed";
  notification.style.bottom = "20px";
  notification.style.right = "20px";
  notification.style.background = "#e6f7ff";
  notification.style.padding = "15px";
  notification.style.borderRadius = "8px";
  notification.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
  notification.style.display = "flex";
  notification.style.alignItems = "center";
  notification.style.zIndex = "2000";
  notification.innerHTML = `
        <div class="info" style="display: flex; align-items: center;">
          <div class="flex-shrink-0" style="margin-right: 10px;">
            <svg class="info-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="24" height="24" aria-hidden="true">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div class="info-prompt-wrap">
            <p style="margin: 0; font-size: 14px;">
              Alerta criado com sucesso!
            </p>
          </div>
        </div>
      `;
  document.body.appendChild(notification);

  // Remove automaticamente após 3 segundos
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

alertaButtons.forEach((button) => {
  button.addEventListener("click", () => {
    modalWrapper.style.display = "block";
  });
});

closeButton.addEventListener("click", () => {
  modalWrapper.style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target === modalWrapper) {
    modalWrapper.style.display = "none";
  }
});

// Escutar o envio do formulário
formElement.addEventListener("submit", (e) => {
  e.preventDefault(); // impede reload
  modalWrapper.style.display = "none"; // fecha o modal
  createToastNotification(); // mostra o aviso no canto
});
