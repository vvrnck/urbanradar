<template>
    <div class="filters-control" id="filters-control">
        <div v-for="layer in selectedLayers" :key="layer.id" style="display: contents;">
            
            <div style="display: contents;">
                
                <div
                    v-for="(filter, i) in layer.filters"
                    :key="i"
                    class="control"
                    
                >
                    
                </div>
           
            </div>           

        </div>
         
    </div>
</template>

<script>

export default {
    name: 'Filters',
    props: ['loadFeatures'],
    data() {
        
        return {
            
            swiper: null,
            atendimentos: ['Furto', 'Contra a Vida', 'Contra a Pessoa'],
            turnos: ['Madrugada', 'Manhã', 'Tarde', 'Noite'],
            swiperOption: {
                slidesPerView: 1,
                slidesPerGroup: 1,
                spaceBetween: 20,
                //direction: 'vertical',
                loop: true,
                loopFillGroupWithBlank: false,
                grabCursor: true,
                centeredSlides: true,
                pagination: {
                    //el: '.swiper-pagination',
                    clickable: true
                },
                keyboard: {
                    enabled: true,
                },
                mousewheel: true,
                zoom: true,
                effect: 'fade',
                navigation: {
                    //nextEl: '.swiper-button-next',
                    // prevEl: '.swiper-button-prev'
                    prevEl: '.swiper-button-prev-unique',
                    nextEl: '.swiper-button-next-unique'
                }
            }
        }
    },
    mounted() {
        let el = document.getElementById('filters-control');
        //const draggable = new L.Draggable(el);
        //draggable.enable();
    },
    methods: {
        search() {            
            setTimeout(() => {
                this.loadFeatures();
            }, 200);
        },
        clickIcon(index) {
            let icon = document.getElementById('icon-'+index);
            icon.click();
            this.loadFeatures();
        },
        getFilterItem(index, indexItem, idLayer) {
            
            const currentMapData = this.$store.getters.map;

            const menu = Object.assign({}, currentMapData.menu);

            let item = null;

            // TODO - trocar para usar o find ou filter
            Object.values(menu).map(section => {
                
                section.data.map(layer => {
                    if (layer.selected && layer.id === idLayer) {
                        if (layer.id !== 49) {
                            layer.filters.map((filter, j) => {
                                if (j === index) {
                                    item = filter.items[indexItem];
                                }
                            })
                        } else {
                            layer.filters.map((filter, j) => {
                                if (j === index) {
                                    item = filter.mobileItems[indexItem];
                                }
                            })
                        }
                    }
                })
            })

            return item;
        },
        selectFilterItem(item) {
            if (!item.selected) return item.selected = true;
            item.selected = false;
        },
        getClickedSlide(e, index, idLayer) {
            
            let indexItem = parseInt(e.target.getAttribute('index'));
            let item = this.getFilterItem(index, indexItem, idLayer);
            if (item) this.selectFilterItem(item);
            
            
        },     
        getLayerFilters(layer) {
            return layer.filters;
        }
    },
    computed: {
        selectedLayers() {
            const currentMapData = this.$store.getters.map;

            const menu = Object.assign({}, currentMapData.menu);

            const selectedLayers = [];

            Object.values(menu).map(section => {
                section.data.map(layer => {
                    if (layer.selected) selectedLayers.push(layer);
                })
            })

            return selectedLayers;
        },
    }
}
</script>

<style lang="scss">

.filters-control {
    position: absolute;
    bottom: 40%;
    left: 0;
    width: 100%;
    height: 48px;
    z-index: 999;
    align-items: center;
    display: grid;
    grid-gap: 10px;
    justify-content: center;
    .filter-tipo-atendimento, .filter-turno {
        height: 100%;
    }
    .filter-items {
        display: grid;
        grid-gap: 30px;
        grid-auto-flow: column;
        align-items: center;
        justify-items: center;
        justify-content: center;
        //height: 24px;
        overflow-x: auto;
        .icon {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            div {
                display: flex;
            }
        }
    }
}

.swiper {
  height: 36px;
  width: 100%;

  .swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: bold;
    font-size: 14px;
    background-color: #FFF;
  }

}

.swiper-button-prev-unique {
    position: absolute !important;
    top: 20% !important;
    left: 0 !important;
    z-index: 99999 !important;
}

.swiper-button-next-unique {
    position: absolute !important;
    top: 20% !important;
    right: 0 !important;
    z-index: 99999 !important;
}

</style>