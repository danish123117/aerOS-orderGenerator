document.addEventListener("DOMContentLoaded", function () {
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const orderSelect = document.getElementById("order-frequency");
    const orderContainer = document.getElementById("order-container");

    let eventSource = null;

    startBtn.addEventListener("click", function () {
        const selectedFrequency = orderSelect.value;
        fetch("/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ frequency: selectedFrequency })
        }).then(response => {
            if (response.ok) {
                startBtn.disabled = true;
                stopBtn.disabled = false;
                orderSelect.disabled = true;
                startLiveUpdates();
            }
        });
    });

    stopBtn.addEventListener("click", function () {
        fetch("/stop", { method: "POST" }).then(response => {
            if (response.ok) {
                startBtn.disabled = false;
                stopBtn.disabled = true;
                orderSelect.disabled = false;
                stopLiveUpdates();
            }
        });
    });

    function startLiveUpdates() {
        if (eventSource) eventSource.close();
        eventSource = new EventSource("/stream");
        eventSource.onmessage = function (event) {
            const orderElement = document.createElement("p");
            orderElement.textContent = event.data;
            orderContainer.appendChild(orderElement);

            // Keep only the latest 3 orders
            while (orderContainer.children.length > 1) {
                orderContainer.removeChild(orderContainer.firstChild);
            }
        };
    }

    function stopLiveUpdates() {
        if (eventSource) {
            eventSource.close();
            eventSource = null;
        }
    }
});
