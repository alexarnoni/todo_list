document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    
    forms.forEach(form => {
        form.addEventListener("submit", function () {
            showLoader();  // Exibe o loader antes de enviar o formulário
        });
    });
});

function showLoader() {
    let loader = document.createElement("div");
    loader.id = "loader";
    loader.innerHTML = "<div class='spinner'></div> Carregando...";
    document.body.appendChild(loader);
}

function hideLoader() {
    let loader = document.getElementById("loader");
    if (loader) loader.remove();
}

// Oculta o loader quando a página recarrega
window.onload = function () {
    hideLoader();
};
