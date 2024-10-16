document.addEventListener("DOMContentLoaded", function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;

            API_KEY = '9b81a23818624d17a88c17c066ba6e10';
            // Llamada a la API de geocodificación inversa de OpenCage
            var geocodeUrl = `https://api.opencagedata.com/geocode/v1/json?q=${latitude}+${longitude}&key=${API_KEY}`;

            fetch(geocodeUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.status.code === 200) {
                        var address = data.results[0].formatted;
                        document.getElementById('address').value = address;
                    } else {
                        console.error("Error al obtener la dirección: ", data.status.message);
                    }
                })
                .catch(error => console.error("Error al llamar a la API de geocodificación: ", error));
        }, function(error) {
            console.error("Error obteniendo la ubicación: ", error);
        });
    } else {
        console.error("La geolocalización no es soportada por este navegador.");
    }
});
