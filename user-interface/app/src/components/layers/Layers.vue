<template>
    <div class="layers">
        <div
            v-for="(menuItem, key) in menuItems"
            :key="key"
        >
            <div v-if="menuItem.layers && hasActiveLayers(menuItem.layers)" class="layers-menu-items">
                <div class="section">
                <div class="section-header">
                    <v-icon>{{ menuItem.icon }}</v-icon>
                    <span>{{ getLabel(menuItem, $i18n.locale) }}</span>
                </div>
                <div 
                    v-for="(layer, layerIndex) in menuItem.layers" 
                    :key="layerIndex"
                    class="layer-menu-item"
                    v-show="layer.active"
                >
                    <div :style="!getMap.loading ? getColorStyle(layer) : ''">{{ getLabel(layer, $i18n.locale) }}</div>
                    <div class="layer-menu-item-actions">
                       
                        <v-menu
                            bottom
                            right
                            :offset-x="true"
                            :content-class="`layer-menu-options-${layer.id}`"
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                    icon
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="changeOptionsStyle(layer)"
                                    :class="`options-${layer.id}-button`"
                                    v-show="layer.configurable"
                                    :color="layer.selected ? '#52FFEE' : '#FFFFFF'"
                                    :disabled="getMap.loading"
                                >
                                    <v-icon>mdi-cog</v-icon>
                                </v-btn>
                            </template>

                            <v-sheet class="layer-menu-item-options" @click="(e) => e.stopPropagation()"  v-if="layer.style">
                                <v-card class="layer-menu-item-options-content" elevation="2" outlined shaped>
                                    <div class="layer-type">
                                        <div class="options-header">
                                            <span>{{ $t('type') }}</span>
                                           
                                            <div class="options-header-actions">
                                                <v-btn icon @click="resetLayerType(layer)">
                                                    <v-icon>
                                                        mdi-rotate-left
                                                    </v-icon>
                                                </v-btn>
                                                <v-btn icon @click="searchLayer(layer)">
                                                    <v-icon>
                                                        mdi-arrow-right-bold-circle-outline
                                                    </v-icon>
                                                </v-btn>
                                            </div>
                                        </div>
                                        <v-card elevation="2" outlined shaped class="options-wrapper">
                                            <div class="options-types">         
                                                <div v-for="type in layer.style.types" :key="type.name">
                                                    <v-tooltip top>
                                                        <template v-slot:activator="{ on, attrs }">
                                                            <v-btn
                                                                v-bind="attrs"
                                                                v-on="on"
                                                                icon
                                                                @click="changeLayerType(layer, type)"

                                                            >
                                                                <v-icon :color="type.value ? '#52FFEE' : ''">{{ type.icon }}</v-icon>
                                                            </v-btn>
                                                        </template>
                                                        <span>
                                                            {{ $t(type.label) }}
                                                        </span>
                                                    </v-tooltip>
                                                </div>                                  
                                            </div>
                                            <div class="options-scale">
                                                <div class="color-picker" v-for="type in layer.style.types" :key="type.name" v-show="type.name === 'hexagon' && type.value === true">
                                                    <ColorPicker 
                                                        :type="type" 
                                                        :colorScale="layer.style.colorScale.polygon" 
                                                        v-if="type.name === 'hexagon' && type.value === true" 
                                                        :layer="layer"
                                                    />
                                                </div>
                                            </div>     
                                        </v-card>
                                    </div>
                                    <div class="texture">
                                        <div class="options-header">
                                            <span>{{ $t('texture') }}</span>
                                           
                                            <div class="options-header-actions">
                                                <v-btn icon @click="resetLayerTexture(layer)">
                                                    <v-icon>
                                                        mdi-rotate-left
                                                    </v-icon>
                                                </v-btn>
                                                <v-btn icon @click="searchLayer(layer)">
                                                    <v-icon>
                                                        mdi-arrow-right-bold-circle-outline
                                                    </v-icon>
                                                </v-btn>
                                            </div>
                                        </div>
                                        <v-card elevation="2" outlined shaped class="options-wrapper">
                                            <div class="options-textures">                                                
                                                <v-radio-group row v-model="layer.style.texture.value" @change="changeLayerTexture(layer)">
                                                    <v-radio color="#52FFEE" v-for="t in layer.style.texture.options" :key="t" :value="t">
                                                        <template v-slot:label>
                                                            <div :class="`box-color texture-${t}`" />
                                                        </template>
                                                    </v-radio>
                                                </v-radio-group>
                                            </div>
                                        </v-card>
                                    </div>                                    
                                </v-card>
                            </v-sheet>
                        </v-menu>


                        <v-btn 
                            v-if="layer.editable"
                            icon
                            @click="openDrawDialog(layer)"
                            :color="layer.selected ? '#52FFEE' : '#FFFFFF'"
                            :disabled="getMap.loading"
                        >
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>

                        <v-menu
                            bottom
                            right
                            :offset-x="true"
                            :content-class="`layer-menu-filter-${layer.id}`"
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                    icon
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="changeFilterStyle()"
                                    :class="`filter-${layer.id}-button`"
                                    v-show="layer.filters.length"
                                    :color="layer.selected ? '#52FFEE' : '#FFFFFF'"
                                    :disabled="getMap.loading"
                                >
                                    <v-icon>mdi-filter</v-icon>
                                </v-btn>
                            </template>

                            <v-sheet class="layer-menu-item-filter" @click="(e) => e.stopPropagation()">
                                <v-card class="layer-menu-item-filter-content" elevation="2" outlined shaped>
                                    <div 
                                        v-for="(filter, i) in layer.filters"
                                        :key="i"
                                    >
                                        <div class="filter-header">
                                            <span>{{ getLabel(filter, $i18n.locale) }}</span>
                                            <div class="filter-header-actions">
                                                <v-btn icon @click="(e) => resetFilter(e, filter)">
                                                    <v-icon>
                                                        mdi-rotate-left
                                                    </v-icon>
                                                </v-btn>
                                                <v-btn icon @click="searchLayer(layer)">
                                                    <v-icon>
                                                        mdi-arrow-right-bold-circle-outline
                                                    </v-icon>
                                                </v-btn>
                                            </div>
                                        </div>
                                        <v-card elevation="2" outlined shaped class="filters-wrapper">
                                            <v-chip
                                                v-for="item in filter.items"
                                                :key="item.id"
                                                class="ma-2"
                                                :close="item.selected ? true : false"
                                                @click="(e) => selectFilterItem(e, item)"
                                                @click:close="(e) => uncheckFilterItem(e, item)"
                                                small
                                                :color="item.selected ? 'teal' : 'gray'"
                                                
                                            >
                                                    <v-avatar left>
                                                        <v-icon>{{ item.selected ? 'mdi-checkbox-marked-circle' : 'mdi-alert-circle-outline' }}</v-icon>
                                                    </v-avatar>
                                                    {{ getLabel(item, $i18n.locale) }}
                                            </v-chip>
                                        </v-card>
                                    </div>
                                </v-card>
                            </v-sheet>
                        </v-menu>
                        
                        <v-btn icon @click="() => toggleSelectedLayer(layer)" :color="layer.selected ? '#52FFEE' : '#FFFFFF'" :disabled="getMap.loading">
                            <v-icon>{{ layer.selected ? `mdi-eye` : `mdi-eye-off`}}</v-icon>
                        </v-btn>

                     

                        
                    </div>
                </div>
            </div>
            </div>
        </div>
           <!-- DIALOG DRAW -->
            <v-dialog
                v-model="drawDialog.open"
                width="500"
                @click:outside="closeDrawDialog()"
                v-if="drawDialog.open"
            >
                <v-card outlined shaped class="dialog-card">
                    <v-toolbar
                        color="teal"
                    >
                        <div class="headline">{{ getLabel(drawDialog.layer, $i18n.locale) }}</div>
                        <v-spacer></v-spacer>
                        <v-btn icon @click="closeDrawDialog()">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </v-toolbar>
                    <Loading color="primary" type="linear" v-if="loading || getMap.loading" />

                    <v-divider></v-divider>

                    <div class="dialog-card-content">
                        <div v-if="drawDialog.type === 'CREATE'">
                            <div 
                                class="layer-fields"
                                v-for="field in drawDialog.layer.filters"
                                :key="field.id"
                            >
                                <div class="field-item" v-if="field.visible">
                                    <div v-if="['text', 'password', 'number'].includes(field.type)">
                                        <v-text-field
                                            :name="field.name"
                                            :label="getLabel(field, $i18n.locale)"
                                            :type="field.type"
                                            v-model="field.key"
                                            outlined
                                            dense
                                            autocomplete="off"
                                        />
                                    </div>

                                    <div v-if="field.type === 'textarea'">
                                        <v-textarea
                                            :label="getLabel(field, $i18n.locale)"
                                            v-model="field.key"
                                            solo
                                            :name="field.name"
                                            no-resize
                                            outlined
                                            autocomplete="off"
                                        />
                                    </div>

                                    <div v-if="field.type === 'boolean'">
                                        <v-switch
                                            v-model="field.key"
                                            :label="getLabel(field, $i18n.locale)"
                                        />
                                    </div>

                                    <div v-if="field.type === 'date'">
                                       <v-date-picker
                                            v-model="field.key"
                                            range
                                        ></v-date-picker>
                                    </div>

                                    <div v-if="field.type === 'image'">
                                        <v-row class="align-center">
                                        <v-col cols="10">
                                            <v-file-input
                                                
                                                :truncate-length="100"
                                                :label="getLabel(field, $i18n.locale)"
                                                v-model="file"
                                                @change="value => onChangeFile(value)"
                                            />
                                        </v-col>
                                        <v-col cols="2">
                                            <v-btn fab  small color="teal" class="mx-auto" @click="getFileURL(field)" :disabled="loading || getMap.loading">
                                                <v-icon v-if="!loading">mdi-upload</v-icon>
                                                <v-progress-circular
                                                    v-else
                                                    indeterminate
                                                    color="teal"
                                                ></v-progress-circular>

                                            </v-btn>
                                        </v-col>
                                        </v-row>
                                    </div>
                                    
                                    


                                </div>
                            </div>                         
                    </div>
                    

                    <div v-if="drawDialog.type === 'EDIT'">
                      
                            <div 
                                    class="layer-fields"
                                    v-for="field in drawDialog.layer.filters"
                                    :key="field.id"
                            >
                                    <div class="field-item" v-if="field.visible">
                                        <div v-if="['text', 'password', 'number'].includes(field.type)">
                                            <v-text-field
                                                :name="field.name"
                                                :label="getLabel(field, $i18n.locale)"
                                                :type="field.type"
                                                :value="field.key"
                                                outlined
                                                dense
                                                autocomplete="off"
                                                @change="(value) => field.key = value"
                                            />
                                        </div>

                                        <div v-if="field.type === 'textarea'">
                                            <v-textarea
                                                :label="getLabel(field, $i18n.locale)"
                                                :value="field.key"
                                                solo
                                                :name="field.name"
                                                no-resize
                                                outlined
                                                autocomplete="off"
                                                @change="(value) => field.key = value"
                                            />
                                        </div>

                                        <div v-if="field.type === 'boolean'">
                                            <v-switch
                                                :value="field.key"
                                                :label="getLabel(field, $i18n.locale)"
                                                @change="(value) => field.key = value"
                                            />
                                        </div>

                                        <div v-if="field.type === 'date'">
                                                <v-date-picker
                                                    :value="field.key"
                                                    range
                                                    @change="(value) => field.key = value"
                                                ></v-date-picker>
                                        </div>

                                        <div v-if="field.type === 'image'">
                                            <v-row class="align-center">
                                                <v-col cols="10">
                                                    <v-file-input
                                                        
                                                        
                                                        :truncate-length="100"
                                                        :label="getLabel(field, $i18n.locale)"
                                                        :value="getFile(field)"
                                                        @change="value => onChangeFile(value)"
                                                    />
                                                </v-col>
                                                <v-col cols="2">
                                                    <v-btn fab  small color="teal" class="mx-auto" @click="getFileURL(field)" :disabled="loading || getMap.loading">
                                                        <v-icon v-if="!loading">mdi-upload</v-icon>
                                                        <v-progress-circular
                                                            v-else
                                                            indeterminate
                                                            color="teal"
                                                        ></v-progress-circular>

                                                    </v-btn>
                                                </v-col>
                                            </v-row>
                                        </div>

                    

                                    </div>
                            </div>
                            
                    </div>

                    </div>


                    <v-divider></v-divider>

                    <v-card-actions class="pa-3 dialog-action-buttons">
                        <div class="timeline">
                        <v-btn
                            v-if="drawDialog.feature && drawDialog.type === 'EDIT'"
                            class="mx-2"
                            fab
                            small
                            color="teal"
                            ripple
                            @click="openTimeline()"
                            :disabled="loading || getMap.loading"
                        >
                            <v-icon>mdi-timer</v-icon>
                        </v-btn>
                        </div>

                        <div class="actions">
                        <v-btn
                            v-if="drawDialog.feature && drawDialog.type === 'EDIT'"
                            
                            color="red"
                            filled
                            ripple
                            width="110"
                            small
                            @click="deleteMarker()"
                            :disabled="loading || getMap.loading"
                        >
                            {{ $t('dialog_btn_delete') }}
                        </v-btn>

                        <v-btn
                            @click="drawPointInMap()"
                            color="green"
                            filled
                            ripple
                            width="110"
                            small
                            :disabled="loading || getMap.loading"
                            v-if="drawDialog.type === 'CREATE'"
                        >
                            {{ $t('dialog_btn_draw') }}
                        </v-btn>

                        
                        <v-btn
                            @click="editPoint()"
                            color="green"
                            filled
                            ripple
                            width="110"
                            small
                            :disabled="loading || getMap.loading"
                            v-if="drawDialog.type === 'EDIT'"
                        >
                            {{ $t('dialog_btn_edit') }}
                        </v-btn>

                        <v-btn 
                            class="mx-2"
                            fab
                            small
                            color="primary"
                            ripple
                            @click="drawPointInMap()"
                            v-if="drawDialog.type === 'EDIT'"
                        >
                            <v-icon>
                                mdi-map-marker
                            </v-icon>
                        </v-btn>
                        </div>
                    </v-card-actions>
                </v-card>
            </v-dialog>

       

            <Timeline 
                v-if="timeline" 
                :timeline="timeline"
                :closeTimeline="closeTimeline"
            />
    </div>
