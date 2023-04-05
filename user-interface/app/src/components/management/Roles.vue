<template>
<div>
    <div class="justify-end" style="display: flex;">
            <v-btn
                class="mx-2"
                fab
                x-small
                color="primary"
                v-if="getUserScopes().includes('role.create')"
                @click="add()"
                :disabled="loading || loadingScopes"
            >
                <v-icon>
                    mdi-plus
                </v-icon>
            </v-btn>
    </div>
    <div class="roles-wrapper">
        <v-card class="role-list" outlined v-if="getUserScopes().includes('role.list.view')">
             <v-list rounded>
                <v-subheader>{{ $t('roles') }}</v-subheader>

                <v-skeleton-loader
                    class="mx-auto"
                    type="list-item"
                    v-for="i in 10"
                    :key="i"
                    v-show="roles.length === 0"
                    loading
                ></v-skeleton-loader>

                <v-list-item-group
                    :value="selectedRole.id"
                    :color="color"
                >
                    <v-list-item
                        v-for="(role, j) in roles"
                        :key="j"
                        :value="role.id"
                        ripple
                        @click="() => onChangeRole(role)"
                        :disabled="loading || loadingScopes"
                    >
                        <v-list-item-icon>
                            <v-icon>mdi-account</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ role.name }}</v-list-item-title>
                        </v-list-item-content>
                         <v-list-item-action>
                             <div style="display: flex; gap: 5px;">
                                <v-btn light :color="color" fab x-small @click="(e) => edit(e, role)" v-if="getUserScopes().includes('role.edit')">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                                
                                <v-btn fab light color="red lighten-1" x-small @click="(e) => del(e, role)" v-if="getUserScopes().includes('role.delete')">
                                    <v-icon>mdi-delete</v-icon>
                                </v-btn>

                             </div>
                        </v-list-item-action>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>

        <v-card class="scope-list" outlined v-if="getUserScopes().includes('scope.list.view')">
            
            <Loading :color="color" type="linear" v-show="loadingScopes" />

             <v-list rounded disabled>
                <v-subheader>{{ $t('scopes') }}</v-subheader>

                <v-skeleton-loader
                    class="mx-auto"
                    type="list-item"
                    v-for="k in 10"
                    :key="k"
                    v-show="scopes.length === 0 && selectedRole.id === ''"
                    loading
                ></v-skeleton-loader>

                <v-list-item-group
                    :value="selectedRole.scopes"
                    multiple
                    :color="color"
                >
                    <v-list-item
                        v-for="(scope, l) in scopes"
                        :key="l"
                        
                        :value="scope"
                        ripple
                        @click="onChangeScope(scope)"
                    >
                        <v-list-item-icon>
                            <v-icon>mdi-account</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title v-text="scope"></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>

        <v-card class="scoped-users-list" outlined v-if="getUserScopes().includes('user.list.view')">
             <v-list rounded disabled>
                <v-subheader>{{ $t('users') }}</v-subheader>

                <v-skeleton-loader
                    class="mx-auto"
                    type="list-item"
                    v-for="m in 10"
                    :key="m"
                    v-show="selectedRole.users.length === 0"
                    loading
                ></v-skeleton-loader>

                <v-list-item-group
                    :color="color"
                >
                    <v-list-item
                        v-for="(user, n) in selectedRole.users"
                        :key="n"
                        ripple
                    >
                        <v-list-item-icon>
                            <v-icon>mdi-account</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title v-text="user.name"></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>

        <Modal 
            :modal="modal" 
            :close="close" 
            :save="save" 
            :color="color" 
            :editingData="selectedRole" 
            :listItems="scopes"
            :loading="loading"
        />


         <v-dialog
            v-model="dialog.open"
            max-width="500"
        >
            <v-card>
                <v-card-title class="headline">
                    {{ $t('delete_role') }}
                </v-card-title>

                <v-card-text>
                    {{ $t('delete_role_warn') }} <b> {{ $t(dialog.role.name) }}</b>. <br>
                    {{ $t('undoable_action') }}
                </v-card-text>

                <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                    :color="color"
                    text
                    @click="dialog.open = false"
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
                    @click="delRole(dialog.role)"
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
import Modal from './Modal';
import Loading from '../loading/Loading.vue';
import { getUserScopes, getApi, getErrors } from '../../utils';
import { isEmpty } from 'lodash';

