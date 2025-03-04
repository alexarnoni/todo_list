function showNotification(message, type = "success") {
    const notificationContainer = document.getElementById("notification-container");

    const notification = document.createElement("div");
    notification.classList.add("notification", type);
    notification.innerText = message;

    notificationContainer.appendChild(notification);

    setTimeout(() => {
        notification.classList.add("fade-out");
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

// Captura as mensagens Django automaticamente
document.addEventListener("DOMContentLoaded", function () {
    const messageContainer = document.getElementById("django-messages");
    if (messageContainer) {
        const messages = messageContainer.getElementsByClassName("django-message");
        for (let msg of messages) {
            const messageType = msg.dataset.type || "success";
            showNotification(msg.innerText, messageType);
        }
        messageContainer.remove();
    }
});

function fadeOutAndRemove(element) {
    element.style.transition = "opacity 0.5s";
    element.style.opacity = "0";
    setTimeout(() => element.remove(), 500);
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
                let taskElement = this.closest(".task");
                fadeOutAndRemove(taskElement);
                window.location.href = this.getAttribute("href");
            }
        });
    });
});

