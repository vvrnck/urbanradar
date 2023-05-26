<template>
    <div class="login-page">
        <v-flex d-flex justify-center align-center class="login-form-wrapper">
            <div class="login-form">
                <v-form>
                    <div class="form-header">
                        <img src="../../assets/images/logo.svg" alt="UrbanMap" />
                        <Loading color="#52FFEE" v-if="loading" type="linear" />
                    </div>
                    <div class="form-body">
                        <div class="form-fields">
                            <div v-for="input in inputs" :key="input.name">
                                <v-text-field
                                    dark
                                    v-model="input.value"
                                    :name="input.name"
                                    :type="input.type"
                                    :color="input.color"
                                    :counter="input.counter"
                                    :rules="input.rules"
                                    :required="input.required"
                                    :label="`${$t(input.label)}`"
                                    :append-icon="input.appendIcon.hasIcon ? input.appendIcon.iconOn : input.appendIcon.iconOff"
                                    @click:append="() => {
                                        input.appendIcon.hasIcon = !input.appendIcon.hasIcon;
                                        input.type = input.type === 'text' ? 'password' : 'text';
                                    }"
                                    @keydown.13="input.name === 'password' && login()"
                                    autocomplete="off"
                                >
                                </v-text-field>
                            </div>
                        </div>
                        <div class="form-actions">
                            <div class="form-actions-links">
                                <div @click="forgotPassword()">
                                    {{ $t('forgot_password') }}
                                </div>
                            </div>
                            <v-btn block dark @click="login()">
                                <div v-if="loading">
                                    <Loading color="#FFF" v-if="loading" type="circular" page="login" />
                                </div>
                                <div v-if="!loading">
                                    {{ $t('btn_login') }}
                                </div>
                            </v-btn>
                        </div>
                    </div>
                    <div class="form-footer">
                        <div class="system-version">
                            {{ getVersion }}
                        </div>
                    </div>
                </v-form>
            </div>
        </v-flex>
    </div>
</template>

<script>
import firebase from 'firebase/app';
import 'firebase/auth';
import { getApi, getErrors, updateMobileItem } from '../../utils';
import axios from 'axios';
import { isEmpty } from 'lodash';
import { Loading } from '../components';

