(function() {
    // Этот код не кроссбраузерный, но, так как главная страница используется
    // на наших терминалах, подключенных к мониторам аэропорта,
    // считаю возможным пожертвовать кроссбраузерностью в пользу компактности,
    // допустив, что терминалы находятся под нашим управлением.
    document.addEventListener('DOMContentLoaded', function() {
        pasty = function() {
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("GET", "/one", false);
            xmlhttp.send();
            document.getElementById('wrapper').innerHTML = xmlhttp.responseText;
        }
        pasty();
        setInterval(pasty, 15000);
    })
})();