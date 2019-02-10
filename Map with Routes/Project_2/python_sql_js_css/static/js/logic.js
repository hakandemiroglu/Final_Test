//console.log(data)
var API_KEY = "pk.eyJ1IjoibWVyeWVtbWxrIiwiYSI6ImNqcHVkanVhbjBmcTM0M282MmowcnJlZ3AifQ.jpDXpNPhKT8vC9vCj6-UrQ";

// Adding tile layer
var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
});

var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
});


//var roughtmap = L.Routing.control({
    //waypoints: [
      //  L.latLng(57.74, 11.94),
      //  L.latLng(57.6792, 11.949)
    //],
    //routeWhileDragging: true
//}).addTo(map);



// Initialize all of the LayerGroups we'll be using
var layers = {
  UBER_POOL: new L.LayerGroup(),
  UBER_X: new L.LayerGroup(),
  UBER_XL: new L.LayerGroup(),
  SELECT: new L.LayerGroup(),
  BLACK: new L.LayerGroup(),
  BLACK_SUV: new L.LayerGroup(),
  Places: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map", {
  center: [33.767693,-84.4908152],
  zoom: 12,
  layers: [
    layers.UBER_POOL,
    layers.UBER_X,
    layers.UBER_XL,
    layers.SELECT,
    layers.BLACK,
    layers.BLACK_SUV,
    layers.Places
  ]
});

// Add our 'lightmap' tile layer to the map
streetmap.addTo(map);
//lightmap.addTo(map);

// Create an overlays object to add to the layer control
var overlays = {
  "Uber Pool": layers.UBER_POOL,
  "Uber X": layers.UBER_X,
  "Uber XL": layers.UBER_XL,
  "Select": layers.SELECT,
  "Black": layers.BLACK,
  "Black SUV": layers.BLACK_SUV,
  "Places": layers.Places
};

// Create a control for our layers, add our overlay layers to it
L.control.layers(null, overlays).addTo(map);

// Create a legend to display information about our map
var info = L.control({
  position: "bottomright"
});

// When the layer control is added, insert a div with the class of "legend"
info.onAdd = function() {
  var div = L.DomUtil.create("div", "legend");
  return div;
};
// Add the info legend to the map
info.addTo(map);

// Initialize an object containing icons for each layer group
var icons = {
   UBER_POOL: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "yellow",
    shape: "circle"
  }),
  UBER_X: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "purple",
    shape: "circle"
  }),
  BLACK: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "red",
    shape: "circle"
  }),
  BLACK_SUV: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "blue-dark",
    shape: "circle"
  }),
  UBER_XL: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "orange",
    shape: "circle"
  }),
  SELECT: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    iconColor: "white",
    markerColor: "green",
    shape: "circle"
  }),
  Places: L.ExtraMarkers.icon({
    icon: "ion-android-car",
    shadowUrl: "",
    iconColor: "white",
    markerColor: "violet",
    shape: "star"
  })
};

var centerMarker = L.marker([33.7762, -84.3895], {
                markerColor: "purple"
              });
centerMarker.addTo(map);

currentKey = "Select";
currentTime = "8:00";
showPlaces = false;

d3.select('#select-key').on('change', function(a) {
  // Change the current key and call the function to update the colors.
  currentKey = d3.select(this).property('value');
  Object.keys(layers).forEach(d=> {layers[d].clearLayers()});
  renderMap(currentKey, currentTime, showPlaces);
});

d3.select('#select-time').on('change', function(a) {
  // Change the current key and call the function to update the colors.
  currentTime = d3.select(this).property('value');
  Object.keys(layers).forEach(d=> {layers[d].clearLayers()});
  renderMap(currentKey, currentTime, showPlaces);
});

d3.select('#select-places').on('change', function(a) {
  // Change the current key and call the function to update the colors.
  if ( d3.select(this).property('value') == "showplaces") {
      showPlaces = true;
  } else {
      showPlaces = false;
  }
  //dontshowplaces
  Object.keys(layers).forEach(d=> {layers[d].clearLayers()});
  renderMap(currentKey, currentTime, showPlaces);
});

