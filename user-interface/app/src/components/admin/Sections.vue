<template>
    <div>
        <div class="justify-end" style="display: flex;">
            <v-btn
                class="mx-2"
                fab
                x-small
                color="primary"
                @click="add()"
                v-if="getUserScopes().includes('section.create')"
                :disabled="loading || loadingSections || loadingLayers"
            >
                <v-icon>
                    mdi-plus
                </v-icon>
            </v-btn>
        </div>

        <div class="sections-wrapper">
            <v-card class="sections-list" outlined v-if="getUserScopes().includes('section.list.view')">
                <Loading :color="color" type="linear" v-show="loadingSections" />
                <v-list rounded>
                
                    <v-subheader>{{ $t('sections') }}</v-subheader>


                    <v-skeleton-loader
                        class="mx-auto"
                        type="list-item"
                        v-for="i in 10"
                        :key="i"
                        v-show="sections.length === 0"
                        loading
                    ></v-skeleton-loader>

                    <v-list-item-group
                        :value="selectedSection.id"
                        :color="color"
                    >
                        <v-list-item
                            v-for="(section, j) in sections"
                            :key="j"
                            :value="section.id"
                            ripple
                            @click="onChangeSection(section)"
                            :disabled="loading || loadingSections"
                            :class="`section-${section.id}`"
                        >
                            <v-list-item-icon>
                                <v-icon>{{ section.icon }}</v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title v-text="getLabel(section, $i18n.locale)"></v-list-item-title>
                            </v-list-item-content>
                                <v-list-item-action>
                                    <div style="display: flex; gap: 5px;">
                            
                                        <v-btn light :color="color" fab x-small @click="(e) => edit(e, section)" v-if="getUserScopes().includes('section.edit')" :disabled="loadingSections || loadingLayers">
                                            <v-icon >mdi-pencil</v-icon>
                                        </v-btn>
                                        
                                        <v-btn fab light color="red lighten-1" x-small @click="(e) => del(e, section)" v-if="getUserScopes().includes('section.delete')" :disabled="loadingSections || loadingLayers">
                                            <v-icon >mdi-delete</v-icon>
                                        </v-btn>

                                    </div>
                                </v-list-item-action>
                            </v-list-item>
                    </v-list-item-group>

                </v-list>
            </v-card>

            <v-card class="layers-list" outlined v-if="getUserScopes().includes('layer.list.view')">
                
                <Loading :color="color" type="linear" v-show="loadingLayers" />
                
                <v-list rounded>
                
                    <v-subheader>{{ $t('layers') }}</v-subheader>


                    <v-skeleton-loader
                        class="mx-auto"
                        type="list-item"
                        v-for="i in 10"
                        :key="i"
                        v-show="sections.length === 0"
                        loading
                    ></v-skeleton-loader>

                    <v-list-item-group
                        :value="selectedSection.layer && selectedSection.layer.id"
                        :color="color"
                        class="layers-list-group"
                    >
                        <v-list-item
                            v-for="(layer, j) in selectedSection.layers"
                            :key="j"
                            :value="layer.id"
                            ripple
                            @click="onChangeLayer(layer)"
                            :disabled="loading || loadingLayers"
                        >
                            <v-list-item-icon>
                                <v-icon>mdi-layers</v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title v-text="getLabel(layer, $i18n.locale)"></v-list-item-title>
                            </v-list-item-content>
                                <v-list-item-action>
                                    <div style="display: flex; gap: 5px;">
                            
                                        <v-btn light :color="color" fab x-small @click="(e) => editLayer(e, layer)" v-if="getUserScopes().includes('layer.edit')" :disabled="loadingSections || loadingLayers">
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        
                                        <v-btn fab light color="red lighten-1" x-small @click="(e) => delLayer(e, layer)" v-if="getUserScopes().includes('layer.delete')" :disabled="loadingSections || loadingLayers">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>

                                    </div>
                                </v-list-item-action>
                            </v-list-item>
                    </v-list-item-group>

                    <div class="layer-list-actions" v-show="sections.length !== 0">
                        <v-btn 
                            color="primary"
                            :disabled="loadingLayers || selectedSection.id === ''"
                            @click="() => openLayerModal('CREATE')"
                            v-if="getUserScopes().includes('layer.create')"
                        >
                            {{ $t('add_layer') }}
                            <v-icon right>mdi-plus</v-icon>
                        </v-btn>
                    </div>
                </v-list>
            </v-card>
    
        <v-dialog
            v-model="sectionModal.open"
            max-width="560"
            @click:outside="() => close()"
        >
            <v-card v-if="sectionModal.type === 'CREATE'">
                    <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t('add_section') }}</div>
                    </v-toolbar>
                    <Loading :color="color" type="linear" v-if="loading" />
                    <v-card-text class="card-content">
                        <div class="fields">
                            <v-row>
                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="fields['name'].value"
                                        :label="$t(fields['name'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        v-model="fields['order'].value"
                                        :label="$t(fields['order'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                        type="number"
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="English"
                                        solo
                                        hide-details="auto"
                                        dense
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="fields['en'].value"
                                        :label="$t(fields['en'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="Português"
                                        hide-details="auto"
                                        dense
                                        solo
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="fields['pt'].value"
                                        :label="$t(fields['pt'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="12" sm="12">
                                    <v-card shaped outlined class="icons-card">
                                        <v-btn-toggle 
                                            dense
                                            group
                                            rounded
                                            mandatory
                                            v-model="fields['icon'].value"
                                        >
                                            <v-btn 
                                                v-for="icon in icons"
                                                :key="icon"
                                                icon
                                                ripple
                                                :value="icon"
                                            >
                                                <v-icon>{{ icon }}</v-icon>
                                            </v-btn>
                                        </v-btn-toggle>
                                    </v-card>
                                </v-col>
                            </v-row>


                            
                        </div>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            :color="color"
                            text
                            @click="() => sectionModal.open = false"
                            ripple
                            width="100"
                        >
                            {{$t('dialog_close')}}
                        </v-btn>

                        <v-btn
                            color="green darken-1"
                            filled
                            ripple
                            width="100"
                            @click="addSection()"
                            :disabled="!isFieldsFilled() || loading"
                        >
                            {{$t('dialog_save')}}
                        </v-btn>
                    </v-card-actions>
            </v-card>

            <v-card v-if="sectionModal.type === 'EDIT' && selectedSection.id !== ''">
                    <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t('edit_section') }}</div>
                    </v-toolbar>
                    
                    <Loading :color="color" type="linear" v-if="loading" />
                    
                    <v-card-text class="card-content">
                        <div class="fields">
                            <v-row>
                                <v-col cols="12" sm="12">
                                    <v-text-field
                                        v-model="fields['name'].value"
                                        :label="$t(fields['name'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="12" sm="12">
                                    <v-text-field
                                        v-model="fields['order'].value"
                                        :label="$t(fields['order'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                        type="number"
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="English"
                                        solo
                                        hide-details="auto"
                                        dense
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="fields['en'].value"
                                        :label="$t(fields['en'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="Português"
                                        hide-details="auto"
                                        dense
                                        solo
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="fields['pt'].value"
                                        :label="$t(fields['pt'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="12" sm="12">
                                    <v-card shaped outlined class="icons-card">
                                        <v-btn-toggle 
                                            dense
                                            group
                                            rounded
                                            mandatory
                                            v-model="fields['icon'].value"
                                        >
                                            <v-btn 
                                                v-for="icon in icons"
                                                :key="icon"
                                                icon
                                                ripple
                                                :value="icon"
                                            >
                                                <v-icon>{{ icon }}</v-icon>
                                            </v-btn>
                                        </v-btn-toggle>
                                    </v-card>
                                </v-col>
                            </v-row>


                            
                        </div>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            :color="color"
                            text
                            @click="() => close()"
                            ripple
                            width="100"
                        >
                            {{$t('dialog_close')}}
                        </v-btn>

                        <v-btn
                            color="green darken-1"
                            filled
                            ripple
                            width="100"
                            @click="editSection(selectedSection.id)"
                            :disabled="!isFieldsFilled() || loading"
                        >
                            {{$t('dialog_edit')}}
                        </v-btn>
                    </v-card-actions>
            </v-card>

            <v-card v-if="sectionModal.type === 'DELETE' && selectedSection.id !== ''">
                <v-toolbar
                        color="primary"
                        dark
                >
                        <div class="text-h5">{{ $t('delete_section') }}</div>
                </v-toolbar>
                <Loading :color="color" type="linear" v-if="loading" />

                <v-card-text class="mt-5">
                    {{ $t('delete_section_warn') }} <b> {{ getLabel(selectedSection, $i18n.locale) }}</b>. <br>
                    {{ $t('undoable_action') }}
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        :color="color"
                        text
                        @click="() => close()"
                        
                        ripple
                        width="100"
                    >
                        {{$t('dialog_close')}}
                    </v-btn>

                    <v-btn
                        color="red darken-1"
                        filled
                        ripple
                        width="100"
                        @click="delSection(selectedSection.id)"
                        :disabled="loading"
                    >
                        {{$t('dialog_delete')}}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>


        <!--------- LAYER ------------>

         <v-dialog
            v-model="layerModal.open"
            max-width="860"
            @click:outside="() => close()"
        >
            <v-card v-if="layerModal.type === 'CREATE'">
                    <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t('add_layer') }}</div>
                    </v-toolbar>
                    <Loading :color="color" type="linear" v-if="loadingLayers" />
                    <v-card-text class="card-content">
                        <div class="fields">
                            <v-row>
                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['name'].value"
                                        :label="$t(layerFields['name'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        v-model="layerFields['order'].value"
                                        :label="$t(layerFields['order'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                        type="number"
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['configurable'].value"
                                            :label="$t(layerFields['configurable'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['active'].value"
                                            :label="$t(layerFields['active'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['editable'].value"
                                            :label="$t(layerFields['editable'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['selected'].value"
                                            :label="$t(layerFields['selected'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="6" sm="6" v-if="layerFields['configurable'].value">
                                    <v-card shaped outlined class="configurable-card">
                                        <v-btn-toggle 
                                            dense
                                            group
                                            rounded
                                            multiple
                                            :value="layerFields['style'].value.types"
                                            
                                            
                                        >
                                            <v-btn 
                                                v-for="type in layerDefaultStyles.types"
                                                :key="type.name"
                                                icon
                                                ripple
                                                :value="type"
                                                @click="() => onChangeDefaultLayerStylesValue(type)"   
                                            >
                                                <v-icon :color="isTypeSelected(type) ? '#52FFEE' : ''">{{ type.icon }}</v-icon>
                                            </v-btn>
                                        </v-btn-toggle>
                                    </v-card>
                                </v-col>

                                <v-col cols="6" sm="6" v-if="layerFields['configurable'].value">
                                    <v-card shaped outlined class="configurable-card">
                                        <v-radio-group row v-model="layerFields['style'].value.texture.value">
                                            <v-radio color="#52FFEE" v-for="t in layerDefaultStyles.texture.options" :key="t" :value="t">
                                                <template v-slot:label>
                                                    <div :class="`box-color texture-${t}`" />
                                                </template>
                                            </v-radio>
                                        </v-radio-group>
                                    </v-card>
                                </v-col>

                                 <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="English"
                                        solo
                                        hide-details="auto"
                                        dense
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['en'].value"
                                        :label="$t(layerFields['en'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="Português"
                                        hide-details="auto"
                                        dense
                                        solo
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['pt'].value"
                                        :label="$t(layerFields['pt'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                    
                            </v-row>
                            
                        </div>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            :color="color"
                            text
                            @click="() => closeLayer()"
                            ripple
                            width="100"
                        >
                            {{$t('dialog_close')}}
                        </v-btn>

                        <v-btn
                            color="green darken-1"
                            filled
                            ripple
                            width="100"
                            @click="addLayer()"
                            :disabled="!isLayerFieldsFilled() || loading"
                        >
                            {{$t('dialog_save')}}
                        </v-btn>
                    </v-card-actions>
            </v-card>

            <v-card v-if="layerModal.type === 'EDIT' && selectedSection.layer !== null">
                    <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t('edit_layer') }}</div>
                    </v-toolbar>
                    
                    <Loading :color="color" type="linear" v-if="loading" />

                    <v-card-text class="card-content">
                        <div class="fields">
                            <v-row>
                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['name'].value"
                                        :label="$t(layerFields['name'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        v-model="layerFields['order'].value"
                                        :label="$t(layerFields['order'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                        type="number"
                                    />
                                </v-col>

                          

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['configurable'].value"
                                            :label="$t(layerFields['configurable'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['active'].value"
                                            :label="$t(layerFields['active'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['editable'].value"
                                            :label="$t(layerFields['editable'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-card shaped outlined class="switch-card">
                                        <v-switch
                                            v-model="layerFields['selected'].value"
                                            :label="$t(layerFields['selected'].label)"
                                            inset
                                        />
                                    </v-card>
                                </v-col>

                                <v-col cols="6" sm="6" v-if="layerFields['configurable'].value">
                                    <v-card shaped outlined class="configurable-card">
                                        <v-btn-toggle 
                                            dense
                                            group
                                            rounded
                                            multiple
                                            :value="layerFields['style'].value.types"
                                            
                                            
                                        >
                                            <v-btn 
                                                v-for="type in layerDefaultStyles.types"
                                                :key="type.name"
                                                icon
                                                ripple
                                                :value="type"
                                                @click="() => onChangeDefaultLayerStylesValue(type)"   
                                            >
                                                <v-icon :color="isTypeSelected(type) ? '#52FFEE' : ''">{{ type.icon }}</v-icon>
                                            </v-btn>
                                        </v-btn-toggle>
                                    </v-card>
                                </v-col>

                                <v-col cols="6" sm="6" v-if="layerFields['configurable'].value">
                                    <v-card shaped outlined class="configurable-card">
                                        <v-radio-group row v-model="layerFields['style'].value.texture.value">
                                            <v-radio color="#52FFEE" v-for="t in layerDefaultStyles.texture.options" :key="t" :value="t">
                                                <template v-slot:label>
                                                    <div :class="`box-color texture-${t}`" />
                                                </template>
                                            </v-radio>
                                        </v-radio-group>
                                    </v-card>
                                </v-col>

                                 <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="English"
                                        solo
                                        hide-details="auto"
                                        dense
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['en'].value"
                                        :label="$t(layerFields['en'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                                <v-col cols="3" sm="3">
                                    <v-text-field
                                        value="Português"
                                        hide-details="auto"
                                        dense
                                        solo
                                        disabled
                                        filled
                                    />
                                </v-col>

                                <v-col cols="9" sm="9">
                                    <v-text-field
                                        v-model="layerFields['pt'].value"
                                        :label="$t(layerFields['pt'].label)"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    />
                                </v-col>

                    
                            </v-row>
                            
                        </div>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            :color="color"
                            text
                            @click="() => closeLayer()"
                            ripple
                            width="100"
                        >
                            {{$t('dialog_close')}}
                        </v-btn>

                        <v-btn
                            color="green darken-1"
                            filled
                            ripple
                            width="100"
                            @click="confirmEditLayer(selectedSection.layer.id)"
                            :disabled="!isLayerFieldsFilled() || loading"
                        >
                            {{$t('dialog_edit')}}
                        </v-btn>
                    </v-card-actions>
            </v-card>

           <v-card v-if="layerModal.type === 'DELETE' && selectedSection.layer.id">
               <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t('delete_layer') }}</div>
                </v-toolbar>
                <Loading :color="color" type="linear" v-if="loading" />

                <v-card-text class="mt-5">
                    {{ $t('delete_layer_warn') }} <b> {{ getLabel(selectedSection, $i18n.locale) }}</b>. <br>
                    {{ $t('undoable_action') }}
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        :color="color"
                        text
                        @click="() => closeLayer()"
                        
                        ripple
                        width="100"
                    >
                        {{$t('dialog_close')}}
                    </v-btn>

                    <v-btn
                        color="red darken-1"
                        filled
                        ripple
                        width="100"
                        @click="confirmDelLayer(selectedSection.layer.id)"
                        :disabled="loading"
                    >
                        {{$t('dialog_delete')}}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { isEmpty } from 'lodash';
