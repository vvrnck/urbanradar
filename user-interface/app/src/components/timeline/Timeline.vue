<template>
    <div>
             <v-dialog
                v-model="timeline"
                width="720"
                @click:outside="closeTimeline()"
                class="dialog-timeline"
                scrollable
            >
                <v-card shaped outlined class="timeline-wrapper">
                    <v-toolbar
                        color="teal"
                    >
                        <div class="headline">{{ $t('timeline') }}</div>
                        <v-spacer></v-spacer>
                        <v-btn icon @click="closeTimeline()">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </v-toolbar>
                    <Loading color="primary" type="linear" v-if="loading" />

                    <v-divider></v-divider>
                    
                    <div class="timeline-loader" v-if="loading" >
                            <v-progress-circular
                                indeterminate
                                color="teal"
                                class="mx-auto ma-5 justify-center align-center"
                                :size="50"
                                width="5"
                            ></v-progress-circular>

                    </div>

                    <div class="timeline-loader" v-if="!loading && !items.length" >
                        
                        <h4>{{ $t('no_data') }}</h4>

                    </div>
                    
                    <div class="timeline" v-if="!loading && items.length">
                        <v-timeline
                            align-top
                            dense
                        >
                            <v-timeline-item
                                
                                v-for="(item, k) in items"
                                :key="k"
                                :icon="item.action === 'CREATE' ? 'mdi-plus' : 'mdi-pencil'"
                                :color="getColor(item.action)"
                                fill-dot
                            >
                                <v-row class="pt-1">
                                    <v-col cols="3">
                                        <strong>{{ formatDate(item.creation_date) }}</strong>
                                    </v-col>
                                    <v-col cols="7">
                                        <strong>{{ $t(getAction(item.action)) }}</strong>
                                        <div class="text-caption">
                                            {{ item.user_name }}
                                        </div>
                                    </v-col>
                                    <v-col v-if="item.data.length" cols="2">
                                         <v-btn 
                                                    
                                                    icon 
                                                    @click="openInfo(item)"
                                                >
                                                    <v-icon>mdi-eye</v-icon>
                                                </v-btn>
                                        
                                    </v-col>
                                </v-row>
                            </v-timeline-item>  
                        </v-timeline>

                </div>
        </v-card>
             
    </v-dialog> 
    <v-dialog
        v-model="info.open"
        width="1000"
        style="overflow-x: hidden;"
        content-class="dialog-timeline-info"
        @click:outside="closeInfo()"
        v-if="info.open"
    >
               <v-card outlined class="card-info">
                    <v-toolbar
                        color="teal"
                    >
                        <div class="headline">{{ $t('fields') }}</div>
                        <v-spacer></v-spacer>
                        <v-btn icon @click="info = false">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                    </v-toolbar>
                        <div class="field-header">
                            <div class="header-old-value">{{ $t('old_value') }}</div>
                            <div class="header-new-value">{{ $t('new_value') }}</div>
                        </div>
                        <div v-for="(dataItem, j) in info.data" :key="j" class="ma-5">
                            <div class="data-item">
                                <div class="attribute">
                                    {{ dataItem.attribute }}:
                                </div>
                                <v-card class="changes pa-1" outlined tile elevation="10">
                                    <div class="old-value">
                                        {{ dataItem.old_value }}
                                    </div>
                                    <v-icon color="primary">mdi-arrow-right-bold-circle-outline</v-icon>
                                    <div class="new-value">
                                        {{ dataItem.new_value }}
                                    </div>
                                </v-card>
                            </div>
                    </div>
                </v-card>
        </v-dialog>
    </div>
</template>

<script>
import moment from 'moment';
import axios from 'axios';
import { getErrors, getApi } from '../../utils';
import { isEmpty } from 'lodash';
import Loading from '../loading/Loading.vue';

export default {
    name: 'Timeline',
    components: { Loading },
    props: ['closeTimeline', 'timeline'],
    data() {
        return {
            loading: true,
            items: [],
            info: { open: false, data: [] }
        }
    },
    mounted() {
        const timelineWrapper = document.querySelector('.timeline-wrapper');
        if (timelineWrapper) {        
            timelineWrapper.parentNode.parentNode.style.setProperty('z-index', '999999', 'important');
        }

        const newDrawDialog = Object.assign({}, this.$store.getters.drawDialog);

        const { feature } = newDrawDialog;

        let url = getApi(`audit/${feature.id}`, { type: 'Feature' });
        axios.get(url).then(response => {
            const { data, errors } = response.data;

            if (!isEmpty(errors)) {
                this.loading = false;
                return getErrors(errors);
            }

            this.items = data;

            this.loading = false;
        })
        .catch(error => {
            console.log(error);
            const snackbar = { open: true, color: '', text: 'error_get_timeline', timeout: 2500, type: 'error' };
            this.$store.dispatch('updateSnackbar', snackbar);
            this.loading = false;
        })
    },
    methods: {
        closeInfo() {
            this.info = { open: false, data: [] };
        },
        openInfo(item) {
            this.info = { open: true, data: item.data };
            setTimeout(() => {
                const fieldsInfo = document.querySelector('.dialog-timeline-info');
                if (fieldsInfo) {        
                    fieldsInfo.parentNode.style.setProperty('z-index', '99999999', 'important');
                }
            }, 100);
            
        },
        getColor(action) {
            if (action === 'CREATE') return 'primary';
            return 'secondary'
        },
        formatDate(date) {
            const language = this.$i18n.locale;
            if (['pt'].includes(language)) return moment(date).format('DD/MM/YYYY hh:mm:ss');
            return moment(date).format('MM-DD-YYYY hh:mm:ss');
        },
        getAction(action) {
            if (action === 'CREATE') return 'object_create';
            return 'object_edit'
        }
    }
}
</script>

<style lang="scss">
.timeline-wrapper {
    overflow-y: auto;
    overflow-x: hidden;
    
    .timeline-loader {
        padding: 20px;
        display: flex;
    }

  
}


.card-info {
    .field-header {
        display: flex;
        justify-content: space-evenly;
        margin-left: 150px;
        padding: 10px;
        .header-old-value, .header-new-value {
            font-size: 20px;
            font-weight: bold;
        }
    }
}

.data-item {
    display: flex;
    gap: 10px;
    align-items: center;
    margin: 5px;


    .attribute {
        width: 150px;
        text-overflow: ellipsis;    
        word-break: break-all;
        align-items: center;
        display: flex;
        justify-items: center;
        padding: 5px;
    }
    .changes {
        width: 100%;
        align-items: center;
        justify-items: center;
        display: grid;
        gap: 10px;
        grid-auto-flow: column;
        grid-auto-columns: 1fr 30px 1fr;
        .old-value {
            font-style: italic;
        }
        .new-value {
            font-weight: bold;
        }
        .old-value, .new-value {
            text-overflow: ellipsis;    
            word-break: break-all;
            align-items: center;
            display: flex;
            justify-items: center;
            justify-content: center;
            padding: 10px;
        }
    }
}

</style>