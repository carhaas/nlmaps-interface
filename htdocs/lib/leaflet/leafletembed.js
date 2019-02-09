var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var geojsonLayer;

L.Map = L.Map.extend({
	openPopup: function(popup) {
		this._popup = popup;
		return this.addLayer(popup).fire('popupopen', {
				popup: this._popup
		});
	}
});

var OSMmap = function () {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	//Stamen
	var osmUrl='https://tile.stamen.com/terrain/{z}/{x}/{y}.jpg';
	//OSM
	var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osmAttrib='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.';

	var osm = new L.TileLayer(osmUrl, {minZoom: 1, maxZoom: 18, attribution: osmAttrib});		

	map.setView(new L.LatLng(49.41,8.71),10);
	map.addLayer(osm);
};

function add_features(geojsonFeature) {
	function onEachFeature(feature, layer) { 
		if(feature.properties && feature.properties.popupContent) {
			layer.bindPopup(feature.properties.popupContent);
		}
	}
			
	geojsonLayer = L.geoJson(geojsonFeature.features, {
			onEachFeature: onEachFeature
	}).addTo(map);	
};

OSMmap.prototype.update_map_center = function(lat, lon) {
	map.setView(new L.LatLng(lat, lon),10);
}	

OSMmap.prototype.clear_map = function(lat, lon) {
	if(geojsonLayer!=null){
		geojsonLayer.clearLayers();
	}
}	

OSMmap.prototype.update_map = function(geojsonFeature) {
	if(geojsonLayer!=null){
		geojsonLayer.clearLayers();
	}
	if(!isNaN(geojsonFeature.lat) && !isNaN(geojsonFeature.lon)){
		map.setView(new L.LatLng(geojsonFeature.lat, geojsonFeature.lon),10);
		var reverse_geocoding_query = "http://open.mapquestapi.com/nominatim/v1/reverse.php?key=API_KEY&format=json&json_callback=renderExampleThreeResults&osm_type=W&osm_ids=";
		
		for(var i = 0; i < geojsonFeature.features.length; i++) {
			if(i != 0){
				reverse_geocoding_query += ","
			}
			reverse_geocoding_query += geojsonFeature.features[i].osm_id;
		}
		$.ajax({
			url: reverse_geocoding_query,
			type: "post",
			datatype:"json",
			success: function(response){
				var assemble_adresses = [];		
				for(var i = 0; i < response.length; i++) {
					var assemble_current_adress = "";
					if(response[i].address.country_code == "de"){
						if(response[i].address.road){
							assemble_current_adress += response[i].address.road;
						}
						if(response[i].address.house_number){
							if(response[i].address.road){
								assemble_current_adress += " "+response[i].address.house_number;								
							} else {
								assemble_current_adress += response[i].address.house_number;								
							}
						}
					} else {
						if(response[i].address.house_number){
							if(response[i].address.road){
								assemble_current_adress += response[i].address.house_number+" ";								
							} else {
								assemble_current_adress += response[i].address.house_number;								
							}
						}
						if(response[i].address.road){
							assemble_current_adress += response[i].address.road;
						}
					}
					if(response[i].address.postcode || response[i].address.city){
						if(assemble_current_adress != ""){
							assemble_current_adress += "<br/>";
						}
						if(response[i].address.postcode){
							assemble_current_adress += response[i].address.postcode;											
						}
						if(response[i].address.city){
							if(response[i].address.postcode){
								assemble_current_adress += " "+response[i].address.city;										
							} else {
								assemble_current_adress += response[i].address.city;									
							}									
						}
					}
					if(response[i].address.country){
						if(assemble_current_adress != ""){
							assemble_current_adress += "<br/>";
						}
						assemble_current_adress += response[i].address.country;						
					}
					assemble_adresses.push(assemble_current_adress);
				}		
					for(var i = 0; i < geojsonFeature.features.length; i++) {
						if(assemble_adresses[i] != "" && assemble_adresses[i]){
							geojsonFeature.features[i].properties.popupContent += "<br/>"+assemble_adresses[i];
						}
					}
				//}
				add_features(geojsonFeature);
			},
			error: function(err) {
				console.log("error");
				add_features(geojsonFeature);
			}
		});
	}
};

OSMmap.prototype.open_popup = function markerFunction(search_for_this){
	var features = geojsonLayer.getLayers();
	for(var i in features){
		features[i].closePopup();
	}
	for(var i in features){
		var search_word = features[i].toGeoJSON().search_word;
		if(~search_word.indexOf(search_for_this)){
			features[i].openPopup();
		};
	}
};