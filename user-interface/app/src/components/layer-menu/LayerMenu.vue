<template>
    <v-slide-x-transition v-if="layer.show">
        <v-sheet class="inner-menu-options">
            <div class="inner-menu-title">
                {{ getLabel(layer, $i18n.locale) }}
                <v-btn icon fab small outlined @click="close()">
                    <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
            </div>
            <v-divider></v-divider>
            <div class="inner-menu-items">
                <v-list dense expand class="inner-menu-items-list">  
                     <v-list-group
                        prepend-icon="mdi-layers"
                        v-for="(l, index) in layer.options"
                        :key="index"
                        class="inner-menu-item"
                        v-model="l.open"
                        color="#52FFEE"
                    >
                        <template v-slot:activator >                            
                            <v-list-item-title>{{ l.name }}</v-list-item-title>
                        </template>

                        <v-divider
                            v-if="index < layer.options.length - 1"
                            :key="index"
                        ></v-divider>

                         <v-card flat>
                             <div class="inner-menu-layer-options">
                                <div class="switches">
                                    <v-switch 
                                        color="#52FFEE"
                                        v-for="type in l.style.types"
                                        v-model="type.value"
                                        :key="type.name"
                                        dense
                                        @change="onChangeType(l, type)"
                                        @click.native.stop
                                    >
                                        <template v-slot:label>
                                            
                                            <p style="font-size: 14px; display: contents;">{{ $t(`${type.name}`) }}</p>
                                            
                                        </template>
                                    </v-switch>
                                </div>
                              

                                <div class="color-picker" v-for="type in l.style.types" :key="type.name" v-show="type.name === 'hexagon' && type.value === true">
                                    <ColorPicker :type="type" :colorScale="l.style.colorScale.polygon" v-if="type.name === 'hexagon' && type.value === true" />
                                </div>

                                <div v-if="l" class="date">
                                    {{ $t('date') }}                                                         

                                    <v-dialog
                                        ref="dates"
                                        v-model="modal"
                                        :return-value.sync="dateToText(dates).dates"
                                        persistent
                                        :retain-focus="false"
                                        width="290px"
                                    >
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-text-field
                                                v-model="dateToText(dates).dates"
                                                label="Date period"
                                                prepend-icon="mdi-calendar"
                                                readonly
                                                color="#52FFEE"
                                                v-bind="attrs"
                                                v-on="on"
                                            ></v-text-field>
                                        </template>

                                        <v-date-picker
                                            range
                                            header-color="secondary"
                                            scrollable
                                            locale="pt-br"
                                            v-model="dates"
                                            color="#52FFEE"
                                            event-color="#52FFEE"
                                            
                                        >
                                            <v-spacer></v-spacer>
                                            <v-btn
                                                text
                                                
                                                @click="modal = false"
                                            >
                                                Cancel
                                            </v-btn>
                                            <v-btn
                                                text
                                                @click="() => onChangeDate(dates)"
                                            >
                                                OK
                                            </v-btn>
                                        </v-date-picker>
                                    </v-dialog>
                                </div>

                                <div v-if="l.style.texture">
                                    {{ $t('texture') }}
                                    <div class="textures">
                                         <v-radio-group row v-model="l.style.texture.value" @change="onChangeTexture(l)">
                                            <v-radio color="#52FFEE" v-for="t in l.style.texture.options" :key="t" :value="t">
                                                <template v-slot:label>
                                                    <div :class="`box-color texture-${t}`" />
                                                </template>
                                            </v-radio>
                                        </v-radio-group>
                                    </div>
                                </div>

                                <div v-if="l.filters">
                                    {{ $t('filters') }}
                                    <div class="filters">
                                        <div class="filter" v-for="filter in l.filters" :key="filter.id">
                                            <span class="filter-title">{{ getLabel(filter, $i18n.locale) }}</span>
                                            <vue-tags-input
                                                v-model="filter.value"
                                                :tags="filter.tags"
                                                :autocomplete-items="filteredItems(filter.items, filter.value)"
                                                :placeholder="getFilterName()"
                                                @tags-changed="newTags => filter.tags = newTags"
                                                :autocomplete-min-length="0"
                                                :avoid-adding-duplicates="false"
                                                :add-only-from-autocomplete="true"
                                            />
                                        </div>
                                    </div>
                             
                                </div>


                             </div>
                         </v-card>
                    </v-list-group>
                    
                </v-list>
            </div>
        </v-sheet>
    </v-slide-x-transition>
