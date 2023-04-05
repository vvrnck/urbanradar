<template>
    <div id="map-mobile">
        <div class="map-wrapper">    
            <div class="map-loading">
              <Loading color="#52FFEE" v-if="loading" type="circular" />
            </div>
            <div id="map">
                 <LMap 
                    :zoom="map.zoom"
                    :center="map.centerMapCoords"
                    :options="map.options"
                    :ref="map.mapRef"
                    @click="closeAll()"
                >
                    <LControlLayers position="topright" />


                    <LControl class="clear-map-control" position="topright">
                        <div class="leaflet-control-layers control" @click="clearMapData()">
                            <v-icon>
                                mdi-broom
                            </v-icon>
                        </div>
                    </LControl>

                    <LControl class="search-features-control" position="topright" v-show="false">
                        <div class="leaflet-control-layers control" @click="loadFeatures()">
                            <v-icon>
                                mdi-magnify
                            </v-icon>
                        </div>
                    </LControl>

                    <LGeoJson 
                        v-for="(geojson, g) in map.geojsons" 
                        :key="g" 
                        :geojson="geojson.data" 
                        :options="geojson.options"
                    />

                    <LControl class="layer-control" position="bottomleft" v-show="false">
                        <div class="control">
                            <LayerMenu :loadFeatures="loadFeatures" />
                        </div>
                    </LControl>
                  
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
                        />

                        <LMarkerCluster ref="markerClusterRef" :options="{ disableClusteringAtZoom: 13 }">
                            <LMarker
                                v-for="(marker, k) in layerGroup.features.marker"
                                :key="'MARKER' + k"
                                :latLng="marker.geometry"
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
                        <img src="../../../assets/images/logo-transparent.svg" class="logo-watermark">
                    </LControl>
                    

                </LMap>
            </div>
            
            <div class="date-visor">
                <div class="leaflet-control-layers control">
                    {{dates}}
                </div>
            </div>
            


            <CustomControl 
                :map="map" 
                :goToInitialLocation="goToInitialLocation"
            />

            <FeatureCreation />
            
            
            <Filters :loadFeatures="loadFeatures" v-show="false" /> 

            <SelectedFilters :loadFeatures="loadFeatures" />

            <div class="date-map-control" id="date-map-control">
                <div class="leaflet-control-layers control">
                    <DatePicker :loadFeatures="loadFeatures" />
                </div>
            </div>
            

        
            <v-dialog
                v-model="popup.open"
                fullscreen
                transition="dialog-bottom-transition"
                scrollable
                class="popup"
            >
                <div class="popup-content">
                    <div class="popup-header">
                        <span>
                            {{ popup.data && popup.data.name }}
                        </span>
                        <v-btn
                            icon
                            dark
                            @click="closePopup()"
                        >
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </div>
                    <div class="popup-body">
                        <div v-for="(chart,c) in popup.charts" :key="c" class="chart">
                            <div v-if="!['dynamic_bar'].includes(chart.chart_options.chart.type) && chart.series.length > 0" v-show="false">
                                <apexchart 
                                    :type="chart.chart_options.chart.type" 
                                    :options="chart.chart_options" 
                                    :series="chart.series"
                                    :height="365"
                                ></apexchart>
                            </div>

                        

                        </div>
                    </div>
                </div>
            </v-dialog>
        
            <div class="actions-control" style="display: none;" >
                <div class="actions">
                    <div class="action-buttons">
                        <div class="control btn-reset" @click="clearMapData()">
                            Reset
                        </div>
                        <div class="control action-button btn-apply" @click="loadFeatures()">
                            Apply
                        </div>
                    </div>
                </div>
            </div>            
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';
import { getApi, getSelectedLayers, getMapCoords, getErrors, getGeojson, getBucketURL, updateMobileItem, getMapZoom, getDefaultSvg, getGradientPattern, getImageToDisplay } from '../../../utils';
import { isEmpty } from 'lodash';
import { Loading } from '../../components';
import NavBar from '../navbar/NavBar';
import LayerMenu from '../layer-menu/LayerMenu';
import Snackbar from '../snackbar/Snackbar';
import DatePicker from '../date-picker/DatePicker';
import * as LMarkerCluster from 'vue2-leaflet-markercluster';
import { 
            LMap, 
            LTileLayer, 
            LControlZoom, 
            LControl, 
            LControlLayers, 
            LGeoJson, 
            LPolygon,
            LImageOverlay,
            LLayerGroup,
            LMarker,
            LIcon,
            LCircle,
            LPopup,
} from 'vue2-leaflet';
import CustomControl from '../controls/CustomControl';
import Popup from '../popup/Popup';
import Filters from '../filters/Filters';
import SelectedFilters from '../filters/SelectedFilters';
import FeatureCreation from '../feature-creation/FeatureCreation.vue';