function renderMap(key, time, showPlaces) {
  // When the first API call is complete, perform another call to the Citi Bike Station Status endpoint
    console.log(showPlaces);

  d3.json("/data", function(response) {
  //d3.json(data, function(response) {
      console.log(response);
    // Create an object to keep of the number of markers in each layer
    var uberInfo = {
      UBER_POOL: 0,
      UBER_X: 0,
      UBER_XL: 0,
      SELECT: 0,
      BLACK: 0,
      BLACK_SUV: 0,
      Places: 0,
    };

    // Initialize a stationStatusCode, which will be used as a key to access the appropriate layers, icons, and station count for layer group
    var stationStatusCode;

    // Loop through the stations (they're the same size and have partially matching data)
    for (var i = 0; i < response.length; i++) {
        if ((response[i][0] == key)& (response[i][8] == time)){
        // Create a new station object with properties of both station objects
        var lat = response[i][1];
        var lon = response[i][2];
        var location = [lat,lon]
        // If a station is listed but not installed, it's coming soon
        // Check for location property
        if (lat) {
          // Add a new marker to the cluster group and bind a pop-up
              stationStatusCode = response[i][4]
              if (stationStatusCode == "Black SUV") {
                  stationStatusCode = "BLACK_SUV";
                  linecolor = "blue-dark";
                  rotationAngle = -90;
                  lat = lat - 0;
                  lon = lon - 0.0008
              }
              if (stationStatusCode == "UberPool") {
                  stationStatusCode = "UBER_POOL";
                  linecolor = "black";
                  rotationAngle = -55;
                  lat = lat + 0.0002;
                  lon = lon - 0.0006
              }
              if (stationStatusCode == "Select") {
                  stationStatusCode = "SELECT";
                  linecolor = "green";
                  rotationAngle = -20;
                  lat = lat + 0.0004;
                  lon = lon - 0.0004
              }
              if (stationStatusCode == "UberXL") {
                  stationStatusCode = "UBER_XL";
                  linecolor = "orange";
                  rotationAngle = 20;
                  lat = lat + 0.0004;
                  lon = lon + 0.0004
              }
              if (stationStatusCode == "Black") {
                  stationStatusCode = "BLACK";
                  linecolor = "red";
                  rotationAngle = 55;
                  lat = lat + 0.0002;
                  lon = lon + 0.0006
              }
              if (stationStatusCode == "UberX") {
                  stationStatusCode = "UBER_X";
                  linecolor = "purple";
                  rotationAngle = 90;
                  lat = lat + 0;
                  lon = lon + 0.0008
              }

              var newMarker = L.marker([lat, lon], {
                icon: icons[stationStatusCode],
                  rotationAngle: rotationAngle
              });
              //console.log(stationStatusCode)
              // Add the new marker to the appropriate layer
              newMarker.addTo(layers[stationStatusCode]);

              // Bind a popup to the marker that will  display on click. This will be rendered as HTML
              newMarker.bindPopup("<h2>" + response[i][0] + "</h2> <br> <h3> Range: " + response[i][7] + "</h3>");

//DELETE THIS PART
              // var line = [
              //     [33.7762, -84.3895],
              //     [location[0], location[1]]
              //   ];


              //  var newLine = L.polyline(line, {
              //     color: linecolor
              //   }).bindPopup("<h1>" + "Uber From GA Tech To: "  + response[i][0] +"</h1> <br> <h2>Travel Time: " + (response[i][6])/60 + " minutes" + "</h2>");
              // newLine.addTo(layers[stationStatusCode]);
              //
              // map.fitBounds(line, { padding: [100, 100] });

//ADD THIS NEW CODE

              var control = L.Routing.control({
              waypoints: [
                 L.latLng(33.7762, -84.3895),
                 L.latLng([location[0], location[1]])
              ],
              lineOptions:{
                 styles: [{color: 'lightgreen', opacity: 1, weight: 5}],
                 addWaypoints:false
              },
              draggableWaypoints: false,
              createMarker: function(){ return false; },
              router: L.Routing.mapbox('pk.eyJ1IjoibWVyeWVtbWxrIiwiYSI6ImNqcHVkanVhbjBmcTM0M282MmowcnJlZ3AifQ.jpDXpNPhKT8vC9vCj6-UrQ'),

              }).addTo(map);


              L.Routing.itinerary({pointMarkerStyle: {radius: 5,color: '#03f',fillColor: 'white',opacity: 1,fillOpacity: 0.7}});
              L.Routing.errorControl(control).addTo(layers[stationStatusCode]);

              map.fitBounds(line, { padding: [100, 100] });

//END NEW CODE

        }
        }
  }
      if (showPlaces) {
          d3.json("/placesinfo", function(places){
              console.log(key);

              if (key == "Select") {
                  pkey = "GaTech"
              } else {
                  pkey = key
              }
              for (var j = 0; j < places.length; j++) {
                  if (places[j][0] == pkey){
                      //console.log(places[j][0]);
                      stationStatusCode = "Places";
                      var clat = places[j][3];
                      var clon = places[j][4];
                      var cname = places[j][5];
                      var cvicinity = places[j][6];
                      console.log(clat);
                      var newMarker = L.marker([clat, clon], {
                        icon: icons[stationStatusCode]
                        });
                      newMarker.addTo(layers[stationStatusCode]);
                      newMarker.bindPopup("<h2 style=\"font-size: 25px\">"+cname + "</h2><br><h4> Address: " + cvicinity+"</h4>");
                  }
              }
          })
          //map.layers.append(layes.places)
      }

      // Update the station count

      // Create a new marker with the appropriate icon and coordinates

    // Call the updateLegend function, which will... update the legend!
    //updateLegend(updatedAt, stationCount);
  });
    //end of d3.json getting data
};
// Call the updateLegend function, which will... update the legend!
    //updateLegend(updatedAt, stationCount);
function updateLegend(time, stationCount) {
  document.querySelector(".legend").innerHTML = [
    "<p>Updated: " + moment.unix(time).format("h:mm:ss A") + "</p>",
    "<p class='out-of-order'>Out of Order Stations: " + stationCount.OUT_OF_ORDER + "</p>",
    "<p class='coming-soon'>Stations Coming Soon: " + stationCount.COMING_SOON + "</p>",
    "<p class='empty'>Empty Stations: " + stationCount.EMPTY + "</p>",
    "<p class='low'>Low Stations: " + stationCount.LOW + "</p>",
    "<p class='healthy'>Healthy Stations: " + stationCount.NORMAL + "</p>"
  ].join("");
}


/*
d3.json("outfile.json", function(response) {
 console.log(response)
  // Create a new marker cluster group
  //var markers = L.markerClusterGroup();

  // Loop through data
  for (var i = 0; i < response.length; i++) {

    // Set the data location property to a variable
    var location = response[i].geometry;

    // Check for location property
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
     str = ""
      for (var j = 0; j < response[i].value.length ; j++)   {
          str = str + "<h2>" + response[i].value[j].display_name + ":"+ response[i].value[j].estimate + "</h2> <hr>"
      }
      //  console.log(response[i].value.length)
      L.marker([location[0], location[1]])
        .bindPopup("<h1>" + response[i].place +"</h1> <hr>" + str ).addTo(map);
    }

  }

  // Add our marker cluster layer to the map
  //myMap.addLayer(markers);

});
*/
