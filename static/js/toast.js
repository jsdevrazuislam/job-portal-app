
window.showToast = function(message, type = "info") {
    const toastContainerId = "toast-container";
    let toastContainer = document.getElementById(toastContainerId);

    if (!toastContainer) {
        toastContainer = document.createElement("div");
        toastContainer.id = toastContainerId;
        toastContainer.className = "fixed top-4 right-4 z-50 space-y-2";
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type} bg-white border shadow rounded px-4 py-2 flex items-center justify-between gap-4`;
    toast.innerHTML = `
        <span>${message}</span>
        <button class="text-gray-500 hover:text-red-500" onclick="this.parentElement.remove()">×</button>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}