import moment from 'moment';
import { download } from '../../../aws/aws';

export default {
    name: 'Map',
    components: { 
        NavBar, Loading, Snackbar, LMap, LTileLayer, LControlZoom, LControlLayers, LControl, LayerMenu, LGeoJson, DatePicker, LPolygon, LImageOverlay, LLayerGroup, LMarker, LIcon, 
        LCircle, CustomControl, Popup, LPopup, Filters, SelectedFilters,
        LMarkerCluster, FeatureCreation
    },
    data() {
        return {
            popup: { open: false, data: null, charts: [] },
            title: 'map',
            loading: false,
            features: [],
            map: {
                mapRef: 'map',
                zoom: getMapZoom(),
                centerMapCoords: getMapCoords(),
                options: { zoomControl: false, attributionControl: false },
                geojsons: [],
                layerGroups: [],
                tileLayers: [
                    {
                        name: 'ROADMAP',
                        label: 'Detalhado',
                        visible: true,
                        origins: { SC: 'Roadmap', CT: 'Roadmap' },
                        url: 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                        options: { maxZoom: 18, attribution: 'Google Maps',  subdomains: ['mt0','mt1','mt2','mt3'], }
                    },
                    {
                        name: 'DARK',
                        label: 'Escuro',
                        origins: { SC: 'Escuro', CT: 'Dark' },
                        url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=39637672-75ae-4744-80c2-5d63301f5b3f',
                        options: { maxZoom: 18, attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors' }
                    },
                ],
            },
        }
    },
    beforeCreate() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
    mounted() {
        const _map = this.$refs.map.mapObject;
        window._map = _map;

        _map.on(L.Draw.Event.CREATED, (e) => {
            const editableLayers = new L.FeatureGroup();
            _map.addLayer(editableLayers);

            let type = e.layerType, layer = e.layer;      
            let geometry = layer.getLatLng();

            const { lng, lat } = geometry;

            const mobile = this.$store.getters.mobile;

            if (type === 'marker') {
                const newGeometry = [lat, lng, 0];
                const mobile = this.$store.getters.mobile;
                const featureData = mobile.draw.feature;
                
                const newFeatureData = Object.assign({}, featureData);

                newFeatureData.geometry = newGeometry;
                newFeatureData.type = 'MARKER';
                layer.bindPopup(newFeatureData.popup);

                const { feature, type } = mobile.draw;

                if (type === 'CREATE') {
                    this.$store.dispatch('updateMobile', { 
                        ...mobile, 
                        draw: { 
                            ...mobile.draw,
                            feature: newFeatureData
                        }
                    }).then(() => {
                        this.createMarkerFeature(newFeatureData);
                    });
                } else {
                    console.log('request edit')  
                }
            }

            editableLayers.addLayer(layer);
        });

        this.loadGeojson();
    },
    methods: {
        async createMarkerFeature(featureData) {
            this.loading = true;
            

            const snackbar = { open: true, color: '', text: 'sending_data', timeout: 2500, type: 'warning' };
            this.$store.dispatch('updateSnackbar', snackbar);    

            let mobile = Object.assign({}, this.$store.getters.mobile);

            const { layer_id } = featureData;

            

            let url = getApi('feature');
            axios.post(url, featureData).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    
                    return getErrors(errors);
                }

                let newFeatureData = {
                    layer_id: null,
                    tenant_id:  null,
                    feature_collection_id: null,
                    language: process.env.VUE_APP_DEFAULT_LOCALE,
                    fields: [],
                    properties: {},
                    geometry: null,
                    type: null,
                    popup: null
                };

                this.$store.dispatch('updateMobile', {
                        ...mobile,
                        draw: {
                            type: '',
                            layer: null,
                            feature: newFeatureData
                        },
                        toggle: {
                            ...mobile.toggle,
                            feature: false
                        }
                });
                            
                const snackbar = { open: true, color: '', text: 'success_create_interest_point', timeout: 2500, type: 'success' }; 
                this.$store.dispatch('updateSnackbar', snackbar);

                // CASO A LAYER NÃO ESTEJA SELECIONADA
                const layers = this.$store.getters.layers;
                const newLayers = Object.assign([], layers);
    
                newLayers.map(section => {
                    section.layers.map(layer => {
                        if (layer.id === layer_id) layer.selected = true;
                    })
                })
    
                this.$store.dispatch('updateLayers', newLayers);
            })
            .then(() => this.loadFeatures())
            .catch(error => {
                console.error(error);
                this.loading = false;
                //this.updateLoading(false);
                const snackbar = { open: true, color: '', text: 'error_create_interest_point', timeout: 2500, type: 'error' };                         
                this.$store.dispatch('updateSnackbar', snackbar);                
                updateMobileItem('feature', true);
            });
        },
        async loadGeojson() {
            const files = getGeojson();
            const url = getBucketURL();
    
            if (isEmpty(files) || !url) return;
                
            files.map(fileName => {
                //this.loading = true;
                //this.updateLoading(true);
                
                let newUrl = `${url}/geojson/${fileName}.geojson`;
                
                var requestOptions = {
                    method: 'GET',
                    redirect: 'follow'
                };
                  
                fetch(newUrl, requestOptions)
                    .then(response => response.json())
                    .then(result => {
                        let geoJSONLayer = result;
                        this.map.geojsons.push({
                            data: geoJSONLayer,
                            options: { 'color': '#c4c4a6', 'stroke-width': '3', 'fill-opacity': 0.5 }
                        });
                        //this.loading = false;
                        //this.updateLoading(false);
                    })
                    .catch(error => {
                        console.log(error)
                        //this.loading = false;
                        //this.updateLoading(false);
                        axios.get(`geojson/default.geojson`).then(response => {
        
                            let geoJSONLayer = response.data;
                            this.map.geojsons.push({
                                data: geoJSONLayer,
                                options: { 'color': '#c4c4a6', 'stroke-width': '3', 'fill-opacity': 0.5 }
                            });

                            //this.loading = false;
                            //this.updateLoading(false);
                        });
                    });
            });
        },      
        closeAll() {
            const currentMenuState = this.$store.getters.menu;

            let newMenu = Object.assign({}, currentMenuState);

            newMenu = {
                layers: false,
                dates: false,
                settings: false,
            }

            document.getElementById('date-map-control').style.bottom = '35px';

            this.$store.dispatch('updateMenu', newMenu);
        },
        getSelectedLayers() {
            return getSelectedLayers();
        },
        closePopup() {
            this.popup = { open: false, data: null, charts: [] }
        },
        openPopup(feature) {
            this.loading = true;

            const currentMapData = this.$store.getters.map;
            const dates = currentMapData.date;

            let dt_start = dates[0];
            let dt_end = dates[1];
            
            const { idLayer, name } = feature;

            let url = getApi('features', { id_layer: idLayer, list_ids_cat: '', dt_start: dt_start, dt_end: dt_end, hexcode: name });

            axios.get(url).then(response => {
                const { charts } = response.data;

                charts.map(chart => {
                    const { chart_options } = chart;
                    
                    if (chart_options.chart.type === 'heatmap') {
                        chart_options.xaxis.categories = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
                    }

                    if (chart_options.chart.type === 'donut') {
                        delete chart_options.responsive;
                    }
                });

                this.popup = { 
                    open: true, 
                    data: feature, 
                    charts: charts
                };

                this.loading = false;
            }).catch(err => {
                console.error(err);
                this.loading = false;
            })
        },
        goToInitialLocation() {
            let initialPosition = this.map.centerMapCoords;
            let zoom = this.map.zoom;
            this.$refs.map.mapObject.flyTo(initialPosition, zoom);
        },
        closeMenu() {
            const mobile = this.$store.getters.mobile;
            this.$store.dispatch('updateMobile', { 
                ...mobile, 
                toggle: { 
                    layers: false,
                    dates: false,
                    settings: false,
                    fullscreen: false,
                    caption: false,
                    feature: false
                } 
            }); 
        },      
        getDates(dates) {
            
            if (dates.length === 1) dates[1] = dates[0];

            if (moment(dates[0]).isAfter(dates[1])) dates = [dates[1], dates[0]];

            return dates;
        },
        async clearMapData() {
            updateMobileItem('caption', false);
            
            if (isEmpty(this.map.layerGroups) && !this.loading) {
                const snackbar = { open: true, color: '', text: 'no_info_to_remove', timeout: 2500, type: 'warn' };
                this.$store.dispatch('updateSnackbar', snackbar);
                return //this.snackbar = { open: true, color: '#cc0000', text: 'Sem informações para remoção.', timeout: 2500 };
            }

            this.map.layerGroups = [];
        },
        getLayerFilters(layer) {
            let filters = [];
            layer.filters.map(filter => {
                filter.values.map(item => filters.push(`filter[]=${filter.name}|${item}`));
            });
            return filters.join('&');
        },
        checkMapConfig() {
            const newSections = Object.assign([], this.$store.getters.layers);
            const dates = this.$store.getters.dates;

            let currentDate = moment().format('yyyy-MM-DD');
            currentDate = moment(currentDate).subtract(1, "days").format("yyyy-MM-DD");

            let firstDate = dates[0];
            
            newSections.map(section => {
                section.layers.map(layer => {
                    const { extra_props } = layer.style;

                    layer.selected = false; // seta todas as layers para false;

                    if (moment(firstDate).isAfter(currentDate)) {
                        if (extra_props && extra_props.mobile && (extra_props.type === 'icon' || extra_props.type === 'marker')) {
                            layer.selected = true;
                            let newDates = [firstDate, firstDate]; // garente que a predição seja para apenas 1 dia
                            this.$store.dispatch('updateDates', newDates);
                        }                        
                    } else {
                        if (extra_props && extra_props.mobile && extra_props.type !== 'icon') layer.selected = true;
                    }
                })
            });

            this.$store.dispatch('updateLayers', newSections);
        },
        async loadFeatures() {
            console.log('loading features...')
            this.loading = true;

            this.clearMapData().then(() => this.closeMenu());

            const sections = this.$store.getters.layers;
            let dates = this.$store.getters.dates;

            if (isEmpty(dates)) { 
                const snackbar = { open: true, color: '', text: 'error_get_layers', timeout: 2500, type: 'error' };
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
                return;
            }
            
            dates = this.getDates(dates);
            let dt_start = dates[0];
            let dt_end = dates[1];

            this.checkMapConfig(); // TROCA ENTRE PASSADO E FUTURO

            sections.map(section => {
                section.layers.map(layer => {
                    
                    const { id, selected, name, editable } = layer;
                    
                    if (selected) {    
                                                
                        let url = getApi(`layer/${id}/feature`); 
                        url += this.getLayerFilters(layer);

                        let data = { id_layer: id, dt_start: dt_start, dt_end: dt_end };
                                                
                        axios.get(url, { params: data }).then(response => { 
                            const { data, errors } = response.data;

                            if (!isEmpty(errors)) {
                                this.loading = false;
                                return getErrors(errors);
                            }

                            const { features, items } = data;

                            if (isEmpty(features)) {
                                const snackbar = { open: true, color: '', text: 'no_features_founded', timeout: 2500, type: 'success' };
                                this.$store.dispatch('updateSnackbar', snackbar);
                                this.loading = false;
                                return;
                            }

                            let LAYER_FEATURES = {
                                polygon: [],
                                imageOverlay: [],
                                marker: [],
                                point: [],
                            };

                            features.map(async (f) => {                                 
                                const feature = await this.getFeature(f, layer);

                                if (isEmpty(feature.fields)) return;

                                if (feature.type === 'POLYGON') LAYER_FEATURES.polygon.push(feature);
                                else if (feature.type === 'IMAGE_OVERLAY') LAYER_FEATURES.imageOverlay.push(feature);
                                else if (feature.type === 'MARKER') LAYER_FEATURES.marker.push(feature);
                                else if (feature.type === 'POINT') LAYER_FEATURES.point.push(feature);

                            });

                            let featuresAmount = 0;
                            Object.values(LAYER_FEATURES).map(item => featuresAmount += item.length)

                            const layerGroup = {
                                id: id,
                                name: name,
                                featuresAmount: featuresAmount,
                                features: LAYER_FEATURES,
                                visible: true,
                                type: 'overlay',
                                editable: editable
                            };         

                            layer.features = features;
                            layer.legend = items;
                            layer.layerGroup = LAYER_FEATURES;

                            this.map.layerGroups.push(layerGroup);
                            const layerGroups = this.map.layerGroups;

                            // montar legenda apos request
                            //updateMobileItem('caption', true);
                            

                            this.loading = false;
                        }).catch(err => {
                            console.log(err);
                            this.loding = false;
                        })
                    }
                })
            })

        },
        hslToHex(color) {
                let hsl = color.substring(
                    color.indexOf('(') + 1,
                    color.indexOf(')')
                ).replace(/%/g, '');
                
                let [h,s,l] = hsl.split(',');                

                l /= 100;
                const a = s * Math.min(l, 1 - l) / 100;
                const f = n => {
                  const k = (n + h / 30) % 12;
                  const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
                  return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
                };
                return `#${f(0)}${f(8)}${f(4)}`;
        },
        async getFeature(feature, layer) {            
            const { id, name, properties, geometry, label, style, type, props, fields } = feature;
                    
            let text = name;
            let language = this.$i18n.locale;
            
            let featureProperties = {
                id,
                name,
                text: text,
                geometry: geometry,
                idLayer: layer.id,
                properties,
                styles: style,
                isOnEditableLayer: layer.editable,
                fields: fields,
                defaultStyle: style
            }

            switch (feature.type) {
                case 'POLYGON': {
                    const { color, fillColor, fillOpacity, opacity, weight } = style;

                    let polygonColor = color;
                    let polygonFillColor = fillColor;
                    
                    try {
                        const layerType = layer.style.types.find(type => type.value);    
                        if (layerType.name === 'hexagon') {
                            polygonColor = layerType.color;
                            polygonFillColor = layerType.color;
                            featureProperties.styles = {
                                ...featureProperties.styles,
                                color: polygonColor,
                                fillColor: polygonFillColor
                            }
                            featureProperties.defaultStyle = {
                                ...featureProperties.defaultStyle,
                                color: polygonColor,
                                fillColor: polygonFillColor
                            }
                        }
                    } catch (error) {
                        console.error(error);
                    }

                    let fillPalette = [];
                    let gradientString = '';
                    let colorFillPallete = this.hslToHex(polygonColor);

                    if (layer.style.texture.value === 'HORIZONTAL') {
                        fillPalette = [colorFillPallete, '#FFFFFF'];
                        gradientString = `<linearGradient id="layer-${layer.id}-stripes-${colorFillPallete}" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset=0 stop-color=${fillPalette[0]} />
                                                <stop offset=20% stop-color=${fillPalette[1]} />
                                                <stop offset=20% stop-color=${fillPalette[0]} />
                                                <stop offset=40% stop-color=${fillPalette[1]} />
                                                <stop offset=40% stop-color=${fillPalette[0]} />
                                                <stop offset=60% stop-color=${fillPalette[1]} />
                                                <stop offset=60% stop-color=${fillPalette[0]} />
                                                <stop offset=80% stop-color=${fillPalette[1]} />
                                                <stop offset=80% stop-color=${fillPalette[0]} />                                                
                                                <stop offset=100% stop-color=${fillPalette[1]} />
                                                <stop offset=100% stop-color=${fillPalette[0]} />
                                              </linearGradient>`;                                      
                        
                         
                    } else if (layer.style.texture.value === 'VERTICAL') {
                        
                        fillPalette = [colorFillPallete, '#FFFFFF'];
                        gradientString = `<linearGradient id="layer-${layer.id}-stripes-${colorFillPallete}" x1="0" y1="0" x2="1" y2="0">
                                                <stop offset=0 stop-color=${fillPalette[0]} />
                                                <stop offset=20% stop-color=${fillPalette[1]} />
                                                <stop offset=20% stop-color=${fillPalette[0]} />
                                                <stop offset=40% stop-color=${fillPalette[1]} />
                                                <stop offset=40% stop-color=${fillPalette[0]} />
                                                <stop offset=60% stop-color=${fillPalette[1]} />
                                                <stop offset=60% stop-color=${fillPalette[0]} />
                                                <stop offset=80% stop-color=${fillPalette[1]} />
                                                <stop offset=80% stop-color=${fillPalette[0]} />                                                
                                                <stop offset=100% stop-color=${fillPalette[1]} />
                                                <stop offset=100% stop-color=${fillPalette[0]} />
                                              </linearGradient>`;

                                          
                    }

                    try {
                        const elExists = document.getElementById(`layer-${layer.id}-stripes-${colorFillPallete}`);
                        if (layer.style.texture.value !== 'NONE' && !elExists) { // PRECISA QUE O MAPA TENHA SVG CARREGADO (VEM DO GEOJSON ATULMENTE)
                            let svg = document.getElementsByTagName('svg')[0];
                            let newSvgDefs = document.createElementNS("http://www.w3.org/2000/svg", 'defs');
                            newSvgDefs.classList.add(`layer-${layer.id}`);
                            newSvgDefs.insertAdjacentHTML('afterbegin', gradientString);
                            svg.appendChild(newSvgDefs);
                        }
                    } catch (error) {
                        console.log(error);
                    }
                    
                    let polygon = {
                        ...featureProperties,
                        color: polygonColor,
                        fillColor: layer.style.texture.value !== 'NONE' ? `url(#layer-${layer.id}-stripes-${colorFillPallete})` : polygonFillColor,
                        fillOpacity: fillOpacity,
                        opacity: opacity,
                        type: type || 'POLYGON',
                        weight: weight,                       
                    };
                    polygon.defaultStyle = {
                        color: polygon.color,
                        fillColor: polygon.fillColor,
                        fillOpacity: polygon.fillOpacity,
                        opacity: polygon.opacity, 
                        weight: polygon.weight,
                    }

                    polygon._polygon = polygon;

                    return polygon;
                }
                case 'IMAGE_OVERLAY': {
                    const { color, fillColor, fillOpacity, opacity, weight } = style;
                    
                    let image = null;
                    let polygonColor = color;
                    let polygonFillColor = fillColor;

                    // IF THERE ARE NO FIELDS OR THE FEATURE DOES NOT HAVE EXTRA_PROPS, RETURNS A DEFAULT IMAGE
                    const field = fields.find(f => f.extra_props !== null);

                    if (isEmpty(fields) || (!field || !field.extra_props || !field.extra_props.image)) {
                        let icon = getDefaultSvg();
                        icon = icon.replace("[width]", 350);
                        icon = icon.replace("[height]", 350);
                        icon = icon.replace("[color]", polygonColor);
                        icon = icon.replace("[opacity]", opacity);
                        
                        let base64 = btoa(icon);
                        let imageUrl = `data:image/svg+xml;base64,${base64}`
                    
                        return {
                            ...featureProperties,
                            bounds: geometry,
                            url: imageUrl,
                            opacity: opacity,
                            type: 'IMAGE_OVERLAY',
                            interactive: true,
                            zIndex: 9999,
                            imageOverlayType: null
                        }
                    }             
                
                   

                    // SET FEATURE PROPERTYS WITH THE LAYER VIEW PROPERTYS
                    // * it is necessary in case the user wants to apply the same color to all features on a layer *
                    try {
                        const layerType = layer.style.types.find(type => type.value);    
                        if (layerType.name === 'hexagon') {
                            polygonColor = layerType.color;
                            polygonFillColor = layerType.color;
                            featureProperties.styles = {
                                ...featureProperties.styles,
                                color: polygonColor,
                                fillColor: polygonFillColor
                            }
                            featureProperties.defaultStyle = {
                                ...featureProperties.defaultStyle,
                                color: polygonColor,
                                fillColor: polygonFillColor
                            }
                        }
                    } catch (error) {
                        console.error(error);
                    }
                    
                    // SET THE PATTERNS ON THE FEATURE
                    let gradientString = '';
                    let colorFillPallete = this.hslToHex(polygonColor);

                    if (layer.style.texture.value === "HORIZONTAL") {
                        gradientString = getGradientPattern(layer, colorFillPallete, "HORIZONTAL");
                    } else if (layer.style.texture.value === "VERTICAL") {
                        gradientString = getGradientPattern(layer, colorFillPallete, "VERTICAL");
                    }

                    // SET THE IMAGE TO BE THE EXTRA_PROPS IMAGE URL
                    const { key } = field;
                    
                    const newUrl = `${process.env.VUE_APP_AWS_BUCKET_URL}/media/${key.toUpperCase()}.svg`;
                    let downloadedImage = null;
                   
                    if (!Object.prototype.hasOwnProperty.call(this.downloadedImagesUrls, key)) {
                        // this.downloadedImagesUrls[key] = null;               
                        // downloadedImage = download(newUrl);
                        // this.downloadedImagesUrls[key] = downloadedImage;
                    } 
                    
                    let icon = null;
                    icon = await getImageToDisplay(this.downloadedImagesUrls[key], polygonColor, opacity);

                    // WORDAROUND TO APPEND PATTERNS TO SVG'S ON RUNTIME
                    try {
                        const elExists = document.getElementById(`layer-${layer.id}-stripes-${colorFillPallete}`);
                        if (layer.style.texture.value !== 'NONE' && !elExists) { // PRECISA QUE O MAPA TENHA SVG CARREGADO (VEM DO GEOJSON ATUALMENTE)
                            let svg = icon;                          
                            let newSvg = new DOMParser().parseFromString(svg, "image/svg+xml").firstElementChild; 
                            let newSvgDefs = document.createElementNS("http://www.w3.org/2000/svg", 'defs');
                            newSvgDefs.classList.add(`layer-${layer.id}`);
                            newSvgDefs.insertAdjacentHTML('afterbegin', gradientString);
                            newSvg.appendChild(newSvgDefs);

                            
                            newSvg.getElementsByTagName('g')[0].setAttribute('fill', `url(#layer-${layer.id}-stripes-${colorFillPallete})`);
                            icon = newSvg.outerHTML.trim();
                    
                        }
                    } catch (error) {
                        console.log(error);
                    }

                    let base64 = btoa(icon);
                    let imageUrl = `data:image/svg+xml;base64,${base64}`;


                    let imageOverlay = {
                        ...featureProperties,
                        bounds: geometry,
                        url: imageUrl,
                        opacity: opacity,
                        type: 'IMAGE_OVERLAY',
                        interactive: true,
                        zIndex: 9999,
                        imageOverlayType: key
                        //type: key
                    }

                    return imageOverlay;
                }
                case 'MARKER': {
                    const { id, image } = properties;
                    const { icon } = style;
                    
                    let text = ``;

                    layer.filters.map(filter => {
                        
                        const field = fields.find(f => f.field_config_id === filter.id);
                        if (!field) return text += '';
                        
                        let fieldName = filter.label && filter.label[language] ? filter.label[language] : filter.name;

                        let row = '';
                        if (filter.type === 'image') {
                            row += `${fieldName}: <a href='${field.key}' target='_blank'>${field.key}</a> <br />`;
                        } else {
                            row += `${fieldName}: ${field.key} <br />`;
                        }

                        text += row;
                    });

                    let iconUrl = require('../../../assets/icons/' + icon);

                    if (image && !isEmpty(image)) {
                        iconUrl = image;
                    }

                    let marker = {
                        ...featureProperties,
                        type: type || 'MARKER',
                        iconUrl: iconUrl,
                        iconRetinaUrl: iconUrl,
                        iconSize: [32, 32],
                        iconAnchor: [16, 37],
                        popupAnchor: [0, -30],
                        text: text
                    }
                    
                    return marker;
                }
                case 'POINT': {
                    const { color, fillColor, fillOpacity, opacity, stroke, radius } = style;

                    let point = {
                        ...featureProperties,
                        type: type || 'POINT',
                        color: color,
                        fillColor: fillColor,
                        fillOpacity: fillOpacity,
                        radius: 3,
                        stroke: false,
                    }

                    return point;
                }
                default:
                    return;
            }
        },      
        isLayerSelected(layer) {
            let isSelected = false;
            Object.keys(layer).map(key => {
                if (key == 'types') {
                    Object.values(layer[key]).map(type => {
                        if (type.value) isSelected = true;
                    })
                }
            })
            return isSelected;
        },
        async reset() {
            window.mapmanager.clearData().then(() => {
                const snackbar = { open: true, color: '', text: 'reset_confi', timeout: 2500, type: 'success' };
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
            });
        },
        getFilterIds(filters) {
            let categorys = [];
            
            filters.map(f => {
                f.tags.map(t => {
                    categorys.push(t.id);
                })
            })

            return categorys;
        }
    },
    computed: {
        menu() {
            return this.$store.getters.menu;
        },     
        dates() {
            const dates = this.$store.getters.dates;
            let start = moment(dates[0]).format('DD/MM/YYYY');
            let end = moment(dates[1]).format('DD/MM/YYYY');
            return start + ' ~ ' + end;
        }
    }
}
</script>