export default {
    name: 'Roles',
    props: ['color', 'api', 'origin', 'openSnackbar'],
    components: { Modal, Loading },
    data() {
        return {
            modal: { open: false, type: { type: '', title:'' }, mode: '' },
            snackbar: { open: false, color: '', text: '', timeout: 2500 },
            selectedRole: { id: '', name: '', scopes: [], users: [] },
            roles: [],
            scopes: [],
            defaultScopes: [],
            dialog: { open: false, role: { id: '', name: '' } },
            loading: false,
            loadingScopes: false
        }
    },
    beforeCreate() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
    mounted() {
        this.getRoles();
        this.getScopes();
    },
    methods: {
        getUserScopes() {
            return getUserScopes();
        },
        getRoles() {
            let roles_url = getApi('role');
            axios.get(roles_url)
                .then(response => {
                    const { data, errors } = response.data;
                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }
                    this.roles = data;
                    this.selectedRole.users = [{id: '', name: '- -'}]
                })
                .catch((err) => {
                    const snackbar = { open: true, color: '', text: 'error_load_roles', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                });
        },
        getScopes() {
            let scopes_url = getApi('scope');
            axios.get(scopes_url)
                .then(response => {
                    const { data, errors } = response.data;
                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }
                    this.defaultScopes = data;
                    this.scopes = data.map(s => s.name);
                })
                .catch((err) => {
                    const snackbar = { open: true, color: '', text: 'error_load_scopes', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                });
        },
        edit(e, role) {
            e.stopPropagation();
            this.onChangeRole(role, true).then(() => {
                this.modal = { open: true, type:  { type: 'role', title:'edit_role' }, mode: 'edit' }
            });
        },
        del(e, role) {
            e.stopPropagation();
            this.dialog.open = true;
            this.dialog.role = role;
        },
        delRole(role) {
            let url = getApi(`role/${role.id}`);
            axios.delete(url).then(response => {
                const { errors } = response.data;

                if (!isEmpty(errors)) {
                    return getErrors(errors);
                }

                const snackbar = { open: true, color: '', text: 'success_delete_role', timeout: 2500, type: 'success' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.dialog.open = false;
                this.dialog.role = { id: '', name: '' };
                this.selectedRole = { id: '', name: '', scopes: [], users:  [{ id: '', name: '- -'}] };
            }).then(() => this.getRoles()).catch(err => {
                console.log(err);
                const snackbar = { open: true, color: '', text: 'error_delete_role', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
            });
        },
        async save(data) {
            this.loading = true;
            if (this.modal.mode === 'create') {
                let create_role_url = getApi('role');
                let scopes = this.defaultScopes.filter(item => data.role.scopes.includes(item.name))
                
                let sendData = {
                    name: data.role.name,
                    scopes: scopes
                }

                axios.post(create_role_url, sendData).then(response => {
                    const { errors } = response.data;
                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }

                    const snackbar = { open: true, color: '', text: 'created_role', timeout: 2500, type: 'success' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                    this.loading = false;
                })
                .then(() => {
                    this.close();
                    this.getRoles()
                })
                .catch(err => {
                    const snackbar = { open: true, color: '', text: 'error_create_role', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                    this.loading = false;
                });
            } else {
                let scopes = this.defaultScopes.filter(item => data.scopes.includes(item.name));
                
                let edit_role_url = getApi(`role/${data.id}`);
                
                let sendData = {
                    name: data.name,
                    scopes: scopes
                }
                
                axios.patch(edit_role_url, sendData)
                    .then(response => {
                        const { errors } = response.data;
                        if (!isEmpty(errors)) {
                            return getErrors(errors);
                        }
                        const snackbar = { open: true, color: '', text: 'success_edit_role', timeout: 2500, type: 'success' }; 
                        this.$store.dispatch('updateSnackbar', snackbar);
                        this.loading = false;
                    })
                    .then(() => {
                        this.close();
                        this.getRoles();
                    })
                    .catch(err => {
                        const snackbar = { open: true, color: '', text: 'error_edit_role', timeout: 2500, type: 'error' }; 
                        this.$store.dispatch('updateSnackbar', snackbar);
                        this.loading = false;
                    });
            }
            
        },
        add() {
            this.modal = { open: true, type: { type: 'role', title:'create_role' }, mode: 'create' };
        },
        close() {
            this.modal = { open: false, type: { type: '', title:'' }, mode: ''  };
            this.selectedRole = { id: '', name: '', scopes: [], users:  [{ id: '', name: '- -'}] };
        },
        async onChangeRole(role, isEditing = false) {
            if (this.selectedRole.id == role.id && !isEditing) return this.selectedRole = { id: '', name: '', scopes: [], users: [{id: '', name: '- -'}] };
            
            this.loadingScopes = true;
            this.loading = true;

            let url = getApi(`role/${role.id}`);
            axios.get(url)
                .then(response => {
                    const { data, errors } = response.data;

                    if (!isEmpty(errors)) {
                        this.loading = false;
                        this.loadingScopes = false;
                        return getErrors(errors);
                    }

                    let newRole = { 
                        id: Number.parseInt(data.id), 
                        name: data.name, 
                        scopes: data.scopes.map(s => s.name), 
                        users: data.users.length === 0 ? [{id: '', name: '- -'}] : data.users
                    };
                    this.selectedRole = newRole;
                    this.loadingScopes = false;
                    this.loading = false;
                }).catch(err => {
                    console.log(err)
                    const snackbar = { open: true, color: '', text: 'error_retrieve_user', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                    this.loadingScopes = false;
                    this.loading = false;
                })
        },
        onChangeScope(scope) {
            if (this.selectedRole.id === '') {
                const snackbar = { open: true, color: '', text: 'warning_select_scope', timeout: 2500, type: 'warning' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.selectedRole = { id: '', name: '', scopes: [], users: [] };
            } else {
                let hasItem = this.selectedRole.scopes.find(r => r === scope);      
                if (hasItem) { // já existe, então remove
                    let newArray = this.selectedRole.scopes.filter(item => item !== scope);
                    this.selectedRole.roles = newArray;
                    // send to back updating
                } else {
                    this.selectedRole.groups.push(scope);
                    // send to back updating
                }                
            }
        }
    },

}
</script>

<style lang="scss">
    .roles-wrapper  {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-gap: 20px;
        margin-top: 10px;

        
            .role-list, .scope-list, .scoped-users-list {
                height: 75vh;
                max-height: 75vh;
                overflow-y: auto;
            }
            
        
    }

       @media (min-width: 320px) and (max-width: 960px) {
        .roles-wrapper {
            grid-template-columns: 1fr;
            .role-list, .scope-list, .scoped-users-list {
                max-height: 35.5vh !important;
                height: 35.5vh !important;
            }
        }
    }
</style>

