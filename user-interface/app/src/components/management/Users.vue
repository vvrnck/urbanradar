<template>
<div>
    <div class="justify-end" style="display: flex;">
            <v-btn
                class="mx-2"
                fab
                x-small
                color="primary"
                @click="add()"
                v-if="getUserScopes().includes('user.create')"
                :disabled="loading || loadingRoles"
            >
                <v-icon>
                    mdi-plus
                </v-icon>
            </v-btn>
    </div>
    <div class="users-wrapper">
        
        <v-card class="users-list" outlined v-if="getUserScopes().includes('user.list.view')">
            <v-list rounded>
                
                <v-subheader>{{ $t('users') }}</v-subheader>


                <v-skeleton-loader
                    class="mx-auto"
                    type="list-item"
                    loading
                    v-for="i in 10"
                    :key="i"
                    v-show="users.length === 0"
                ></v-skeleton-loader>

                <v-list-item-group
                    :value="selectedUser.uid"
                    :color="color"
                >
                    <v-list-item
                        v-for="(user, j) in users"
                        :key="j"
                        :value="user.uid"
                        ripple
                        @click="onChangeUser(user)"
                        :disabled="loading || loadingRoles"
                    >
                        <v-list-item-icon>
                            <v-icon>mdi-account</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title v-text="user.name"></v-list-item-title>
                        </v-list-item-content>
                         <v-list-item-action>
                            <div style="display: flex; gap: 5px;">
                                <v-btn light :color="color" fab x-small @click="(e) => edit(e, user)" v-if="getUserScopes().includes('user.edit')">
                                    <v-icon >mdi-pencil</v-icon>
                                </v-btn>
                                
                                <v-btn fab light color="red lighten-1" x-small @click="(e) => del(e, user)" v-if="getUserScopes().includes('user.delete')">
                                    <v-icon >mdi-delete</v-icon>
                                </v-btn>

                            </div>
                        </v-list-item-action>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>

        <div class="manage-user-role-group">
            <div class="user-role">
                <v-card outlined class="manage-user-item" v-if="getUserScopes().includes('role.list.view')">
                    
                    <Loading :color="color" type="linear" v-show="loadingRoles" />

                    <v-list rounded disabled>
                        <v-subheader>{{ $t('roles') }}</v-subheader>
    
                        <v-skeleton-loader
                            class="mx-auto"
                            type="list-item"
                            loading
                            v-for="i in 3"
                            :key="i"
                            v-show="roles.length === 0"
                        ></v-skeleton-loader>
    

                        <v-list-item-group
                            :value="selectedUser.roles"
                            multiple
                            :color="color"
                        >
                            <v-list-item
                                v-for="(role, k) in roles"
                                :key="k"
                                :value="role"
                                ripple
                                @click="onChangeRole(role)"
                            >
                                <v-list-item-content>
                                    <v-list-item-title v-text="role"></v-list-item-title>
                                </v-list-item-content>
                               
                            </v-list-item>
                        </v-list-item-group>
                    </v-list>
                </v-card>
            </div>
        </div>

        <Modal 
            v-if="modal.open" 
            :modal="modal" 
            :close="close" 
            :save="save" 
            :color="color" 
            :editingData="selectedUser" 
            :listItems="roles"
            :loading="loading"
        />


         <v-dialog
            v-model="dialog.open"
            max-width="500"
            
        >
            <v-card>
                <v-card-title class="headline">
                    {{ $t('delete_user') }}
                </v-card-title>

                <v-card-text>
                    {{ $t('delete_user_warn') }} <b> {{ $t(dialog.user.name) }}</b>. <br>
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
                        @click="delUser(dialog.user)"
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
import firebase from 'firebase/app'
import 'firebase/auth';
import Modal from './Modal';
import Loading from '../loading/Loading.vue';
import { getUserScopes, getApi, getErrors } from '../../utils'
import { isEmpty } from 'lodash';

