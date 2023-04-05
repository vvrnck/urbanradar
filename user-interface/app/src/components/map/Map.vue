<template>
    <div class="map-wrapper">
        <div class="map-loading">
            <Loading color="primary" v-if="getMap.loading" type="linear" />
        </div>
        <div id="map">
            <LMap 
                :zoom="map.zoom"
                :center="map.centerMapCoords"
                :options="map.options"
                :ref="map.mapRef"
            >
                <VGeosearch :options="map.geosearchOptions" />

                <LControlLayers position="topright" />

                <LDrawToolbar position="topright" v-if="false" />

                <LTileLayer
                    v-for="tileLayer in map.tileLayers"
                    :key="tileLayer.name"
                    :url="tileLayer.url"
                    :visible="tileLayer.visible"
                    :name="tileLayer.label"
                    :attribuition="tileLayer.options.attibuition"
                    :subdomains="tileLayer.options.subdomains"
                    layer-type="base"
                >
                </LTileLayer>

                <LGeoJson 
                    v-for="(geojson, g) in map.geojsons" 
                    :key="g" 
                    :geojson="geojson.data" 
                    :options="geojson.options"
                />

                <LLayerGroup
                    v-for="(layerGroup, lg) in map.layerGroups"
                    :key="'LAYER_GROUP' + lg"
                    :visible="layerGroup.visible"
                    :layerType="layerGroup.type"
                    :name="`${layerGroup.name} (${layerGroup.featuresAmount})`"
                    ref="layerGroup"
                >

                    <LPolygon
                        v-for="(polygon, i) in layerGroup.features.polygon"
                        :key="'POLYGON' + i"
                        :options="{ id: polygon.id, name: polygon.name, value: polygon.value, defaultStyle: polygon.defaultStyle, polygon: polygon._polygon }"
                        :latLngs="polygon.geometry"
                        :color="polygon.color"
                        :fillColor="polygon.fillColor"
                        :fillOpacity="polygon.fillOpacity"
                        :opacity="polygon.opacity"
                        :weight="polygon.weight"
                        @click="openPopup(polygon)"
                    /> 

                    <LImageOverlay
                        v-for="(imageOverlay, j) in layerGroup.features.imageOverlay"
                        :key="'IMAGE_OVERLAY' + j"
                        :className="'IMAGE_OVERLAY_' + imageOverlay.id"
                        :options="{ id: imageOverlay.id, name: imageOverlay.name }"
                        :bounds="imageOverlay.bounds"
                        :url="imageOverlay.url"
                        :interactive="imageOverlay.interactive"
                        :zIndex="imageOverlay.zIndex"
                        :opacity="imageOverlay.opacity"
                        @click="openPopup(imageOverlay)"
                        @mouseenter="(e) => onMouseEnterImageOverlay(e, imageOverlay)"
                        @mouseleave="onMouseLeaveImageOverlay()"
                    />

                    <LMarkerCluster ref="markerClusterRef" :options="{ disableClusteringAtZoom: 13 }">
                        <LMarker
                            v-for="(marker, k) in layerGroup.features.marker"
                            :key="'MARKER' + k"
                            :latLng="marker.geometry"
                            @click="openDrawDialog(marker, layerGroup)"
                            :options="{ id: marker.id, name: marker.name }"
                        >
                            <LPopup :content="marker.text" />
                            <LIcon
                                :iconUrl="marker.iconUrl"
                                :iconRetinaUrl="marker.iconRetinaUrl"
                                :iconSize="marker.iconSize"
                                :iconAnchor="marker.iconAnchor"
                                :popupAnchor="marker.popupAnchor"
                            />
                        </LMarker>
                    </LMarkerCluster>
                    

                    <LMarkerCluster ref="pointClusterRef" :options="{ disableClusteringAtZoom: 15 }">
                        <LCircle 
                            v-for="(point, l) in layerGroup.features.point"
                            :key="'POINT' + l"
                            :latLng="point.geometry"
                            :color="point.color"
                            :fillColor="point.fillColor"
                            :fillOpacity="point.fillOpacity"
                            :radius="point.radius"
                        />
                        
                    </LMarkerCluster>


                </LLayerGroup>

                
                <LControl 
                    position="bottomleft"
                    class="map-watermark"
                >
                    <img src="../../assets/images/logo-transparent.svg" class="logo-watermark">
                </LControl>
                
            </LMap>
        
            <MapMenu 
                :loadFeatures="loadFeatures" 
                :clearMapData="clearMapData"
                :removeLayer="removeLayer"
            />

            <Filters />

            <Legend v-if="!getMap.loading" />

            <FeatureInformation 
                :featureInformation="featureInformation" 
                :key="featureInformation.open"
                v-if="featureInformation.open"
            />

            <Popup 
                :popup="popup" 
                :closePopup="closePopup" 
                v-if="popup.open"
            />

            <LayerOverlay
                v-if="getSelectedLayers().length > 1"
                :loadLayer="loadLayer"
                :clearMapData="clearMapData"
             />

            <Toolbox 
                :loadFeatures="loadFeatures" 
            />

            <TourDialog />
        </div>
    </div>
</template>

<script src="./map.js"></script>

<style lang="scss">
    @import "./map.scss";
</style>