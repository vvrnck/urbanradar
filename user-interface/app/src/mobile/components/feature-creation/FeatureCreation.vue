<template>
    <div class="feature-creation-control-content" v-show="feature" > 
        <div class="leaflet-control-layers control">
            <div class="feature-menu-action" @click="toggleFeature()">
                <v-icon>mdi-close</v-icon>
            </div>
            <div class="feature-creation" v-if="draw.layer">
                <div
                    v-for="field in draw.layer.filters"
                    :key="field.id"
                >
                    <div class="field-item" v-if="field.visible">
                           <div v-if="draw.type === 'CREATE'">
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
                                            <v-col cols="9">
                                                <v-file-input
                                                    
                                                    :truncate-length="50"
                                                    :label="getLabel(field, $i18n.locale)"
                                                    v-model="file"
                                                    @change="value => onChangeFile(value)"
                                                    
                                                />
                                            </v-col>
                                            <v-col cols="1">
                                                <v-btn 
                                                    fab  
                                                    small 
                                                    color="teal" 
                                                    class="mx-auto" 
                                                    @click="getFileURL(field)" 
                                                    :disabled="loading"
                                                >
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
                <div class="actions">
                        <v-btn
                            color="red"
                            filled
                            ripple
                            width="110"
                            small
                            @click="deleteMarker()"
                            
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
                        >
                            {{ draw.type === 'EDIT' ? $t('dialog_btn_edit') : $t('dialog_btn_draw') }}
                        </v-btn>
                    </div>
            </div>
        </div>
    </div>
</template>

<script>
import L from 'leaflet';
import axios from 'axios';
import { s3, addPhoto } from '../../../aws/aws';
import { isEmpty } from 'lodash';
import { updateMobileItem, getLabel, getApi, getErrors } from '../../../utils';

export default {
    name: 'FeatureCreation',
    data() {
        return {
            loading: false,
            file: null,
            reader: null,
            timeline: false,
        }
    },
    mounted() {
        
    },
    methods: {
        drawPointInMap() {     

            const mobile = this.$store.getters.mobile;
            const layer = mobile.draw.layer;

            const newLayer = Object.assign({}, layer);
            const { id, filters, style } = newLayer;

            let language = this.$i18n.locale;
            
            let isFormFilled = true;
            let hasFile = true;
            filters.map(filter => {
                if (!filter.key || filter.key === '') {
                    isFormFilled = false;
                }

                if (filter.key === '' && filter.type === 'image') {
                    hasFile = false;
                }

                if (!this.file) {
                    hasFile = false;
                }
            });

            if (!hasFile) {
                const snackbar = { open: true, color: '', text: 'warning_upload_file', timeout: 2500, type: 'warning' }; 
                return this.$store.dispatch('updateSnackbar', snackbar);  
            }

            if (!isFormFilled) {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' }; 
                return this.$store.dispatch('updateSnackbar', snackbar);  
            } 
              
            updateMobileItem('feature', false);
            
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

            
            // CREATE DEFAULT MARKER - PRIORITIZE IMAGE OVER ICON IN EXTRA PROPS
            let icon = require('../../../assets/icons/pin.png');
            if (!isEmpty(properties)) {
                if (!isEmpty(properties.icon) || properties.icon.trim() !== '') icon = require(`../../../assets/icons/${properties.icon}`);
                if (!isEmpty(properties.image) || properties.image.trim() !== '') icon = properties.image;
            }
            
            const _map = window._map;
            console.log(_map);
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

            this.$store.dispatch('updateMobile', {
                ...mobile,
                draw: {
                    ...mobile.draw,
                    feature: newFeatureData
                }
            });
        },
        onChangeFile(value) {
            if (!value) return;
            const fr = new FileReader();
            fr.readAsDataURL(value);
            fr.addEventListener('load', () => {
                this.reader = { name: value.name, data: fr.result }
            });
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
        },
        getLabel(field, language) {
            return getLabel(field, language);
        },
        toggleFeature() {
            const mobile = this.$store.getters.mobile;
            
            updateMobileItem('feature', !mobile.toggle.feature);
        },
    },
    computed: {      
        feature() {
            const mobile = this.$store.getters.mobile;
            return mobile.toggle.feature;
        },
        draw() {
            const mobile = this.$store.getters.mobile;
            return mobile.draw;
        }
    }
}
</script>


<style lang="scss">

.feature-menu-action {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}

.feature-creation-control-content {
    position: absolute;
    top: 120px;
    width: 80%;
    height: 100px;
    z-index: 9999;
    margin: 10%;

    .feature-creation {
        .actions {
            display: flex;
            justify-content: space-evenly;
            margin-bottom: 10px;
        }
    }
}

</style>