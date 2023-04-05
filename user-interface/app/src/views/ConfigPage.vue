<template>
    <div class="wrapper">
        <div v-if="showConfig" class="center">
            <div>
                <v-btn
                    class="mx-2"
                    fab
                    x-small
                    color="primary"
                    @click="showConfig = false"
                >
                    <v-icon>
                        mdi-arrow-left
                    </v-icon>
                </v-btn>
            </div>
            <div>
                <div class="form-fields">
                    <form>
                        <v-text-field
                            v-model="data.user.email"
                            name="email"
                            type="email"
                            :required="true"
                            color="#FFF"
                            label="Email"
                            :rules="[
                                v => !!v, 
                                v => /.+@.+\..+/.test(v),
                            ]"
                            autocomplete="off"
                        >
                        </v-text-field>
                        <v-text-field
                            v-model="data.user.password"
                            name="password"
                            type="password"
                            :required="true"
                            color="#FFF"
                            label="Password"
                            autocomplete="off"
                        >
                        </v-text-field>
                        <v-text-field
                            v-model="data.user.confirmPassword"
                            name="confirmPassword"
                            type="password"
                            :required="true"
                            color="#FFF"
                            label="Confirm Password"
                            autocomplete="off"
                        >
                        </v-text-field>
                    </form>
                </div>
                <v-btn block @click="createUser()" :disabled="checkInputs()">
                    Create Admin User
                </v-btn>
            </div>
        </div>
        <div class="form" v-else>
            <div class="form-fields">
                <div v-for="input in inputs" :key="input.name">
                    <v-text-field
                        v-model="input.value"
                        :name="input.name"
                        :type="input.type"
                        :color="input.color"
                        :required="input.required"
                        :label="input.label"
                        autocomplete="off"
                    >
                    </v-text-field>
                </div>
            </div>
            <div>
                <v-btn block @click="login()">
                    <div>
                        {{ $t('btn_login') }}
                    </div>
                </v-btn>
            </div>
        </div>
    </div>
</template>
 
<script>
import firebase from 'firebase/app'
import 'firebase/auth';
import axios from 'axios';
import { getApi, getErrors } from '../utils';
import { isEmpty } from 'lodash';

export default {
    name: 'ConfigPage',
    data() {
        return {
            showConfig: false,
            inputs: [ 
                { name: 'username', label: 'Username', type: 'text', color: '#FFF', required: true, value: '', },
                { name: 'password', label: 'Password', type: 'password', color: '#FFF', required: true, value: '' }
            ],
            data: { 
                role: { name: '', scopes: [] }, 
                user: { name: '', roles: [], email: '', password: '', confirmPassword: '' },
            },
        }
    },
    methods: {
        checkInputs() {
            let isDisabled = true;
            if (
                this.data.user.password === this.data.user.confirmPassword 
                && (this.data.user.password !== '' 
                && this.data.user.confirmPassword !== '')
                && /.+@.+\..+/.test(this.data.user.email)
            ) {
                isDisabled = false;
            }

            return isDisabled;
        },  
        async login() {
            const data = {
                username: this.inputs[0].value,
                password: this.inputs[1].value,
            }
            axios.post("/configuration", data).then(res => {
                const { login } = res.data;
                if (!login) {
                    const snackbar = { open: true, color: '', text: 'error_config_login', timeout: 2500, type: 'error' }; 
                    return this.$store.dispatch('updateSnackbar', snackbar);  
                }
                this.showConfig = true;
                this.getRoles();
            });
        },
        async createUser() {

            if (!this.roles) return;
            
            let url = getApi('user');
            const data = this.data;

            firebase.auth().createUserWithEmailAndPassword(this.email, this.password)
                .then(firebaseResponse => {

                    const adminRole = this.roles.filter(item => item.name === "admin");

                    let sendData = {
                        uid: firebaseResponse.user.uid,
                        email: firebaseResponse.user.email,
                        name: data.user.email,
                        role: adminRole,
                        active: true, 
                        roles: this.roles
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
    }
}
</script>

<style>

.wrapper {
    background-image: url("../assets/images/background.jpg");
    background-position: center;
    background-size: cover;
    width: 100%;
    height: 100%;
}

.form {
    display: flex;
    margin: 10% auto;
    gap: 15px;
    flex-direction: column;
    width: 35%;
    padding: 10px;
    background-color: #080808;
    border-radius: 5px;
}

.form-fields {
    padding: 20px;
    background-color: #080808;
}


.center {
    display: flex;
    margin: 10% auto;
    gap: 15px;
    flex-direction: column;
    width: 30%;
    padding: 10px;
    background-color: #080808;
    border-radius: 5px;
}

</style>