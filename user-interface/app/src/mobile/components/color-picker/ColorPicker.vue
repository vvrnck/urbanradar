<template>
    <v-row no-gutters>
        <v-col cols="3" align="start">
            <p class="text-color">{{$t("color")}}:  </p>
        </v-col>
        <v-col cols="12">
            <v-carousel 
                height="150px"
                dark
                continuous
                mandatory
                hide-delimiter-background
                @change="(e) => onChangeColor(e)"
            >
                <v-carousel-item
                    v-for="(color, n) in colorScale"
                    :key="n"
                    ripple
                >
                    <v-sheet
                        height="100%"
                        tile
                        dark
                        style="background-color: #181818"
                    >
                        <v-row
                            class="fill-height"
                            align="center"
                            justify="center"
                        >
                            <div class="display-1">
                                <svg width="28" height="32" style="cursor: pointer;" xmlns="http://www.w3.org/2000/svg">
                                    <g>
                                        <polygon stroke="#CCCCCCB3" transform="rotate(89.91702270507812 14.000076293945314,16.00004768371582) " id="svg_1" :fill='color' :key="n" points="29.47113710641861,16.000048220157623 21.735606253147125,29.30253654718399 6.264545977115631,29.30253654718399 -1.4709843397140503,16.000048220157623 6.264545977115631,2.6975608468055725 21.735606253147125,2.6975608468055725 29.47113710641861,16.000048220157623 "/>
                                    </g>
                                </svg>
                            </div>
                        </v-row>
                    </v-sheet>
                </v-carousel-item>
            </v-carousel>
        </v-col>
    </v-row>
</template>

<script>
export default {
    name: 'ColorPicker',
    props: ['type', 'colorScale'],
    data() {
        return {

        }
    },
    mounted() {
        this.updateHexagonColors();
    },
    methods: {
        onChangeColor(index) {
            this.type.color = this.colorScale[index];
        },
        updateHexagonColors() {
            function chunck(arr, chunkSize) {
                var results = [];
                let newArray = []
                Object.values(arr).map(item => newArray.push(item))
                for (var i=0,len=newArray.length; i<len; i+=chunkSize) {
                    results.push(newArray.slice(i,i+chunkSize));
                }
                return results;
            }

            this.$nextTick(() => {          
                var elements = document.getElementsByClassName("v-carousel__controls__item");
                if (elements) {
                    let newElements = chunck(elements, this.colorScale.length)
                    newElements.map(arrayItem => {
                        arrayItem.map((item, j) => {
                            item.style.margin = '0px';
                            item.style.color = this.colorScale[j]
                        })
                    })
                } 
            })
        },
    }
}
</script>