</template>

<script>
import { isEmpty } from 'lodash';
import { getApi, getOrigin, getLabel } from '../../utils';

import VueTagsInput from '@johmun/vue-tags-input';
import ColorPicker from '../color-picker/ColorPicker.vue';


export default {
    name: 'LayerMenu',
    props: ['layer', 'close'],
    components: { VueTagsInput, ColorPicker },
    data() {
        return {
            modal: false,
            textures: ['NONE', 'HORIZONTAL', 'VERTICAL'],    
        }
    },
    methods: {
        getLabel(item, language) { 
            return getLabel(item, language) ;
        },
        getFilterName() {
            // ADD LOGIC ACCORDINGLY TO TENANT/ORIGIN
            return 'Add Filter'
        }, 
        onChangeDate(dates){
            if (dates.length == 1) dates[1] = dates[0];
            this.$refs.dates[0].save();
        },
        onChangeTexture(layer) {

        },
        onChangeType(layer, type) {
            const newSections = Object.assign([], this.$store.getters.layers);
            
            newSections.map(section => {
                section.layers.map(l => {
                    if (l.id === layer.id) {
                        l.style.types.map(t => {
                            t.value = false;
                            
                            if (t.name === type.name) {
                                t.value = true;
                                l.selected = !l.selected;
                            }

                        });
                        
                    }
                });
            });
            
            this.$store.dispatch('updateLayers', newSections);    
        },             
        onChangeFilter(filter, newTags) {
            filter.tags = newTags
        },
        dateToText(dates) {
            const result = { dates: null };
            result.dates = dates.join(' ~ ');
            return result;
        },
        filteredItems (listItems, value) {
            if (value.length > 0) {
                listItems = listItems.filter(i => {
                    if (value !== '') return i.text.toLowerCase().includes(value.toLowerCase());
                })
            }

            return listItems
        },
    },   
    computed: {
        menu() {
            return this.$store.getters.menu;
        },
        availableDates() {
            return this.$store.getters.availableDates;
        },
        dates: {
            get() {
                return this.$store.getters.dates;
            },
            set(dates) {
                this.$store.dispatch('updateDates', dates);
            }
        },
    }
}
</script>

