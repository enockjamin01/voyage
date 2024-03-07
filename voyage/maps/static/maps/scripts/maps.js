var accessToken='<ADD YOUR MAPBOX TOKEN HERE>'
mapboxgl.accessToken = accessToken;
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    projection:'globe',
    zoom: 15,
    center: [77.6040276,12.9747819]
});

map.on('style.load', () => {
    map.setFog({});
})

const nav = new mapboxgl.NavigationControl({
    showCompass: false
});
map.addControl(nav, 'bottom-right');

map.addControl(
    new MapboxGeocoder({
        accessToken: accessToken,
        mapboxgl: mapboxgl,
        placeholder: "Search Your Next Trip",
        marker: true,
    })
)

var coordinates = { coordinates:[] }
var markers = []
var markerToRemove = undefined

function onSavedCoordinatesFetched() {
    console.log(document.getElementById("savedcoordinates").value)
}


map.on('click', (event) => {
    var coordinate = event.lngLat;
    var markerExists = markers.find(function (marker) {
        if (marker.getLngLat()['lng'] == coordinate['lng'] && marker.getLngLat()['lat'] == coordinate['lat']) {
            markerToRemove = marker
            return true
        } else {
            return false
        }
    })
    if (markerExists) {
            coordinates.coordinates.pop(markerToRemove.getLngLat())
            markerToRemove.remove()
            markers.pop(markerToRemove)
        document.getElementById("coordinatesInput").value = JSON.stringify(coordinates)
        } else {
        var marker = new mapboxgl.Marker(
            {
                    color:'red'
            }
            ).setLngLat(coordinate).addTo(map)
        markers.push(marker)
        coordinates.coordinates.push(marker.getLngLat())
        document.getElementById("coordinatesInput").value = JSON.stringify(coordinates)
    }
});


function optionHandling() {
    alert("Hi")
}