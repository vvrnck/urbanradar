<template>
    <v-card shaped outlined class="admin">
        <div class="admin-header">
            <v-tabs
                v-model="tab"
            >
                <v-tabs-slider :color="color"></v-tabs-slider>
                <v-tab
                    v-for="item in items"
                    :key="item.type"
                    ripple
                    :show-arrows="false"
                >
                    {{ $t(item.label) }}
                </v-tab>
            </v-tabs>
        </div>

        <div class="admin-content">
             <v-tabs-items v-model="tab">
                <v-tab-item
                    v-for="item in items"
                    :key="item.type"
                    dark
                >
                    <div class="admin-type">

                        <div class="sections" v-if="item.type === 'SECTIONS'" :key="tab">
                            <Sections />
                        </div>

                    </div>
                </v-tab-item>
            </v-tabs-items>
        </div>
    </v-card>
</template>

<script>
import Sections from './Sections.vue';

export default {
    name: 'Admin',
    components: { Sections },
    data() {
        return {
            color: '#52FFEE',
            tab: 0,     
            items: [
                {
                    type: 'SECTIONS',
                    label: 'sections',
                },
            ],
        }
    }    
}
</script>


<style lang="scss">
.admin {
    //display: flex;
    //align-items: center;
    //justify-content: center;
    width: 100%;
    margin: 10px;
    padding: 10px;
    
    .admin-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .admin-content {
        height: 100%;

        .admin-type {
            //height: 100vh;
         
            .sections {
                padding: 20px 50px;
                height: 100%;
                overflow: auto;
            }
        }
    }
}


@media (min-width: 320px) and (max-width: 960px) {
    .admin {
        margin-top: 56px;
    }
}
</style>