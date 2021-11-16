function myMap() {
    let mapOptions = {
        center: new google.maps.LatLng(51.5, -0.12),
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.HYBRID,
    };
    let map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
