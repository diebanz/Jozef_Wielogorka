function myMap() {
    const store = { lat: 51.5, lng: -0.12 };
    let mapOptions = {
        center: store,
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.HYBRID,
    };
    let map = new google.maps.Map(document.getElementById("map"), mapOptions);
    const marker = new google.maps.Marker({
        position: store,
        map: map,
      });    
}
