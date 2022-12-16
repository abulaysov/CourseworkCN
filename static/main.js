document.addEventListener('DOMContentLoaded', function () {

    const messagesButton = document.querySelector("[name=send_button]");

    const websocketClient = new WebSocket("ws://localhost:8001")

    websocketClient.onopen = () => {
        websocketClient.send("Hello")

        messagesButton.onclick = () => {
            websocketClient.send("Click")
        };
    };

    websocketClient.onmessage = (message) => {
        let data = JSON.parse(message.data)
        console.log(data.hello)
    }

}, false);
