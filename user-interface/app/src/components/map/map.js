import L from 'leaflet';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import VGeosearch from 'vue2-leaflet-geosearch';
import LDrawToolbar from 'vue2-leaflet-draw-toolbar';
import * as LMarkerCluster from 'vue2-leaflet-markercluster';

import { 
    LMap, LTileLayer, LControlZoom, LControl, LControlLayers, LGeoJson,
    LPolygon, LImageOverlay, LLayerGroup, LMarker, LIcon, LCircle, LPopup
} from 'vue2-leaflet';


import LayerOverlay from '../layer-overlay/LayerOverlay.vue';
import Loading from '../loading/Loading.vue';
import MapMenu from '../map-menu/MapMenu.vue';
import FeatureInformation from '../feature-information/FeatureInformation.vue';
import Filters from '../filters/Filters.vue';
import Popup from '../popup/Popup.vue';
import Toolbox from '../toolbox/Toolbox.vue';
import Legend from '../legend/Legend.vue';
import TourDialog from '../tour-dialog/TourDialog.vue';

import { getApi, getBucketURL, getErrors, getGeojson, getMapCoords, getMapZoom, getMapTileLayer, getSelectedLayers, getImageToDisplay, getGradientPattern, getDefaultSvg } from '../../utils';
import { isEmpty } from 'lodash';
import axios from 'axios';
import moment from 'moment';
import { download } from '../../aws/aws';
import router from '../../routes/router';