export default {
    name: 'LoginPage',
    components: { Loading },
    data() {
        return {
            loading: false,
            snackbar: { open: false, color: '', text: '', timeout: 2500 },
            inputs: [ 
                { 
                    name: 'email', label: 'email', type: 'text', color: '#FFF', required: true, value: '',
                    appendIcon: { hasIcon: false, iconOn: '', iconOff: '' },
                    counter: 50,
                    rules: [ v => !!v || 'O Email é obrigatório', v => /.+@.+\..+/.test(v) || 'O email deve ser válido',]
                },
                {   
                    name: 'password', label: 'password', type: 'password', color: '#FFF', required: true, 
                    show: false, value: '',
                    counter: 20,
                    appendIcon: { hasIcon: true, iconOn: 'mdi-eye', iconOff: 'mdi-eye-off' },
                    rules: [ v => !!v || 'A Senha é obrigatória', v => (v && v.length <= 15) || 'A senha deve ter no máximo 15 caracteres',]
                }
            ]
        }
    },
    mounted() {
        
    },
    methods: {
        forgotPassword() {
            this.loading = true;

            const email = this.inputs[0];
            if (email.value === '') {
                this.loading = false;
                const snackbar = { open: true, color: '', text: 'no_email_provided', timeout: 2500, type: 'warning' };
                return this.$store.dispatch('updateSnackbar', snackbar);
            }

            firebase.auth().sendPasswordResetEmail(email.value).then(() => {
                this.loading = false;
                const snackbar = { open: true, color: '', text: 'success_reset_password', timeout: 2500, type: 'success' };
                return this.$store.dispatch('updateSnackbar', snackbar);
            }).catch((err) => {
                this.loading = false;
                const snackbar = { open: true, color: '', text: 'error_reset_password', timeout: 2500, type: 'error' };
                return this.$store.dispatch('updateSnackbar', snackbar);
            });
        },
        goFullscreen() {
            var element = document.getElementById("app");
        
            if (element.requestFullscreen) {
                element.requestFullscreen();
                updateMobileItem('fullscreen', true);
            }
            else if (element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
                updateMobileItem('fullscreen', true);
            }
            else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
                updateMobileItem('fullscreen', true);
            }
            else if (element.webkitEnterFullscreen) {
                element.webkitEnterFullscreen();
                updateMobileItem('fullscreen', true);
            }
            else if (element.msRequestFullscreen) {
                element.msRequestFullscreen();
                updateMobileItem('fullscreen', true);
            }
        },
        login() {
            this.goFullscreen();

            this.loading = true;
            const email = this.inputs[0].value;
            const senha = this.inputs[1].value;
            
            firebase.auth().signInWithEmailAndPassword(email, senha).then(async (firebaseResponse) => {
                if (firebaseResponse.error) return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_firebase', timeout: 2500, type: 'error' });
             
                const { user } = firebaseResponse;

                const token = await user.getIdToken();
                
                let url = getApi(`auth/token`);
                
                const bodyData = {
                    email: user.email,
                    access_token: token,
                    tenant_id: process.env.VUE_APP_TENANT
                }

                axios.post(url, bodyData).then(response => {
                    const { data, errors } = response.data;

                    const { active, tenants, email, token } = data;

                    if (!isEmpty(errors)) {
                        this.loading = false;
                        return getErrors(errors);
                    }
                    
                    if (isEmpty(data)) {
                        this.loading = false;
                        return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_user_not_found', timeout: 2500, type: 'error' });
                    }                    

                    axios.defaults.headers.common['Authorization'] = token.access_token;

                    const canLogin = tenants.find(tenant => tenant == process.env.VUE_APP_TENANT);

                    if (!canLogin) {
                        this.loading = false;
                        return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_user_without_permission', timeout: 2500, type: 'error' });
                    }

                    if (active) {
                        let loginURL = getApi(`auth/tenant/${process.env.VUE_APP_TENANT}/token`);
                        
                        axios.post(loginURL).then(response => {
                            const { data : { email, name, roles, token: { scope, access_token } } } = response.data;
                            localStorage.setItem('crimeradarToken', access_token);
                            sessionStorage.setItem('user', JSON.stringify({ name, roles, scope, tenants, email }));
                            this.loading = false;
                            this.$router.push({ name: 'map' }).catch(err => console.log(err));
                        }).catch(err => {
                            console.log(err);
                            this.loading = false;
                            return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_api', timeout: 2500, type: 'error' });
                        });
                    } else {
                        this.loading = false;
                        return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_user_not_active', timeout: 2500, type: 'error' });
                    }

                }).catch(err => {
                    this.loading = false;
                    return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_api', timeout: 2500, type: 'error' });
                })
            }).catch(firebaseErr => {
                this.loading = false;
                return this.$store.dispatch('updateSnackbar', { open: true, color: '', text: 'error_firebase', timeout: 2500, type: 'error' });
            });
        }
    },
    computed: {
        getVersion: () => {
            const version = process.env.VUE_APP_VERSION;
            return `v.${version}`;
        }
    }
}
</script>

<style lang="scss">
    .login-page {
        overflow: auto;
        filter: brightness(80%);
        height: 100vh;
        background-image: url("../../assets/images/background.jpg");
        background-position: center;
        background-size: cover;
        .login-form-wrapper {
            height: 100%;
            .login-form {
                border: 1px solid #000;
                background-color: #080808;
                opacity: 0.9;
                color: white;
                max-width: 360px;
                width: 60%;
                .form-header {
                    margin-bottom: 10px;
                }
                .form-body {
                    padding: 0 25px 10px 25px;
                    .form-fields {
                        margin-bottom: 10px;
                        .v-text-field__details {
                            justify-content: flex-end;
                        }
                    }
                    .form-actions {
                        .form-actions-links {
                            display: flex;
                            justify-content: space-between;
                            margin: 0 0 15px 0;
                            color: #b5b5b5;
                            font-size: 12px;
                            div {
                                cursor: pointer;
                                &:hover {
                                    color: #FFF;
                                }
                            }
                            
                        }
                    }
                }
                .form-footer {
                    position: relative;
                    height: 20px;
                    color: #b5b5b5;
                    .system-version {
                        position: absolute;
                        right: 10px;
                        font-size: 12px;
                    }
                }
            }
        }
    }

    @media (max-width: 960px) {
        .login-form {
            width: 90% !important;
        }
    }

</style>