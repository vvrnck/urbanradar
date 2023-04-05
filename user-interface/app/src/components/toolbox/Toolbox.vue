<template>
    <div
      class="toolbox" 
      @click="toolbox = true"
      :style="{'width': !toolbox ? '44px' : 'fit-content', 'height': !toolbox ? '44px' : 'fit-content' }"
      data-v-step="toolbox"
    >
        <v-sheet class="toolbox-content">
            <v-icon v-if="!toolbox"> 
                mdi-tools
            </v-icon>
     
            <div v-if="toolbox">
                <div class="quick-search">
                    <div class="close">
                        <span class="close-title">{{  $t("quick_filter") }}</span>
                        <v-btn icon @click="(e) => { e.stopPropagation(); toolbox = false; }">
                            <v-icon >
                                mdi-close
                            </v-icon>
                        </v-btn>
                    </div>
                    
                    <div class="quick-search-content">
                        <v-card elevation="2" outlined shaped>
                            <div class="quick-search-items">
                                <div v-for="action in actions" :key="action.name">
                                    <v-btn :small="action.small" @click="handleToolboxDate(action.name)" block>
                                        <div v-if="action.direction === 'left'">
                                            <v-icon left>{{ action.icon }}</v-icon>
                                            {{ $t(action.name.toLowerCase()) }}
                                        </div>
                                        <div v-if="action.direction === 'right'">
                                            {{ $t(action.name.toLowerCase()) }}
                                            <v-icon right>{{ action.icon }}</v-icon>
                                        </div>
                                    </v-btn>
                                </div>
                            </div>
                        </v-card>
                    </div>
                    
              </div>
            </div>
        </v-sheet>
    </div>
</template>

<script>
import moment from 'moment';

export default {
    name: 'Toolbox',
    props: ['loadFeatures'],
    data() {
        return {
            toolbox: false,
            actions: [
                { name: 'PREVIOUS_DAY', icon: 'mdi-arrow-left', direction: 'left', small: true },
                { name: 'NEXT_DAY', icon: 'mdi-arrow-right', direction: 'right', small: true },
                { name: 'PREVIOUS_WEEK', icon: 'mdi-arrow-left', direction: 'left', small: true },
                { name: 'NEXT_WEEK', icon: 'mdi-arrow-right', direction: 'right', small: true },
                { name: 'PREVIOUS_MONTH', icon: 'mdi-arrow-left', direction: 'left', small: true },
                { name: 'NEXT_MONTH', icon: 'mdi-arrow-right', direction: 'right', small: true },
                // { name: 'PREVIOUS_YEAR', icon: 'mdi-arrow-left', direction: 'left', small: true },
                // { name: 'NEXT_YEAR', icon: 'mdi-arrow-right', direction: 'right', small: true },
            ]
        }
    },
    methods: {
        handleToolboxDate(type) {
            let newDate = this.$store.getters.dates;
            
            let newFirstDate;
            let newLastDate;

            if (type === 'PREVIOUS_DAY') {
                newFirstDate = moment(newDate[0]).subtract(1, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).subtract(1, 'days').format('yyyy-MM-DD');
            } else if (type === 'NEXT_DAY') {
                newFirstDate = moment(newDate[0]).add(1, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).add(1, 'days').format('yyyy-MM-DD');
            } else if (type === 'PREVIOUS_WEEK') {
                newFirstDate = moment(newDate[0]).subtract(7, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).subtract(7, 'days').format('yyyy-MM-DD');
            } else if (type === 'NEXT_WEEK') {
                newFirstDate = moment(newDate[0]).add(7, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).add(7, 'days').format('yyyy-MM-DD');
            } else if (type === 'PREVIOUS_MONTH') {
                let firstDate = moment(newDate[0]);
                let previousMonthDays = moment(firstDate).subtract(1, 'month').daysInMonth();
                newFirstDate = moment(newDate[0]).subtract(previousMonthDays, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).subtract(previousMonthDays, 'days').format('yyyy-MM-DD');
            } else if (type === 'NEXT_MONTH') {
                let firstDate = moment(newDate[0]);
                let currentMonthDays = moment(firstDate).daysInMonth();
                newFirstDate = moment(newDate[0]).add(currentMonthDays, 'days').format('yyyy-MM-DD');
                newLastDate = moment(newDate[1]).add(currentMonthDays, 'days').format('yyyy-MM-DD');
            }
            
            const dates = [newFirstDate, newLastDate];
            this.$store.dispatch('updateDates', dates);
            this.loadFeatures();
        },
    }
}
</script>

<style lang="scss">
.toolbox {
    position: absolute !important;
    bottom: 10px;
    right: 10px;
    z-index: 999;
    width: 44px;
    height: 44px;
    border: 2px solid rgba(0,0,0,0.2);   
    box-shadow: 0 1px 5px rgba(0,0,0,0.2);
    background-clip: padding-box;
    //padding: 5px 10px;
    border-radius: 5px !important;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 400px;
    max-height: 650px;
    overflow-y: hidden;    
    overflow-x: hidden;
    opacity: 0.9;    

    .toolbox-content {
        display: flex;
        justify-content: center;
        justify-items: center;
        align-items: center;
        width: 100%;
        height: 100%;
        transition: all 0.7s ease-in-out 0s;
        opacity: 0.9;
        border-radius: 3px !important;
        .quick-search {
            display: flex;
            flex-direction: column;
            .quick-search-content {
                margin: 10px;
                .quick-search-items {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 5px;
                    margin: 10px;
                }
            }
        }

        .close {
            display: grid;
            grid-template-columns: 9fr 1fr;
            margin: 5px;
            align-items: center;
            .close-title {
                font-size: medium;
                margin-left: 10px;
            }
        }
    }
}
</style>