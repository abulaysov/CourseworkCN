document.addEventListener('DOMContentLoaded', function () {

    const sendButton = document.querySelector("[name=send_button]");
    let name = document.getElementById('name');
    let temp = document.getElementById('temp');
    let weather = document.getElementById('weather');
    let wind_speed = document.getElementById('wind_speed');
    let wind_deg = document.getElementById('wind_deg');
    let humidity = document.getElementById('humidity');
    let last_update = document.getElementById('last_update');
    let city_name = document.getElementById('city_name');

    const websocketClient = new WebSocket("ws://172.20.10.2:8001")

    websocketClient.onopen = () => {
        websocketClient.send("Hello")

        sendButton.onclick = () => {
            websocketClient.send(city_name.value)
            city_name.value = ""
        };

        websocketClient.onmessage = (message) => {
            let data = JSON.parse(message.data);
            console.log(data)

            if (typeof name.textContent !== "undefined") {
                name.textContent = `City: ${data.name}`;
            } else {
                name.innerText = 'an error has occurred';
            }
            name.innetHTML = '<p>data.name</p>'

            if (typeof temp.textContent !== "undefined") {
                temp.textContent = `Temp: ${data.temp}`;
            } else {
                temp.innerText = 'an error has occurred';
            }
            temp.innetHTML = '<p>data.temp</p>'

            if (typeof weather.textContent !== "undefined") {
                weather.textContent = `Weather: ${data.weather}`;
            } else {
                weather.innerText = 'an error has occurred';
            }
            weather.innetHTML = '<p>data.weather</p>'

            if (typeof wind_speed.textContent !== "undefined") {
                wind_speed.textContent = `Wind speed: ${data.wind_speed}`;
            } else {
                wind_speed.innerText = 'an error has occurred';
            }
            wind_speed.innetHTML = '<p>data.wind_speed</p>'

            if (typeof wind_deg.textContent !== "undefined") {
                wind_deg.textContent = `Wind deg: ${data.wind_deg}`;
            } else {
                wind_deg.innerText = 'an error has occurred';
            }
            wind_deg.innetHTML = '<p>data.wind_deg</p>'

            if (typeof humidity.textContent !== "undefined") {
                humidity.textContent = `Humidity: ${data.humidity}`;
            } else {
                humidity.innerText = 'an error has occurred';
            }
            humidity.innetHTML = '<p>data.humidity</p>'

            if (typeof last_update.textContent !== "undefined") {
                last_update.textContent = `Last update: ${data.last_update}`;
            } else {
                last_update.innerText = 'an error has occurred';
            }
            last_update.innetHTML = '<p>data.last_update</p>'

        }
    };


}, false);