</template>

<script>
import L from 'leaflet';
import axios from 'axios';
import { s3, addPhoto } from '../../aws/aws';
import { isEmpty } from 'lodash';
import { getApi, getErrors, getLabel, getSelectedLayers } from '../../utils';
import ColorPicker from '../color-picker/ColorPicker.vue';
import Timeline from '../timeline/Timeline.vue';
import Loading from '../loading/Loading.vue';

export default {
    name: 'Layers',
    props: ['loadFeatures', 'clearMapData', 'removeLayer'],
    components: { ColorPicker, Timeline, Loading },
    data() {
        return {
            timeline: false,
            layerRectOptions: null,
            file: null,
            reader: null,
            loading: false,
        }
    },
    mounted() {
        
    },
    methods: {
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
                
                this.loadFeatures()
            })
            
            .catch(error => {
                console.error(error);
                //this.loading = false;
                this.updateLoading(false);

                const snackbar = { open: true, color: '', text: 'error_edit_interest_point', timeout: 2500, type: 'error' };                         
                this.$store.dispatch('updateSnackbar', snackbar);                

                return this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: true });
            });

        },
        // clearFile(field) {
        //     field.key = '';
        //     var f = new File([""], field.key);
        //     this.file = f;
        // },
        getFile(field) {
            if (!this.file) {
                var f = new File([""], field.key);
                this.file = f;
            }
            return this.file;
        },
        async getFileURL(field) {
            console.log(field);
            this.loading = true;

            if (!this.reader || !this.file) {
                this.loading = false;
                const snackbar = { open: true, color: '', text: 'warning_send_file', timeout: 2500, type: 'warning' };
                return this.$store.dispatch('updateSnackbar', snackbar);           
            }

            if (!this.reader) return this.loading = false;
            
            const { name, data } = this.reader;

            
            // FILE TO BUFFER
            const buffer = new Buffer(data.replace(/^data:image\/\w+;base64,/, ""),'base64');

            // const uploadFile = await addPhoto(buffer, name);

            // if (uploadFile) {
            //     this.loading = false;
            //     const snackbar = { open: true, color: '', text: 'success_send_file', timeout: 2500, type: 'success' };
                
            //     var f = new File([""], uploadFile.Location);
            //     this.file = f;     
            //     field.key = f.name;       

            //     return this.$store.dispatch('updateSnackbar', snackbar);           
            // } else {
            //     this.loading = false;
            //     const snackbar = { open: true, color: '', text: 'fail_send_file', timeout: 2500, type: 'error' };
            //     return this.$store.dispatch('updateSnackbar', snackbar);           
            // }


            //addPhoto(file);
            
            // setTimeout(() => {
            //     var f = new File([""], "url");
            //     this.file = f;     
            //     field.key = f.name;       
            //     this.loading = false;
            // }, 1000);
        },
        onChangeFile(value) {
            if (!value) return;
            const fr = new FileReader();
            fr.readAsDataURL(value);
            fr.addEventListener('load', () => {
                this.reader = { name: value.name, data: fr.result }
            });
        },
        getColorStyle(layer) {
            if (this.$vuetify.theme.dark) {
                return layer.selected ? 'color: #52FFEE' : 'color: #FFFFFF';
            }
            return layer.selected ? 'color: teal' : 'color: #181818';
        },
        closeTimeline() {
            this.timeline = false;
        },
        getLabel(item, language) {
            return getLabel(item, language);
        },
        getField(field) {
            let featureData = { label: { en: '--', pt: '--' }, key: '--'};

            let featureFields = this.$store.getters.drawDialog;
            const { feature } = featureFields;
            

            const hasData = feature.fields.find(ff => ff.field_config_id === field.id);
            if (!hasData) return featureData;
            
            feature.fields.map(ff => {
                if (ff.field_config_id === field.id) {
                    let value = ff.key;
                                      
                    field.key = value;
                    featureData = {
                        ...ff,
                        key: value,
                        label: field.label,
                    }
                }
            });
            
            return featureData;
        },
        openTimeline() {
            this.timeline = open;  
        },
        changeLayerTexture(layer) {
        
        },
        resetLayerType(layer) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(l => {
                    if (l.id === layer.id) {
                        l.style.types.map((t, index) => {
                            t.value = false;
                            if (index === 0) t.value = true;
                            const menu = document.querySelector(`.layer-menu-options-${layer.id}`);
                            const menuTop = this.layerRectOptions.top;
                            menu.style.top = `${menuTop}px`;        
                        });
                    }
                })
            })
            
            this.$store.dispatch('updateLayers', newSections);    
        },
        resetLayerTexture(layer) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(l => {
                    if (l.id === layer.id) {
                        l.style.texture.value = 'NONE';
                    }
                })
            });
            
            this.$store.dispatch('updateLayers', newSections);    
        },
        changeLayerType(layer, type) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(l => {
                    if (l.id === layer.id) {
                        l.style.types.map(t => {
                            t.value = false;
                            if (t.name === type.name) {
                                const menuConfigurableHeight = 160;   
                                const menu = document.querySelector(`.layer-menu-options-${layer.id}`);
                                const menuTop = this.layerRectOptions.top;

                                if (t.name === 'hexagon') {
                                    if (this.layerRectOptions.top + this.layerRectOptions.y + menuConfigurableHeight >= window.screen.height) {
                                        menu.style.top = `${menuTop - menuConfigurableHeight}px`;                       
                                    }
                                } else {
                                    menu.style.top = `${menuTop}px`;        
                                }

                                t.value = true;
                            }
                            
                            
                        });
                    }
                });
            });
            
            this.$store.dispatch('updateLayers', newSections);    
        },
        async removeFeatureFromMap(id) {
            const _map = window._map;
            _map.eachLayer(layer => {
                if(layer instanceof L.Marker) {
                    if(_map.getBounds().contains(layer.getLatLng())) {
                        if (layer.options.id === id) {
                            _map.removeLayer(layer);
                        }
                    }
                }
            });
        },
        deleteMarker() {
            this.loading = true;

            const snackbar = { open: true, color: '', text: 'removing_data', timeout: 2500, type: 'warning' };
            this.$store.dispatch('updateSnackbar', snackbar);           
      
            
            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            
            const { feature: { id } } = newDrawDialog;
            
            let url = getApi(`feature/${id}`);   
            axios.delete(url).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }
                
                this.removeFeatureFromMap(id);
                const refs = window._refs;
                refs.markerClusterRef[0].mapObject.refreshClusters();
                    
                newDrawDialog = { 
                    open: false, 
                    layer: null,
                    feature: null,
                    type: ''
                }


                this.$store.dispatch('updateDrawDialog', newDrawDialog); 
                const snackbar = { open: true, color: '', text: 'success_delete_interest_point', timeout: 2500, type: 'success' };
                this.$store.dispatch('updateSnackbar', snackbar);
                
                this.loading = false;

                this.loadFeatures();
                
            }).catch(error => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_delete_interest_point', timeout: 2500, type: 'error' };
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
            });
        },
        editPoint() {
            const drawDialog = this.$store.getters.drawDialog;
            const { layer, feature } = drawDialog;

            const newLayer = Object.assign({}, layer);
            const { id, filters, style } = newLayer;

            let language = this.$i18n.locale;
            
            let isFormFilled = true;
            //let hasFile = true;
            filters.map(filter => {
                if ((!filter.key || filter.key === '') && filter.type !== 'image') {
                    isFormFilled = false;
                }
            });

            if (!isFormFilled) {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' }; 
                return this.$store.dispatch('updateSnackbar', snackbar);  
            } 
              
            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: false }); // FECHA DIALOG DE DRAW SEM PERDER INFO
            
            const { extra_props } = style;

            let properties = {};
            if (extra_props) {
                if (extra_props.marker) {
                    Object.keys(extra_props.marker).map(key => properties[key] = extra_props.marker[key]);
                }
            }
            
            let popupText = ``;
            let fields = [];
            
            filters.map(filter => {
                const { id, name, key } = filter;
                
                fields.push({ key: key, value: "1", field_config_id: id  });
                let fieldName = filter.label && filter.label[language] ? filter.label[language] : filter.name;

                let row = '';
                if (filter.type === 'image') {
                    row += `${fieldName}: <a href='${key}' target='_blank'>${key}</a> <br />`;
                } else {
                    row += `${fieldName}: ${key} <br />`;
                }

                popupText += row;
            });


            let newFeatureData = Object.assign({}, this.$store.getters.featureData);
            let feature_collections = JSON.parse(sessionStorage.getItem('featureCollections'))[0];

            newFeatureData = {
                ...newFeatureData,
                layer_id: id,
                tenant_id:  process.env.VUE_APP_TENANT,
                feature_collection_id: feature_collections.id,
                language: this.$i18n.locale,
                fields,
                properties,
                popup: popupText,
                geometry: feature.geometry,
                type: feature.type,
            };

            this.$store.dispatch('updateFeatureData', newFeatureData);

            this.editMarkerFeature(newFeatureData);
            
        },
        drawPointInMap() {     
            const { layer } = this.drawDialog;

            const newLayer = Object.assign({}, layer);
            const { id, filters, style } = newLayer;

            let language = this.$i18n.locale;
            
            let isFormFilled = true;
            let hasFile = true;
            filters.map(filter => {
                if ((!filter.key || filter.key === '') && filter.type !== 'image') {
                    isFormFilled = false;
                }

                // if (filter.key === '' && filter.type === 'image') {
                //     hasFile = false;
                // }

                // if (!this.file) {
                //     hasFile = false;
                // }
            });

            if (!hasFile) {
                const snackbar = { open: true, color: '', text: 'warning_upload_file', timeout: 2500, type: 'warning' }; 
                return this.$store.dispatch('updateSnackbar', snackbar);  
            }

            if (!isFormFilled) {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' }; 
                return this.$store.dispatch('updateSnackbar', snackbar);  
            } 
              
            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: false }); // FECHA DIALOG DE DRAW SEM PERDER INFO
            
            const { extra_props } = style;

            let properties = {};
            if (extra_props) {
                if (extra_props.marker) {
                    Object.keys(extra_props.marker).map(key => properties[key] = extra_props.marker[key]);
                }
            }
            
            let popupText = ``;
            let fields = [];
            
            filters.map(filter => {
                const { id, name, key } = filter;
                
                fields.push({ key: key, value: "1", field_config_id: id  });
                let fieldName = filter.label && filter.label[language] ? filter.label[language] : filter.name;

                let row = '';
                if (filter.type === 'image') {
                    row += `${fieldName}: <a href='${key}' target='_blank'>${key}</a> <br />`;
                } else {
                    row += `${fieldName}: ${key} <br />`;
                }

                popupText += row;
            });

            
            // CRIA MARKER PRETO DEFAULT - PRIORIZA IMAGEM SOBRE ICON EM EXTRA PROPS
            let icon = require('../../assets/icons/pin.png');
            if (!isEmpty(properties)) {
                if (!isEmpty(properties.icon) || properties.icon.trim() !== '') icon = require(`../../assets/icons/${properties.icon}`);
                if (!isEmpty(properties.image) || properties.image.trim() !== '') icon = properties.image;
            }
            
            const _map = window._map;
            var marker = new L.Draw.Marker(_map, { 
                icon: 
                    L.icon({
                        iconRetinaUrl: icon,
                        iconUrl: icon,
                        iconSize: [32, 32],
                        iconAnchor: [16, 37],
                        popupAnchor: [0, -30],
                    })
                },
            );    
            marker.enable();

            let newFeatureData = Object.assign({}, this.$store.getters.featureData);
            let feature_collections = JSON.parse(sessionStorage.getItem('featureCollections'))[0];

            newFeatureData = {
                ...newFeatureData,
                layer_id: id,
                tenant_id:  process.env.VUE_APP_TENANT,
                feature_collection_id: feature_collections.id,
                language: this.$i18n.locale,
                fields,
                properties,
                popup: popupText
            };

            this.$store.dispatch('updateFeatureData', newFeatureData);
        },
        openDrawDialog(layer) {
            this.file = null;
            layer.filters.map(filter => filter.key = '');
            const newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            this.$store.dispatch('updateDrawDialog', { ...newDrawDialog, open: true, layer: layer, type: 'CREATE', feature: null });
        },
        closeDrawDialog() {
            let newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);
            
            newDrawDialog = { open: false, layer: null, feature: null, type: '' };

            this.$store.dispatch('updateDrawDialog', newDrawDialog);
        },
        searchLayer(layer) {
            const newSections = Object.assign([], this.$store.getters.layers);
            newSections.map(section => {
                section.layers.map(l => {
                    if (l.id === layer.id) l.selected = true;
                })
            });
            this.$store.dispatch('updateLayers', newSections);
            this.loadFeatures();
            
            // fecha opções
            const optionsMenu = document.querySelector(`.layer-menu-options-${layer.id}`);
            if (optionsMenu) {
                const el = document.querySelector(`.options-${layer.id}-button`);
                el.click();
            }
            
        
            // fecha filtro
            const filterMenu = document.querySelector(`.layer-menu-filter-${layer.id}`);
            if (filterMenu) {
                const el = document.querySelector(`.filter-${layer.id}-button`);
                el.click();
            }

            
        },
        selectFilterItem(e, item) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(layer => {
                    layer.filters.map(filter => {
                        filter.items.map(filterItem => {
                            if (filterItem.id === item.id) {
                                if (filterItem.selected) { // uncheck
                                    filterItem.selected = false;    
                                    filter.values = filter.values.filter(it => it !== item.text);
                                } else { // check + add to array
                                    filterItem.selected = true;
                                    filter.values.push(filterItem.text);
                                }
                            }
                        });
                    });
                });
            });
            
            this.$store.dispatch('updateLayers', newSections);
            e.stopPropagation();
        },
        uncheckFilterItem(e, item) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(layer => {
                    layer.filters.map(filter => {
                        filter.items.map(filterItem => {
                            if (filterItem.id === item.id) {
                                if (filterItem.selected) { // uncheck
                                    filterItem.selected = false;    
                                    filter.values = filter.values.filter(it => it !== item.text);
                                }
                            }
                        });
                    });
                });
            });
            
            this.$store.dispatch('updateLayers', newSections);
            e.stopPropagation();
        },
        resetFilter(e, filter) {
            filter.items.map(item => item.selected = false);
            e.stopPropagation();
        },
        changeFilterStyle() {
            setTimeout(() => {
                const menu = document.querySelector('.map-menu');
                var rect = menu.getBoundingClientRect();
                const menuStyle = getComputedStyle(menu);
                const menuOffsetLeft = rect.left;
                const menuWidth = parseInt(menuStyle.width);
                
                const openMenu = document.getElementsByClassName('layer-menu-item-filter');
                
                for (let i = 0; i < openMenu.length; i++) {
                    const openMenuItem = openMenu[i].parentNode;
                    openMenuItem.style.left = `${menuOffsetLeft + menuWidth}px`;
                }
                
                
            }, 200);
        },
        changeOptionsStyle(layer) {
            setTimeout(() => {
                const menu = document.querySelector('.map-menu');
                const rect = menu.getBoundingClientRect();
                const menuStyle = getComputedStyle(menu);
                const menuOffsetLeft = rect.left;
                const menuWidth = parseInt(menuStyle.width);

                const settingsMenu = document.querySelector(`.layer-menu-options-${layer.id}`);
                this.layerRectOptions = settingsMenu.getBoundingClientRect();
                                
                const openMenu = document.getElementsByClassName('layer-menu-item-options');
                
                for (let i = 0; i < openMenu.length; i++) {
                    const openMenuItem = openMenu[i].parentNode;
                    openMenuItem.style.left = `${menuOffsetLeft + menuWidth}px`;
                }
                
            }, 200);
        },
        getSelectedLayers() {
            const currentStoreLayers = this.$store.getters.layers;
  
            const menu = Object.assign([], currentStoreLayers);

            const selectedLayers = [];

            menu.map(section => {
                section.layers.map(layer => {
                    if (layer.selected) selectedLayers.push(layer);
                })
            })

            return selectedLayers;
        },
        updateLoading(value) {
            const map = this.$store.getters.map;
            this.$store.dispatch('updateMap', { ...map, loading: value });
        },
        toggleSelectedLayer(selectedLayer) {
            //this.clearMapData();
            
            const currentStoreLayers = this.menuItems;

            const newSections = Object.assign([], currentStoreLayers);

            newSections.map(section => {
                section.layers.map(layer => {
                    if (layer.id === selectedLayer.id) {
                        layer.selected = !layer.selected;

                        if (layer.selected) {
                            this.updateLoading(true);
                            this.$store.dispatch('updateLayers', newSections).then(() => {
                                this.$store.dispatch('updateSelectedLayers', this.getSelectedLayers());
                            });  
                            return this.loadFeatures();
                        }

                        if (!layer.selected) {
                            this.$store.dispatch('updateLayers', newSections).then(() => {
                                this.$store.dispatch('updateSelectedLayers', this.getSelectedLayers());
                            });  
                            return this.removeLayer(layer);
                        }
                        
                    }
                });
            });
        },        
        hasActiveLayers(layers) {
            let hasActiveLayer = false;
            layers.map(layer => {
                if (layer.active) hasActiveLayer = true;
            })
            return hasActiveLayer;
        }
    },
    computed: {
        menuItems() {
            return this.$store.getters.layers;
        }, 
        drawDialog() {
            return this.$store.getters.drawDialog;
        },
        getMap() {
            return this.$store.getters.map;
        }

    }

}
</script>