<style lang='scss'>

#map-mobile {
    height: 100%;
    min-height: -webkit-fill-available;
}
.map-wrapper {
    //margin-top: 56px !important;
    min-height: -webkit-fill-available;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
    .map-loading {
        position: absolute;
        top: 1px;
        width: 100%;
        z-index: 99999999999;
    }
}

#map {
    height: 100%;    
    min-height: -webkit-fill-available;
}

.popup {
    position: absolute;
    top:0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 99999999;        
}

.popup-content  {
    overflow-y: auto;
    
    .popup-header {
        color: #FFFFFF;
        position: fixed;
        top: 0;
        width: 100%;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        padding: 15px 10px;
        height: 64px;
    }
    .popup-body {
        margin-top: 64px;
        overflow: hidden;
        
        .chart {
            
            width: 100%;
            height: 100%;
            margin: 20px 0px; 
            
        }
    }
}


// TODO - popup style
.v-dialog {
    //background-color: rgba(0,0,0, 0.9) !important;
    color: #FFF !important;
}


.actions-control {
    position: absolute;
    bottom: 45px;
    z-index: 999;
    width: 100%;
    .actions {
        width: 100%;
        position: inherit;
        display: flex;
        gap: 10px;
        justify-items: center;
        justify-content: center;
        align-items: center;
        .action-buttons {
            display: contents;
            border-radius: 20px;
            color: #FFF;
            .btn-apply {
                background-color: #73b8ad;
            }
            .btn-reset {
                background-color: #e05a4c;
            }
        }
    }
}