export default {
    name: 'Map',
    components: { 
        VGeosearch, LDrawToolbar, LMarkerCluster,
        LMap, LTileLayer, LControlZoom, LControl, LControlLayers, LGeoJson, 
        LPolygon, LImageOverlay, LLayerGroup, LMarker, LIcon, LCircle, LPopup,
        LayerOverlay, Loading, MapMenu, FeatureInformation, Filters, Popup, Toolbox, Legend, TourDialog
    }, 
    data() {
        return {
            downloadedImagesUrls: {},
            loading: true,
            popup: { 
                open: false, 
                data: null, 
                tray: false,
                charts: [], 
                tabs: []
            },
            dialog: false,
            featureInformation: {
                open: false,
                position: null,
                element: null,
                data: null
            },
            map: {
                mapRef: 'map',
                zoom: getMapZoom(),
                centerMapCoords: getMapCoords(),
                options: { zoomControl: false, attributionControl: false },
                layerGroups: [],
                geojsons: [],
                tileLayers: getMapTileLayer(),
                geosearchOptions: {
                    provider: new OpenStreetMapProvider(),
                    autoComplete: true,
                    autoCompleteDelay: 0,
                    autoClose: true, 
                }
            }
        }
    },  
    beforeCreate() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
    mounted() {
        const _map = this.$refs.map.mapObject;
        
        window._map = _map;     
        window._refs = this.$refs;
        
        _map.on(L.Draw.Event.CREATED, (e) => {
            const editableLayers = new L.FeatureGroup();
            _map.addLayer(editableLayers);

            let type = e.layerType, layer = e.layer;      
            let geometry = layer.getLatLng();

            const { lng, lat } = geometry;

            if (type === 'marker') {
                const newGeometry = [lat, lng, 0];
                const featureData = this.$store.getters.featureData;
                
                const newFeatureData = Object.assign({}, featureData);

                newFeatureData.geometry = newGeometry;
                newFeatureData.type = 'MARKER';
                layer.bindPopup(newFeatureData.popup);

                const drawDialog = this.$store.getters.drawDialog;
                const { feature, type } = drawDialog;

                if (type === 'CREATE') {
                    this.$store.dispatch('updateFeatureData', newFeatureData).then(() => {
                        this.createMarkerFeature(newFeatureData);
                    });
                } else {
                    this.$store.dispatch('updateFeatureData', newFeatureData).then(() => {
                        this.editMarkerFeature(newFeatureData);
                    });
                }
                
                
            }

            editableLayers.addLayer(layer);
        });

        setTimeout(() => {
            this.loadGeojson().then(() => this.updateLoading(false));
        }, 500);
        
        window._mapFunctions = {
            loadFeatures: this.loadFeatures,
        }
    },
    methods: {
        async loadGeojson() {
            console.log("Loading geojsons...")
            const files = getGeojson();
            //const url = getBucketURL();
    
            if (isEmpty(files)) return;
                
            files.map(fileName => {
                //this.loading = true;
                //this.updateLoading(true);
                
                let newUrl = `/geojson/${fileName}.geojson`;
                
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
        async editMarkerFeature(featureData) {
            this.updateLoading(true);

            const snackbar = { open: true, color: '', text: 'sending_data', timeout: 2500, type: 'warning' };
            this.$store.dispatch('updateSnackbar', snackbar);    

            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            const { feature, layer } = newDrawDialog;
            const { layer_id, geometry, fields } = featureData;
            
            const payload = {
                geometry,
                fields,
                laguage: this.$i18n.locale
            }

            let url = getApi(`feature/${feature.id}`);
            axios.patch(url, payload).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    //this.loading = false;
                    this.updateLoading(false);
                    return getErrors(errors);
                }       
                
                newDrawDialog = { open: false, layer: null, feature: null, type: '' };
                this.$store.dispatch('updateDrawDialog', newDrawDialog);

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
                
                this.$store.dispatch('updateFeatureData', newFeatureData);
                            
                const snackbar = { open: true, color: '', text: 'success_edit_interest_point', timeout: 2500, type: 'success' }; 
                this.$store.dispatch('updateSnackbar', snackbar);

                // CARREGA LAYER
                const layers = this.$store.getters.layers;
                const newLayers = Object.assign([], layers);
    
                newLayers.map(section => {
                    section.layers.map(layer => {
                        if (layer.id === layer_id) {
                            layer.selected = true;
                            layer.filters.map(filter => filter.key = '');
                        }
                    })
                })
    
                this.$store.dispatch('updateLayers', newLayers);

                //this.$refs.clusterRef.refreshClusters();

                this.updateLoading(false);
                
                this.loadFeatures();
            })
            
            .catch(error => {
                console.error(error);
                //this.loading = false;
                this.updateLoading(false);

                this.removeMarkerFromMap(feature);

                const snackbar = { open: true, color: '', text: 'error_edit_interest_point', timeout: 2500, type: 'error' };                         
                this.$store.dispatch('updateSnackbar', snackbar);                

                return this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: true });
            });

        },
        async createMarkerFeature(featureData) {
            //this.loading = true;
            this.updateLoading(true);

            const snackbar = { open: true, color: '', text: 'sending_data', timeout: 2500, type: 'warning' };
            this.$store.dispatch('updateSnackbar', snackbar);    

            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);

            const { layer_id } = featureData;

            

            let url = getApi('feature');
            axios.post(url, featureData).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    //this.loading = false;
                    this.updateLoading(false);
                    return getErrors(errors);
                }

                
                newDrawDialog = { open: false, layer: null, feature: null, type: '' };
                this.$store.dispatch('updateDrawDialog', newDrawDialog);

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
                
                this.$store.dispatch('updateFeatureData', newFeatureData);
                            
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
                //this.loading = false;
                this.updateLoading(false);
                const snackbar = { open: true, color: '', text: 'error_create_interest_point', timeout: 2500, type: 'error' };                         
                this.$store.dispatch('updateSnackbar', snackbar);                
                return this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: true });
            });
        },
        getLayerFilters(layer) {
            let filters = [];
            layer.filters.map(filter => {
                filter.values.map(item => filters.push(`filter[]=${filter.name}|${item}`));
            });
            return filters.join('&');
        },
        async removeMarkerFromMap(marker) {
            //this.$refs.clusterRef.refreshClusters();
            const _map = this.$refs.map.mapObject;
            
            
            _map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    
                    console.log(layer);
                }
            });
        },
        async removeAllMarkers() {
            const _map = this.$refs.map.mapObject;
            _map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    if (_map.getBounds().contains(layer.getLatLng())) {
                        _map.removeLayer(layer);
                    }
                }
            });
        },  
        async removeLayer(layerToRemove) {
            let layerGroups = Object.assign([], this.map.layerGroups);

            layerGroups = layerGroups.filter(lg => lg.id !== layerToRemove.id);

            if (!layerGroups.length) {
                this.$store.dispatch('updateLegend', false);
                this.removeAllMarkers();
            }

            this.map.layerGroups = layerGroups;
        },
        async clearMapData() {            
            this.removeAllMarkers();

            this.removePolygonsPattern();

            this.$store.dispatch('updateMap', {});

            this.$store.dispatch('updateLegend', false);
            
            if (isEmpty(this.map.layerGroups) && !this.loading) {
                const snackbar = { open: true, color: '', text: 'no_info_to_remove', timeout: 2500, type: 'warning' };
                this.$store.dispatch('updateSnackbar', snackbar);
            }

            this.map.layerGroups = [];
        },
        async removePolygonsPattern() {
            try {
                let svg = document.getElementsByTagName('svg')[0];
                if (!svg) return;
                let defs = svg.getElementsByTagName('defs');
                if (!defs) return;
                
                while (svg.childNodes[1]) {
                    for (let def of defs) {
                        svg.removeChild(def)
                    }
                }
            } catch (error) {
                console.error(error);
            }            
        },
        checkLayerRequirements(layer, dates) {
            let hasRequirement = false;

            const { extra_props, style } = layer;

            if (style.extra_props) {
                if (style.extra_props.required_filters && !isEmpty(style.extra_props.required_filters)) {
                    let hasFilterSelected = false;
                    layer.filters.map(filter => {
                        if (style.extra_props.required_filters.includes(filter.name)) {
                            if (!isEmpty(filter.values)) {
                                hasFilterSelected = true;
                            }
                        }
                    });

                    if (hasFilterSelected) return false;

                    const snackbar = { open: true, color: '', text: 'no_filter_selected', timeout: 2500, type: 'warning' };
                    this.$store.dispatch('updateSnackbar', snackbar);
                    layer.selected = false;    
                    hasRequirement = true;
                    console.log('requirement: required filters - ' + style.extra_props.required_filters);
                }

                // caso a camada seja single date
                if (style.extra_props && style.extra_props.single_date && dates[0] !== dates[1]) {
                    const snackbar = { open: true, color: '', text: 'no_single_date_selected', timeout: 2500, type: 'warning' };
                    this.$store.dispatch('updateSnackbar', snackbar);
                    layer.selected = false;    
                    hasRequirement = true;
                    console.log('requirement: single date - ' + style.extra_props.single_date);
                }

                // TODO - add ifs para outros requirements quando existir
            }
            return hasRequirement;
        },
        async loadLayer(layer, dates) {
            return new Promise((resolve, reject) => {
                this.updateLoading(true);

                const { id, selected, name, editable, extra_props } = layer;
                        
                if (!selected) return;
    
                dates = this.getDates(dates);

                if (this.checkLayerRequirements(layer, dates)) {
                    setTimeout(() => { this.updateLoading(false) }, 50);
                    return reject(null);
                }

                let dt_start = dates[0];
                let dt_end = dates[1];

                let url = getApi(`layer/${id}/feature?`); 
                url += this.getLayerFilters(layer);

                let data = { id_layer: id, dt_start: dt_start, dt_end: dt_end };
                

                axios.get(url, { params: data }).then(response => { 
                    const { data, errors } = response.data;

                    if (!isEmpty(errors)) {
                        //this.loading = false;
                        this.updateLoading(false);
                        return getErrors(errors);
                    }

                    const { features, items } = data;

                    if (isEmpty(features)) {
                        const snackbar = { open: true, color: '', text: 'no_features_founded', timeout: 2500, type: 'success' };
                        //this.loading = false;
                        this.updateLoading(false);
                        return this.$store.dispatch('updateSnackbar', snackbar);
                    }


                    let LAYER_FEATURES = {
                        polygon: [],
                        imageOverlay: [],
                        marker: [],
                        point: [],
                    };

                    
                    features.map(async (f) => { 
                        try {                            
                            const feature = await this.getFeature(f, layer);    
                            
                            if (isEmpty(feature.fields)) return reject();

                            if (feature.type === 'POLYGON') LAYER_FEATURES.polygon.push(feature);
                            else if (feature.type === 'IMAGE_OVERLAY') LAYER_FEATURES.imageOverlay.push(feature);
                            else if (feature.type === 'MARKER') LAYER_FEATURES.marker.push(feature);
                            else if (feature.type === 'POINT') LAYER_FEATURES.point.push(feature);
                        } catch (error) {
                            console.error(error);
                            return reject(null)
                        }
                    });

                    const layerType = layer.style.types.find(lt => lt.value);
                    if (['point','marker'].includes(layerType.name)) {
                        Object.keys(LAYER_FEATURES).map(key => {
                            if (key !== layerType.name) LAYER_FEATURES[key] = [];
                        })
                    }

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
                    
                    // ADD LAYER INFORMATIONS BY REQUEST
                    layer.features = features;
                    layer.legend = items;
                    layer.layerGroup = LAYER_FEATURES;

                    const newLayers = Object.assign([], this.$store.getters.layers);

                    newLayers.map(section => {
                        section.layers.map(l => {
                            if (l.id === layer.id) l = layer;
                        })
                    });

                    this.$store.dispatch('updateLayers', newLayers);

                    this.map.layerGroups.push(layerGroup);
                    const layerGroups = this.map.layerGroups;

                    this.$store.dispatch('updateMap', { layerGroups });
                    
                    //this.loading = false;
                    this.updateLoading(false);

                    const snackbar = { open: true, color: '', text: 'success_load_features', timeout: 2500, type: 'success' };
                    this.$store.dispatch('updateSnackbar', snackbar);

                    this.$store.dispatch('updateLegend', true);

                    resolve(true);
                }).catch(() => {
                    const newLayers = Object.assign([], this.$store.getters.layers);

                    newLayers.map(section => {
                        section.layers.map(l => {
                            if (l.id === layer.id) l.selected = false;
                        });
                    });

                    this.$store.dispatch('updateLayers', newLayers);

                    //this.loading = false
                    this.updateLoading(false);
                    
                    // reject(null);
                });
            }).catch(error => console.error(error));
            //this.loading = true;
           
        },
        updateLoading(value) {
            const map = this.$store.getters.map;
            this.$store.dispatch('updateMap', { ...map, loading: value });
        },
        async loadFeatures() {
            this.updateLoading(true);
            
            await this.clearMapData();

            const currentStoreLayers = this.$store.getters.layers;
            const currentStoreDates = this.$store.getters.dates;
            
            const sections = Object.assign([], currentStoreLayers);
            let dates = currentStoreDates;
            
            const hasSelectedLayers = this.getSelectedLayers();       
                                    
            if (isEmpty(dates) || isEmpty(hasSelectedLayers)) {
                const snackbar = { open: true, color: '', text: 'no_layer_selected', timeout: 2500, type: 'warning'};
                this.$store.dispatch('updateSnackbar', snackbar);
                this.updateLoading(false);
                return;
            }

            sections.map(section => {
                section.layers.map(layer => {
                    this.loadLayer(layer, dates);
                });
            });
        },
        openDrawDialog(marker, layerGroup) {
            const { isOnEditableLayer, idLayer } = marker;
            
            if (isOnEditableLayer) {
                let layer = null;
                const sections = Object.assign([], this.$store.getters.layers);
                sections.map(section => {
                    section.layers.map(l => {
                        if (l.id === idLayer) layer = l;
                    })
                });

                if (!layer) return;

                let newFilters = [];
                layer.filters.map(filter => {
                    marker.fields.map(field => {
                        if (field.field_config_id === filter.id) {
                            newFilters.push({
                                ...filter,
                                key: field.key,
                                value: field.value
                            });
                        }
                    });
                });
                layer.filters = newFilters;

                let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
                
                newDrawDialog = {
                    open: true,
                    layer: layer,
                    feature: marker, 
                    type: 'EDIT'
                }             

                this.$store.dispatch('updateDrawDialog', newDrawDialog);
            }
        },
        heatMapColorforValue(value){
            var h = (1.0 - value) * 240;
            console.log(h);
            return `hsl(${h}, 100%, 50%)`;
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
            const { id, name, properties, geometry, label, style, type, fields } = feature;
                        
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

            switch (type) {
                case 'POLYGON': {
                    const { color, fillColor, fillOpacity, opacity, weight } = style;

                    let polygonColor = color;
                    let polygonFillColor = fillColor;
                    
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
                    
                    
                    let gradientString = '';
                    let colorFillPallete = this.hslToHex(polygonColor);

                    if (layer.style.texture.value === "HORIZONTAL") {
                        gradientString = getGradientPattern(layer, colorFillPallete, "HORIZONTAL");
                    } else if (layer.style.texture.value === "VERTICAL") {
                        gradientString = getGradientPattern(layer, colorFillPallete, "VERTICAL");
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


                    // SELF REFERENCE
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

                    // MOUNT POPUP TEXT
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

                    // define default icon, if there is a image on
                    // feature properties, then replace it
                    let iconUrl = require(`../../assets/icons/${icon}.png`);
                    if (image && !isEmpty(image)) iconUrl = image;                    

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
        async getSvgString(url) {
            //return await download(url);
        },
        onMouseEnterImageOverlay(e, imageOverlay) {
            const element = e.originalEvent.target;
            const position = element.getBoundingClientRect();
            this.featureInformation = {
                open: true,
                position,
                element,
                data: imageOverlay
            }
        },
        onMouseLeaveImageOverlay() {
            this.featureInformation = {
                open: false,
                position: null,
                element: null,
                data: null
            }
        },
        getDates(dates) {    
            if (dates.length === 1) dates[1] = dates[0]; // garante que há sempre 2 datas selecionadas

            if (moment(dates[0]).isAfter(moment(dates[1]))) dates = [dates[1], dates[0]]; // arrumar ordem da data caso data 1 > data 0

            return dates;
        }, 
        getSelectedLayers() {
            return getSelectedLayers();
        },
        clearHighlightedFeatures() {
            try {
                const _map = this.$refs.map.mapObject;
                _map.eachLayer(layer => {
                    if(layer instanceof L.Polygon && _map.getBounds().contains(layer.getLatLngs())) {
                        const { defaultStyle } = layer.options;
                        if (defaultStyle) {
                            layer.setStyle({
                                ...layer.options,
                                color: defaultStyle.color,
                                fillColor: defaultStyle.fillColor,
                                opacity: defaultStyle.opacity,
                                fillOpacity: defaultStyle.fillOpacity,
                                weight: defaultStyle.weight
                            });
                        } else {
                            layer.setStyle({
                                ...layer.options,
                                color: layer.options.color,
                                fillColor: layer.options.fillColor,
                                opacity: layer.options.opacity,
                                fillOpacity: layer.options.fillOpacity,
                                weight: layer.options.weight
                            });
                        }
                        
                    }
                });
            } catch (error) {
                console.error(error);
            }
        },
        highlightFeature(feature) {
            try {
                const _map = this.$refs.map.mapObject;
                _map.eachLayer(layer => {
                    if((layer instanceof L.Polygon) && _map.getBounds().contains(layer.getLatLngs())) {
                        if (layer.options.id === feature.id) {
                            layer.setStyle({
                                ...layer.defaultStyle,
                                weight: 3,
                                color: 'teal', 
                                fillColor: 'teal',
                            });
                        }
                    }

                    if ((layer instanceof L.ImageOverlay) && _map.getBounds().contains(layer.getBounds())) {
                        if (layer.options.id === feature.id) {

                            layer.setStyle({
                                weight: 3,
                                color: 'teal', 
                                //fillColor: 'teal',
                                stroke: true
                            });
                        }
                    }
                });
            } catch (error) {
                console.error(error);
            }
        },
        openPopup(feature) {
            this.clearHighlightedFeatures();
            this.highlightFeature(feature);

            //this.loading = true;
            this.updateLoading(true);

            let dates = this.$store.getters.dates;

            dates = this.getDates(dates);

            let dt_start = dates[0];
            let dt_end = dates[1];
            
            const { idLayer, id } = feature;

            
            let url = getApi(`feature/${id}/chart`, { id_layer: idLayer, dt_start: dt_start, dt_end: dt_end });
            axios.get(url).then(response => {
                const { data, errors } = response.data;

                if(!isEmpty(errors)) {
                    //this.loading = false;
                    this.updateLoading(false);
                    return getErrors(errors);
                }

                const { tabs } = data;

                this.popup = {
                    ...this.popup,
                    tray: false,
                    open: true,
                    data: feature, 
                    tabs: tabs
                };

                //this.loading = false;
                this.updateLoading(false);
            }).catch(error => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_api', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                //this.loading = false;
                this.updateLoading(false);
            })

            

            try {
                const hasPopup = document.querySelector('.opacity-95'); // possui popup
                if (!hasPopup) return;

                const dialog = document.querySelector('.opacity-95').parentNode;
                const popupHeader = document.querySelector('.popup-header');
                dialog.style.top = 'unset';
                popupHeader.style.bottom = 'unset';
                popupHeader.style.top = '0px';
            } catch (error) {
                console.error(error);
            }
        },
        closePopup() {
            this.popup = { 
                ...this.popup,
                open: false, 
                data: null, 
                charts: [],
            };
            this.clearHighlightedFeatures();
        }
    },
    computed: {
        getMap() {
            return this.$store.getters.map;
        }
    }
}