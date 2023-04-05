<template>
    <div class="filters-control" id="filters-control">
        <div v-for="layer in selectedLayers" :key="layer.id">
            <div
                v-for="(filter, i) in layer.filters"
                :key="i"
                style="max-width: 300px; width: 300px;"
            >
                <v-select
                    v-model="filter.values"
                    :items="filter.mobileItems"
                    item-value="text"
                    chips
                    :label="filter.type"
                    multiple
                    solo
                    @change="loadFeatures()"
                ></v-select>
            </div>
        </div>
    </div>                    
</template>

<script>
export default {
    name: 'SelectedFilters',
    props: ['loadFeatures'],
    data() {
        return {
            
        }
    },
    computed: {
        selectedLayers() {
            const sections = this.$store.getters.layers;

            const newSections = Object.assign([], sections);

            const selectedLayers = [];

            newSections.map(section => {
                section.layers.map(layer => {
                    const { extra_props } = layer.style;
                    
                    if (extra_props && extra_props.mobile && extra_props.type != 'marker' && layer.selected) selectedLayers.push(layer);
                })
            })

            return selectedLayers;
        },
    }
}
</script>