<style lang="scss">

    .global-overlap-index {
        z-index: 9999 !important;
    }

    .inner-menu-title {
        font-size: 18px;
        grid-gap: 10px;
        padding: 10px;
        display: grid;
        grid-template-columns: 9fr 1fr;
        align-items: center;
        //background-color: #2a2b26;
    }

    .inner-menu-options {
        overflow-y: auto;
        //background-color: #343331;
        //color: #FFF;
        height: 84.5%;
        position: absolute;
        top: 65px;
        width: -webkit-fill-available;
        margin-left: 56px;
        .inner-menu-items-list {
            padding: 0 !important;
            .inner-menu-item {
                border-bottom: 1px solid #444444;
                //background-color: #2b2a26;
                .inner-menu-layer-options {
                    padding: 15px 25px;
                    display: grid;
                    grid-auto-flow: row;
                    grid-gap: 20px;
                    .switches {
                        .v-input--selection-controls {
                            margin-top: 0 !important;
                        }

                        .color-picker {
                            width: 100%;
                        }
                    }
                    .textures {
                        display: grid;
                        grid-auto-flow: column;
                        justify-content: center;
                        justify-items: center;
                        align-items: center;
                        .box-color {
                            cursor: pointer;
                            width: 35px;
                            height: 35px;
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
                    .filters {
                        padding: 10px;
                        margin-top: 5px;
                        .filter {
                            margin-bottom: 10px;
                            .filter-title {
                                font-size: 14px;
                            }
                        }
                    }
                }
            }
        }
    }

    @media (min-width: 360px) and (max-width: 768px) {
        .inner-menu-options {
            height: 81%;
        }
    }

    @media (min-width: 768px) and (max-width: 960px) {
        .inner-menu-options {
            height: 87.5%;
        }

        .textures {
            display: flex;
            align-items: center;
            .box-color {
                cursor: pointer;
                width: 30px;
                height: 30px;
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
    }

    @media (max-width: 320px) and (max-width: 360px) {
        .inner-menu-options {
            height: 78%;    
        }

        .textures {
            .v-input--radio-group__input {
                display: grid;
                grid-auto-flow: row;
                grid-gap: 20px;
                justify-content: center;
                justify-items: center;
                align-items: center;
            }
            .box-color {
                cursor: pointer;
                width: 100px !important;
                height: 100px !important;
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
    }

    
    @media (min-width: 400px) and (max-width: 414px) {
        .inner-menu-options {
            height: 83%;
        }
    }

    @media (min-width: 1024px) {
        .inner-menu-options {
            height: 84.5%;
        }
    }

    @media (min-width: 1440px) {
        .inner-menu-options {
            height: 84.5%;
        }
    }

    @media (min-width: 360px) and (max-width: 960px) and (orientation: landscape) {
        .inner-menu-options {
            height: 62%;
        }
        .textures {
            .v-input--radio-group__input {
                display: grid;
                grid-auto-flow: row;
                grid-gap: 20px;
                justify-content: center;
                justify-items: center;
                align-items: center;
            }
            .box-color {
                cursor: pointer;
                width: 100px !important;
                height: 100px !important;
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
    }

    .vue-tags-input {
        font-size: 14px;    
    }

    .vue-tags-input .ti-new-tag-input {
        background: transparent;
        color: white;
      }

      .vue-tags-input .ti-input {
        padding: 4px 10px;
        transition: border-bottom 200ms ease;
        background-color: #222;
      }
      
      /* we cange the border color if the user focuses the input */
      .vue-tags-input.ti-focus .ti-input {
        border: 2px solid #fff;
      }
      
      /* some stylings for the autocomplete layer */
      .vue-tags-input .ti-autocomplete {
        border: 1px solid #fff;
        border-top: none;
        position: relative;
        background-color: #222;
        color: #fff;
        font-size: 14px;
      }

      /* the selected item in the autocomplete layer, should be highlighted */
      .vue-tags-input .ti-item.ti-selected-item {
        background: #000;
        color: #6dc1b2;
      }

      /* style the placeholders color across all browser */
      .vue-tags-input ::-webkit-input-placeholder {
        color: #fff;
      }

      .vue-tags-input ::-moz-placeholder {
        color: #fff;
      }

      .vue-tags-input :-ms-input-placeholder {
        color: #fff;
      }

      .vue-tags-input :-moz-placeholder {
        color: #fff;
      }

      /* default styles for all the tags */
      .vue-tags-input .ti-tag {
        position: relative;
        background: #6dc1b2;
        /* color: #283944; */
        
        color: #fff;
      }

      /* we defined a custom css class in the data model, now we are using it to style the tag */
      .vue-tags-input .ti-tag.custom-class {
        background: transparent;
        border: 1px solid #6dc1b2;
        color: #6dc1b2;
        margin-right: 4px;
        border-radius: 0px;
        font-size: 13px;
      }

      /* the styles if a tag is invalid */
      .vue-tags-input .ti-tag.ti-invalid {
        background-color: #e88a74;
      }

      /* if the user input is invalid, the input color should be red */
      .vue-tags-input .ti-new-tag-input.ti-invalid {
        color: #e88a74;
      }

      /* if a tag or the user input is a duplicate, it should be crossed out */
      .vue-tags-input .ti-duplicate span,
      .vue-tags-input .ti-new-tag-input.ti-duplicate {
        text-decoration: line-through;
      }

      /* if the user presses backspace, the complete tag should be crossed out, to mark it for deletion */
      .vue-tags-input .ti-tag:after {
        transition: transform .2s;
        position: absolute;
        content: '';
        height: 2px;
        width: 108%;
        left: -4%;
        top: calc(50% - 1px);
        background-color: #000;
        transform: scaleX(0);
      }

      .vue-tags-input .ti-deletion-mark:after {
        transform: scaleX(1);
      } 

        // vuetify conflicting with vue input tags padding
      .v-application ol, .v-application ul {
          padding-left: 10px !important;
      }
    
</style>