export default {
    name: 'Users',
    props: ['openSnackbar', 'color', 'origin'],
    components: { Modal, Loading },
    data() {
        return {
            modal: { open: false, type: { type: '', title: '' }, mode: '' },
            snackbar: { open: false, color: '', text: '', timeout: 2500 },
            selectedUser: { uid: '', name: '', roles: [], groups: [], email: '', id: '' },
            defaultRoles: [],
            roles: [],
            groups: [],
            users: [],
            dialog: { open: false, user: { id: '', name: '' } },
            defaultData: {},
            loading: false,
            loadingRoles: false
        }
    },
    beforeCreate() {
        axios.defaults.headers.common['Authorization'] = localStorage.getItem('crimeradarToken');
    },
    mounted() {
        
        this.getUsers();
        this.getRoles();


 
    },
    methods: {
        getUserScopes() {
            return getUserScopes()
        },
        getUsers() {
            let users_url = getApi('user');
            axios.get(users_url).then(response => {
                    const { data, errors } = response.data;

                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }

                    this.users = data;
                })
                .catch((err) => {
                    const snackbar = { open: true, color: '', text: 'error_load_users', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                });
        },
        getRoles() {
            let roles_url = getApi('role');
            axios.get(roles_url)
                .then(response => {
                    const { data, errors } = response.data;

                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }

                    this.defaultRoles = data;
                    let roles = [];
                    data.map(role => {
                        roles.push(role.name)
                    })
                    this.roles = roles;
                })
                .catch((err) => {
                    const snackbar = { open: true, color: '', text: 'error_load_roles', timeout: 2500, type: 'error' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                });
        },
        edit(e, user) {
            e.stopPropagation();
            this.onChangeUser(user, true)
                .then(() => {
                    this.modal = { open: true, type:  { type: 'users', title:'edit_user' }, mode: 'edit' }
                });
        },
        del(e, user) {
            e.stopPropagation();
            this.dialog.open = true;
            this.dialog.user = user;
        },
        delUser(user) {
            const url = getApi(`user/${user.id}`);
            axios.delete(url)
                .then(response => {
                    const { errors } = response.data;

                    if (!isEmpty(errors)) {
                        return getErrors(errors);
                    }

                    const snackbar = { open: true, color: '', text: 'succes_delete_user', timeout: 2500, type: 'success' }; 
                    this.$store.dispatch('updateSnackbar', snackbar);
                    this.dialog = { open: false, user: { id: '', name: '' } };
                }).then(() => this.getUsers())
        },
        async save(data) {
            // TODO - checar se os campos estão vazios
            this.loading = true;
            if (this.modal.mode === 'create') {
                let url = getApi('user');
                
                firebase.auth().createUserWithEmailAndPassword(data.user.email.toLowerCase(), data.user.password)
                    .then(firebaseResponse => {

                        let roles = this.defaultRoles.filter(item => data.user.roles.includes(item.name));

                        let sendData = {
                            uid: firebaseResponse.user.uid,
                            email: firebaseResponse.user.email,
                            name: data.user.name,
                            role: data.user.role,
                            // password: data.user.password,
                            // confirm_password: data.user.confirmPassword,
                            active: true, 
                            roles: roles
                        }

                        axios.post(url, sendData).then(response => {
                            const { errors } = response.data;

                            if (!isEmpty(errors)) {
                                this.loading = false;
                                return getErrors(errors);
                            }                              

                            firebase.auth().sendPasswordResetEmail(data.user.email.toLowerCase()).then(() => {
                                const snackbar = { open: true, color: '', text: 'success_create_user', timeout: 2500, type: 'success' }; 
                                this.$store.dispatch('updateSnackbar', snackbar);
                                this.loading = false;
                            }).catch(err => {
                                const snackbar = { open: true, color: '', text: 'error_create_user', timeout: 2500, type: 'error' }; 
                                this.$store.dispatch('updateSnackbar', snackbar);
                                this.loading = false;
                                //this.modal = { open: false, type: { type: '', title: '' }, mode: '' };
                            })  
                        }).then(() => {
                            this.close();
                            this.getUsers();
                        })
                        .catch((err) => {
                            // deletar usuário do firebase caso erro na API
                            this.deleteUserFirebase(sendData.email, data.user.password);
                            const snackbar = { open: true, color: '', text: 'error_create_user', timeout: 2500, type: 'error' }; 
                            this.$store.dispatch('updateSnackbar', snackbar);
                            this.loading = false;
                        });
                    }).catch(err => {
                        console.log(err);
                        const snackbar = { open: true, color: '', text: 'error_create_user', timeout: 2500, type: 'error' }; 
                        this.$store.dispatch('updateSnackbar', snackbar);
                        this.loading = false;
                        //this.modal = { open: false, type: { type: '', title: '' }, mode: '' };
                    })

       

            } else {   
                let roles = this.defaultRoles.filter(item => data.roles.includes(item.name));
                let url = getApi(`user/${data.id}`);
                
                let sendData = {
                    id: data.id,
                    name: data.name,
                    roles: roles,
                    email: data.email
                }
                
                axios.patch(url, sendData)
                    .then(response => {
                        const { errors } = response.data;

                        if (!isEmpty(errors)) {
                            this.loading = false;
                            return getErrors(errors);
                        }

                        const snackbar = { open: true, color: '', text: 'success_edit_user', timeout: 2500, type: 'success' }; 
                        this.$store.dispatch('updateSnackbar', snackbar);
                        this.loading = false;
                    })
                    .then(() => {
                        this.close();
                        this.getUsers();
                    })
                    .catch(() => {
                        this.loading = false;
                        const snackbar = { open: true, color: '', text: 'error_edit_user', timeout: 2500, type: 'error' }; 
                        this.$store.dispatch('updateSnackbar', snackbar);
                    });

            }
            
        },
        add() {
            this.modal = { open: true, type: { type: 'users', title:'create_user' }, mode: 'create' };
        },
        close() {
            this.modal = { open: false, type: { type: '', title:'' }, mode: '' };
            this.selectedUser = { uid: '', name: '', roles: [], groups: [], id: '' };
        },
        async onChangeUser(user, isEditing = false) {
            if (this.selectedUser.uid == user.uid && !isEditing) return this.selectedUser = { uid: '', name: '', roles: [], groups: [], id: '' };

            this.loadingRoles = true;
            this.loading = true;
                        
            let url = getApi(`user/${user.id}`);
            axios.get(url).then(response => {
                const { data, errors } = response.data;

                if (!isEmpty(errors)) {
                    this.loadingRoles = false;
                    this.loading = false;    
                    return getErrors(errors);
                }

                let newUser = { uid: data.uid, name: data.name, roles: data.roles.map(r => r.name), groups: [], email: data.email, id: data.id };
                this.selectedUser = newUser;
                this.loadingRoles = false;
                this.loading = false;
            }).catch(err => {
                const snackbar = { open: true, color: '', text: 'error_retrieve_user', timeout: 2500, type: 'error' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.loadingRoles = false;
                this.loading = false;
            });
        },
        onChangeRole(value) {
            if (this.selectedUser.name === '') {
                const snackbar = { open: true, color: '', text: 'warning_select_user', timeout: 2500, type: 'warning' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.selectedUser = { uid: '', name: '', roles: [], groups: [], id: '' };
            } else {
                let hasItem = this.selectedUser.roles.find(r => r === value);            
                if (hasItem) { // já existe, então remove
                    let newArray = this.selectedUser.roles.filter(item => item !== value);
                    this.selectedUser.roles = newArray;
                    // enviar para o back update user sem o scope
                } else {
                    this.selectedUser.roles.push(value);
                    // enviar para o back update user com o novo scope
                }                
            }
        },
        onChangeGroup(value) {
            if (this.selectedUser.name === '') {
                const snackbar = { open: true, color: '', text: 'warning_select_user', timeout: 2500, type: 'warning' }; 
                this.$store.dispatch('updateSnackbar', snackbar);
                this.selectedUser = { uid: '', name: '', roles: [], groups: [], id: '' };
            } else {
                let hasItem = this.selectedUser.groups.find(r => r === value);      
                if (hasItem) { // já existe, então remove
                    let newArray = this.selectedUser.groups.filter(item => item !== value);
                    this.selectedUser.groups = newArray;
                } else {
                    this.selectedUser.groups.push(value);
                }                
            }
        },
        deleteUserFirebase(email, password) {
            firebase.auth().signInWithEmailAndPassword(email, password)
                .then(firebaseResponse => {
                    if (firebaseResponse.user) {
                        firebaseResponse.user.delete().then(() => {
                            console.log('user created on firebase, but deleted cause an API error')
                        });
                    }
                })
                .catch(err => console.log('error to delete user created on firebase'));
        }

    }
}
</script>

<style lang="scss">

    .users-wrapper  {
        display: grid;
        grid-template-columns: 1fr 2fr;
        grid-gap: 20px;
        margin-top: 10px;

        
            .users-list {
                height: 75vh;
                max-height: 75vh;
                overflow-y: auto;
            }
            
            .manage-user-role-group {
                display: grid;
                grid-auto-flow: row;
                grid-gap: 20px;
                height: 75vh;
                .user-role, .user-group {
                    // max-height: 36.25vh;
                    // height: 36.25vh;
                    .manage-user-item {
                        height: 100%;
                        overflow-y: auto;
                    }
                }
            }
        
    }

    @media (min-width: 320px) and (max-width: 960px) {
        .users-wrapper {
            grid-template-columns: 1fr;
            .user-role, .user-group {
                max-height: 35.5vh !important;
                height: 35.5vh !important;
            }
        }
    }



</style>