<style lang="scss">


    .layers {
        overflow: auto;
        height: auto;
        //min-height: 720px;
        
        padding: 5px;
        .layers-menu-items {
            .section {
                margin: 10px 0px;
                .section-header {
                    font-size: 14px;
                    align-items: center;
                    display: flex;
                    justify-items: center;
                    gap: 10px;
                }
            }
            .layer-menu-item {
                margin: 5px 10px;
                display: flex;
                
                justify-content: space-between;
                align-items: center;
                font-size: 12px;

            }
        }
    }

    .layer-menu-item-options {
        width: 510px;
        max-height: 700px;
        padding: 10px;
        opacity: 0.9;
        .layer-menu-item-options-content {
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            overflow-x: hidden;
            gap: 5px;
            padding: 10px;
            height: 100%;
            font-size: 14px;
            .layer-menu-item-options-actions {
                display: flex;
                justify-content: flex-end;
            }

            .options-types {
                display: flex;
                justify-content: center;
                gap: 10px;
                align-items: center;
                padding: 5px;
            }

            .options-scale {
                .color-picker {
                    height: 160px;
                }
            }

            .options-textures {                
                .v-input--radio-group__input {
                    display: grid;
                    grid-auto-flow: column;
                    grid-gap: 20px;
                    justify-content: center;
                    justify-items: center;
                    align-items: center;
                }

                .box-color {
                    cursor: pointer;
                    width: 30px !important;
                    height: 30px !important;
                    min-width: 20px;
                    position: relative;
                    border: 2px solid #545454;
                    border-radius: 2px;
                    transition: .4s cubic-bezier(.25,.8,.25,1);
                }

                .texture-NONE {
                    background-color: #545454;
                }

                .texture-HORIZONTAL {
                    background-image: linear-gradient(0deg, #ffffff 25%, #545454 25%, #545454 50%, #ffffff 50%, #ffffff 75%, #545454 75%, #545454 100%);
                    position: relative;
                    border: 2px solid #545454;
                    border-radius: 2px;
                    transition: .4s cubic-bezier(.25,.8,.25,1);
                }

                .texture-VERTICAL {
                    background-image: linear-gradient(90deg, #ffffff 21.28%, #545454 21.28%, #545454 50%, #ffffff 50%, #ffffff 71.28%, #545454 71.28%, #545454 100%);
                    position: relative;
                    border: 2px solid #545454;
                    border-radius: 2px;
                    transition: .4s cubic-bezier(.25,.8,.25,1);
                }
            }
            .options-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 5px;
                .options-header-actions {
                    display: flex;
                    align-items: center;
                }
            }
            
        }
    }

    .layer-menu-item-filter {
        width: 510px;
        max-height: 700px;
        overflow-y: auto;
        padding: 10px;
        opacity: 0.9;
        .layer-menu-item-filter-content {
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            overflow-x: hidden;
            gap: 5px;
            padding: 10px;
            height: 100%;
            font-size: 14px;
            .layer-menu-item-filter-actions {
                display: flex;
                justify-content: flex-end;
            }
            .filter-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 5px;
                .filter-header-actions {
                    display: flex;
                    align-items: center;
                }
            }
        }
    }

    .dialog-card {
        overflow: hidden;
        .dialog-card-content {
            padding: 20px 20px 0px;
        }

        .dialog-action-buttons {
            display: flex;
            justify-content: space-between;
            .timeline {

            }

            .actions {
                align-items: center;
                display: flex;
                gap: 10px;
            }
        }
    }

    .dialog-timeline {
        overflow: hidden;
        .timeline-wrapper {
            overflow: hidden;
            padding: 20px;
            z-index: 999999999 !important;
        }
    }
    
</style>

