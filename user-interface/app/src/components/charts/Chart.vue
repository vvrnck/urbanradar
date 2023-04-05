<template>
    <div :style="`grid-area: ${gridName}`">
        <v-card outlined shaped class="chart-wrapper">
            <div :id="gridName" :style="styles"></div>
        </v-card>
    </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'Chart',
    props: ['options', 'styles', 'gridName', 'interactive'],
    mounted() {
        // NON INTERACTIVE - interactive = { type: '', custom_data: [] }
        if (!this.interactive) return this.createChart();

        // INTERACTIVE CHART
        const interactiveChart = this.createInteractiveChart();
        if (interactiveChart) return interactiveChart;
    },
    methods: {
        createChart() {
            var chart = echarts.init(document.getElementById(this.gridName), "dark");
        
            const newOptions = Object.assign({}, this.options);
            
            chart.setOption(newOptions);

            return chart;
        },
        createInteractiveChart() {
            switch (this.interactive.type) {
                case 'BAR':
                    return this.getInteractiveBarChart();
                default:
                    return null;
            }
        },
        getInteractiveBarChart() {
            const { custom_data } = this.interactive;

            var chart = this.createChart();

            chart.on('click', (event) => {
                if (event.data) {
                    var subData = custom_data.find(function (data) {
                        return data.dataGroupId === event.data.groupId;
                    });
                    
                    if (!subData) {
                        return;
                    }

                    chart.setOption({
                        yAxis: {
                            data: subData.data.map(function (item) {
                                return item[0];
                            })
                        },
                        series: {
                            type: 'bar',
                            dataGroupId: subData.dataGroupId,
                            data: subData.data.map(function (item) {
                                return item[1];
                            }),
                            universalTransition: {
                                enabled: true,
                                divideShape: 'clone'
                            }
                        },
                        graphic: [
                            {
                                type: 'image',
                                left: 50,
                                top: 20,
                                style: {
                                    image: `data:image/png;base64,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`,
                                    width: 50,
                                    height: 50
                                },
                                onclick: () => {
                                    chart.setOption(this.options);
                                }
                            }
                        ]
                    });
                }
            });
            
            return chart;
        }
    }
}
</script>

<style lang="scss">
.chart-wrapper {
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #0e0c1e !important;
}
</style>