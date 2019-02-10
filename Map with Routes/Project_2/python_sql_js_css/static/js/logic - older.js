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

// Initialize all of the LayerGroups we'll be using
var layers = {
  COMING_SOON: new L.LayerGroup(),
  EMPTY: new L.LayerGroup(),
  LOW: new L.LayerGroup(),
  NORMAL: new L.LayerGroup(),
  OUT_OF_ORDER: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map", {
  center: [33.767693,-84.4908152],
  zoom: 12,
  layers: [
    layers.COMING_SOON,
    layers.EMPTY,
    layers.LOW,
    layers.NORMAL,
    layers.OUT_OF_ORDER
  ]
});

// Add our 'lightmap' tile layer to the map
streetmap.addTo(map);
//lightmap.addTo(map);

// Create an overlays object to add to the layer control
var overlays = {
  "Coming Soon": layers.COMING_SOON,
  "Empty Stations": layers.EMPTY,
  "Low Stations": layers.LOW,
  "Healthy Stations": layers.NORMAL,
  "Out of Order": layers.OUT_OF_ORDER
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
  COMING_SOON: L.ExtraMarkers.icon({
    icon: "ion-settings",
    iconColor: "white",
    markerColor: "yellow",
    shape: "star"
  }),
  EMPTY: L.ExtraMarkers.icon({
    icon: "ion-android-bicycle",
    iconColor: "white",
    markerColor: "red",
    shape: "circle"
  }),
  OUT_OF_ORDER: L.ExtraMarkers.icon({
    icon: "ion-minus-circled",
    iconColor: "white",
    markerColor: "blue-dark",
    shape: "penta"
  }),
  LOW: L.ExtraMarkers.icon({
    icon: "ion-android-bicycle",
    iconColor: "white",
    markerColor: "orange",
    shape: "circle"
  }),
  NORMAL: L.ExtraMarkers.icon({
    icon: "ion-android-bicycle",
    iconColor: "white",
    markerColor: "green",
    shape: "circle"
  })
};

var centerMarker = L.marker([33.7762, -84.3895], {
                markerColor: "purple"
              });
centerMarker.addTo(map);


  // When the first API call is complete, perform another call to the Citi Bike Station Status endpoint
  d3.json("/data", function(response) {
  //d3.json(data, function(response) {
      console.log(response);
    // Create an object to keep of the number of markers in each layer
    var uberInfo = {
      COMING_SOON: 0,
      EMPTY: 0,
      LOW: 0,
      NORMAL: 0,
      OUT_OF_ORDER: 0
    };

    // Initialize a stationStatusCode, which will be used as a key to access the appropriate layers, icons, and station count for layer group
    var stationStatusCode;

    // Loop through the stations (they're the same size and have partially matching data)
    for (var i = 0; i < response.length; i++) {

        // Create a new station object with properties of both station objects
        var lat = response[i].[1];
        var lon = response[i].[2];
        // If a station is listed but not installed, it's coming soon
        // Check for location property
        if (lat) {

          // Add a new marker to the cluster group and bind a pop-up
         
          for (var j = 0; j < response[i].value.length ; j++)   {
              stationStatusCode = response[i].value[j].display_name
              if (stationStatusCode == "Black SUV") {
                  stationStatusCode = "COMING_SOON"
              }
              if (stationStatusCode == "UberPool") {
                  stationStatusCode = "EMPTY"
              }
              if (stationStatusCode == "Select") {
                  stationStatusCode = "LOW"
              }
              if (stationStatusCode == "UberXL") {
                  stationStatusCode = "NORMAL"
              }
              if (stationStatusCode == "Black") {
                  stationStatusCode = "OUT_OF_ORDER"
              }
              if (stationStatusCode == "UberX") {
                  stationStatusCode = "OUT_OF_ORDER"
              }
              var newMarker = L.marker([location[0], location[1]], {
                icon: icons[stationStatusCode]
              });
              console.log(stationStatusCode)
              // Add the new marker to the appropriate layer
              newMarker.addTo(layers[stationStatusCode]);

              // Bind a popup to the marker that will  display on click. This will be rendered as HTML
              newMarker.bindPopup(response[i].place + "<br> Range: " + response[i].value[j].estimate);
              
              var line = [
                  [33.7762, -84.3895],
                  [location[0], location[1]]
                ];
                L.polyline(line, {
                  color: "purple"
                }).addTo(map);
              
              
            }  
         
        }

  }

  
      // Update the station count
      
      // Create a new marker with the appropriate icon and coordinates
      
   

    // Call the updateLegend function, which will... update the legend!
    //updateLegend(updatedAt, stationCount);
  });

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