import { getUserScopes, getApi, getErrors, getDefaultLayerStyles, getDefaultColorScales, getLabel } from '../../utils';
import Loading from '../loading/Loading.vue'

export default {
    name: 'Sections',
    components: { Loading },
    data() {
        return {
            selectedSection: { id: '', name: '', layers: [], layer: null },
            color: '#52FFEE',
            sections: [],
            layers: [],
            loading: false,
            loadingSections: false,
            loadingLayers: false,
            sectionModal: { open: false, type: '' },
            layerModal: { open: false, type: '' },
            icons: ['mdi-home', 'mdi-lightbulb', 'mdi-layers', 'mdi-flag', 'mdi-car', 'mdi-walk', 'mdi-hospital-building', 'mdi-bank'],
            fields: {
                name: { value: '', label: 'field_name' },
                order: { value: '', label: 'field_order' },
                en: { value: '', label: 'field_en' },
                pt: { value: '', label: 'field_pt' },
                icon: { value: '', label: 'field_icon' },
            },
            layerFields: {
                name: { value: '', label: 'field_name' },
                order: { value: '', label: 'field_order' },
                selected: { value: false, label: 'field_selected' },
                configurable: { value: false, label: 'field_configurable' },
                active: { value: false, label: 'field_active' },
                editable: { value: false, label: 'field_editable' },
                en: { value: '', label: 'field_en' },
                pt: { value: '', label: 'field_pt' },
                style: { value: getDefaultLayerStyles(), label: 'field_styles' }
            },
            layerDefaultStyles: getDefaultLayerStyles()
        }
    },
    beforeMount() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
    mounted() {
        this.loadSections();
    },
    methods: {
        getLabel(item, language) { 
            return getLabel(item, language) ;
        },
        isTypeSelected(type) {
            const types = this.layerFields['style'].value.types;
            for (let i = 0; i < types.length; i++) {
                if (types[i].name === type.name) return true;
            }
            return false;
        },
        onChangeDefaultLayerStylesValue(type) {
            let newFields = Object.assign({}, this.layerFields);

            const found = newFields['style'].value.types.find(t => t.name === type.name);

            if (found) return this.layerFields['style'].value.types = newFields['style'].value.types.filter(t => t.name !== type.name);
            
            this.layerFields['style'].value.types.push(type);            
        },
        loadSections() {
            this.loadingSections = true;
            let url = getApi(`section`)
            axios.get(url).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loadingSections = false;
                    return getErrors(errors);
                }

                this.sections = data;

                this.loadingSections = false;
            }).catch(error => {
                console.log(error);
                this.loadingSections = false;
            });
        },
        async close() {
            this.sectionModal = { open: false, type: '' };
            this.selectedSection = { id: '', name: '', layers: [], layer: null };
            Object.values(this.fields).map(item => item.value = '');
        },
        add() {
            this.sectionModal = { open: true, type: 'CREATE' };
        },
        async edit(e, section) {
            e.stopPropagation();
            this.onChangeSection(section, true).then(() => {
                this.sectionModal = { open: true, type: 'EDIT' };
                
                const { name, order, label, icon } = this.selectedSection;

                const newFields = Object.assign({}, this.fields);

                newFields.name.value = name;
                newFields.order.value = order;
                newFields.en.value = label.en;
                newFields.pt.value = label.pt;
                newFields.icon.value = icon;

                this.fields = newFields;
            });
               
        },
        async del(e, section) {
            e.stopPropagation();
            this.onChangeSection(section).then(() => {
                this.sectionModal = { open: true, type: 'DELETE' };
            });
        },
        delSection(sectionId) {
            this.loading = true;

            let url = getApi(`section/${sectionId}`);
            axios.delete(url).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }

                this.loading = false;

                this.close();
            })
                .then(() => this.loadSections())
                .catch(error => {
                    console.log(error);
                    this.loading = false;
                })
            
        },
        editSection(sectionId) {
            this.loading = true;

            const { name, order, pt, en, icon } = this.fields;

            const payload = {
                name: name.value,
                order: order.value,
                label: { en: en.value, pt: pt.value },
                icon: icon.value
            }

            let url = getApi(`section/${sectionId}`)
            axios.patch(url, payload).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }

                this.close().then(() => {
                    this.loading = false;    
                });
            })
            .then(() => this.loadSections())
            .catch(error => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_update_section', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
            });
        },
        isFieldsFilled() {
            let verifiedFields = true;
            Object.values(this.fields).map(field => {
                if (field.value === '') {
                    verifiedFields = false
                }
            });
            return verifiedFields;
        },
        addSection() {
            if (!this.isFieldsFilled()) {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' };
                return this.$store.dispatch('updateSnackbar', snackbar);
            }

            this.loading = true;

            const { name, order, pt, en, icon } = this.fields;
            const payload = {
                name: name.value,
                order: order.value,
                label: { en: en.value, pt: pt.value },
                icon: icon.value
            }
                        
            let url = getApi(`section`)
            axios.post(url, payload).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }

                this.sectionModal = { open: false, type: '' };

                this.loading = false;
            })
            .then(() => this.loadSections())
            .catch(error => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_create_section', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
            });
        },
        getUserScopes() {
            return getUserScopes();
        },
        async onChangeSection(section, isEditing = false) {
            if (this.selectedSection.id == section.id && !isEditing) return this.selectedSection = { id: '', name: '', layers: [], layer: null };

            this.loadingLayers = true;

            let url = getApi(`section/${section.id}`);
            return axios.get(url).then(response => {
                const { data, errors } = response.data;
                
                if (!isEmpty(errors)) {
                    this.selectedSection = { id: '', name: '', layers: [], layer: null };
                    this.loadingLayers = false;
                    return getErrors(errors);
                }

                this.selectedSection = data;

                this.loadingLayers = false;
            }).catch(error => {
                console.log(error);
                this.loadingLayers = false;
            });
        },
        async onChangeLayer(layer, isEditing = false) {
            const newSelectedSection = Object.assign({}, this.selectedSection);
            newSelectedSection.layer = layer;
            this.selectedSection = newSelectedSection;
        },
        async closeLayer() {
            this.layerModal = { open: false, type: '' };
            Object.keys(this.layerFields).map(key => {
                if (['selected', 'configurable', 'active', 'editable'].includes(key)) this.layerFields[key].value = false;
                else if (key === 'style') this.layerFields[key].value = getDefaultLayerStyles();
                else this.layerFields[key].value = '';
            });
        },
        openLayerModal(type) {
            this.layerModal = { open: true, type: type };
        },
        isLayerFieldsFilled() {
            let verifiedFields = true;
            Object.values(this.layerFields).map(field => {
                if (field.value === '') {
                    verifiedFields = false
                }
            });
            return verifiedFields;
        },
        addLayer() {
            if (!this.isLayerFieldsFilled()) {
                const snackbar = { open: true, color: '', text: 'warning_fill_fields', timeout: 2500, type: 'warning' };
                return this.$store.dispatch('updateSnackbar', snackbar);
            }

            this.loading = true;

            const { id } = this.selectedSection;
            const { name, order, selected, configurable, active, editable, en, pt, style } = this.layerFields;
                                  
            const payload = {
                name: name.value,
                order: order.value,
                selected: selected.value,
                configurable: configurable.value,
                active: active.value,
                editable: editable.value,
                style: style.value,
                id_section: id,
                label: { en: en.value, pt: pt.value }
            }

            let url = getApi(`layer`);
            axios.post(url, payload).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }

                this.loading = false;
                this.layerModal = { open: false, type: '' }

                const section = document.querySelector(`.section-${id}`);
                if (section) {
                    section.click();
                    section.click();
                }
            })
            .catch(error => {
                console.log(error);
                this.loading = false;
            });
        },
        async editLayer(e, layer) {
            e.stopPropagation();
            this.onChangeLayer(layer).then(() => {                
                const { name, order, label, selected, configurable, active, editable, style } = this.selectedSection.layer;

                const newFields = Object.assign({}, this.layerFields);

                newFields.name.value = name;
                newFields.order.value = order;
                newFields.en.value = label.en;
                newFields.pt.value = label.pt;
                newFields.selected.value = selected;
                newFields.configurable.value = configurable;
                newFields.active.value = active;
                newFields.editable.value = editable;
                newFields.style.value = style;               

                this.layerFields = newFields;

                this.layerModal = { open: true, type: 'EDIT' };
            });
               
        },
        async delLayer(e, layer) {
            e.stopPropagation();
            this.onChangeLayer(layer).then(() => {
                this.layerModal = { open: true, type: 'DELETE' };
            });
        },
        confirmDelLayer(layerId) {
            this.loading = true;

            const { id } = this.selectedSection;

            let url = getApi(`layer/${layerId}`);
            axios.delete(url).then(response => {

                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }                

                this.closeLayer().then(() => {
                    const section = document.querySelector(`.section-${id}`);
                    if (section) {
                        section.click();
                        section.click();
                    }
                });

                this.loading = false;
            })

            .catch(error => {
                console.log(error);
                this.loading = false;
            });
            
        },
        confirmEditLayer(layerId) {
            this.loading = true;

            const { id } = this.selectedSection;
            const { name, order, selected, configurable, active, editable, en, pt, style } = this.layerFields;
            
            const payload = {
                name: name.value,
                order: order.value,
                selected: selected.value,
                configurable: configurable.value,
                active: active.value,
                editable: editable.value,
                style: style.value,
                id_section: id,
                label: { en: en.value, pt: pt.value }
            }            

            this.loading = false;

            let url = getApi(`layer/${layerId}`)
            axios.patch(url, payload).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loading = false;
                    return getErrors(errors);
                }

                this.closeLayer().then(() => {
                    const section = document.querySelector(`.section-${id}`);
                    if (section) {
                        section.click();
                        section.click();
                    }
                });

                this.loading = false;
            })
            .catch(error => {
                console.log(error);
                const snackbar = { open: true, color: '', text: 'error_update_layer', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loading = false;
            });
        },
    }
}
</script>

<style lang="scss">
.card-content {
    padding: 20px !important;
    .fields {
        padding: 10px;
        .switch-card {
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }

    .icons-card {
        display: flex;
        gap: 10px;
        padding: 10px;
        align-items: center;
        justify-content: center;
    }

    .configurable-card {
        display: flex;
        gap: 10px;
        padding: 10px;
        align-items: center;
        justify-content: center;
        height: 80px;
    }

     .editable-card {
        display: flex;
        gap: 10px;
        padding: 10px;
        align-items: center;
        justify-content: center;
     }
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

.sections-wrapper  {
    display: grid;
    grid-template-columns: 1fr 2fr;
    grid-gap: 20px;
    margin-top: 20px;
    .sections-list, .layers-list {
        height: 75vh;
        max-height: 75vh;
        overflow-y: auto;
    }

    .layers-list {
        .layers-list-group {
            min-height: 65vh;
        }

        .layer-list-actions {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            bottom: 0;
            //margin-bottom: 10px;
            position: sticky;
            padding: 10px;
        }

    }
}

@media (min-width: 320px) and (max-width: 960px) {
    .users-wrapper {
        grid-template-columns: 1fr;
    }
}


</style>