.control {
    border: 2px solid rgba(0,0,0,0.2);   
    background-clip: padding-box;
    padding: 5px 10px;
    border-radius: 5px;
    //background-color: #FFF;
    max-width: 300px;
    cursor: pointer;
    label {
        color: #adadad !important;
        font-size: 16px;
    }
}

.date-visor {
    position: absolute;
    top: 5px;
    align-items: center;
    width: 100%;
    height: 48px;
    z-index: 999;
    display: grid;
    grid-gap: 10px;
    justify-content: center;
}

.date-map-control {
    position: absolute;
    bottom: 35px;
    align-items: center;
    width: 100%;
    height: 48px;
    z-index: 999;
    display: grid;
    grid-gap: 10px;
    justify-content: center;
}

.map-caption {
    width: 200px;
    background-color: #000;
    border: 1px solid;
    //transition: all 0.3s ease-in-out 0s;
    opacity: 0.6;
    padding: 5px;
    color: #FFF;
    .caption-header {
        margin-bottom: 5px;;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .inner-caption {
        border: 1px solid #FFF;
        padding: 5px;
        .inner-caption-marker, .inner-caption-point {
            display: flex;
            justify-content: space-between;
            padding: 5px;
        }

        .inner-caption-polygon {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .inner-caption-scale-color {
            margin-left: 10px;
            .inner-caption-scale-color-item {
                display: flex;
                align-items: center;
                gap: 10px;
            }
        }

    }
}

.map-filter {
    width: 200px;
    background-color: #000;
    border: 1px solid;
    //transition: all 0.3s ease-in-out 0s;
    opacity: 0.6;
    padding: 5px;
    color: #FFF;
    .filter-header {
        margin-bottom: 5px;;
    }
    .inner-filter {
        border: 1px solid #FFF;
        padding: 5px;
        .inner-filter-item {
            display: grid;
            grid-auto-flow: row;
            background-color: #000;
            border: 1px solid;
            padding: 5px;
            margin-bottom: 5px;
        }
    }
}

</style>