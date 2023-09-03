// Função para abrir o pop-up
function abrirPopup() {
    document.getElementById("popup").style.display = "block";
}

// Função para fechar o pop-up
function fecharPopup() {
    document.getElementById("popup").style.display = "none";
}

// Evento para abrir o pop-up quando a página carregar
window.onload = abrirPopup;

// Evento para fechar o pop-up quando o formulário for enviado
document.getElementById("email-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Evita o envio padrão do formulário
    fecharPopup(); // Fecha o pop-up
    // Você pode adicionar código adicional aqui para processar o formulário
});
