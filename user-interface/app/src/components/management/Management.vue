<template>
    <v-card shaped outlined class="manage">
        <div class="manage-header">
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
                    {{ $t(item.type) }}
                </v-tab>
            </v-tabs>
        </div>

        <div class="manage-content">
            <v-tabs-items v-model="tab">
                <v-tab-item
                    v-for="(item, k) in items"
                    :key="k"
                    dark
                >
                    <div class="manage-type">
                        <div class="users" v-if="item.type.toLowerCase() === 'users'" :key="item.type">
                            <Users :color="color" />
                        </div>

                        <div class="roles" v-if="item.type.toLowerCase() === 'roles'" :key="item.type">
                            <Roles :color="color" />
                        </div>

                    </div>
                </v-tab-item>
            </v-tabs-items>
        </div>
    </v-card>
</template>

<script>
import axios from 'axios';
import Users from './Users.vue';
import Roles from './Roles.vue'

export default {
    name: 'Management',
    components: { Users, Roles },
    data() {
        return {
            color: '#52FFEE',
            tab: 0,     
            items: [
                {
                    type: 'users',
                    text: 'users text',
                    title: 'create_user'    
                },
                {
                    type: 'roles',
                    text: 'role text',
                    title: 'create_role'    
                },
                // {
                //     type: 'Group',
                //     text: 'group text'
                // },
            ],
        }
    }, 
    beforeCreate() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
}
</script>

<style lang="scss">
.manage {
    width: 100%;
    margin: 10px;
    padding: 10px;
    
    .manage-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .manage-content {
        height: 100%;

        .manage-type {
            //height: 100vh;
         
            .users, .roles {
                padding: 20px 50px;
                height: 100%;
                overflow: auto;
            }
        }
    }
}

@media (min-width: 320px) and (max-width: 960px) {
    .manage {
        margin-top: 56px;
    }
}
</style>