import firebase from 'firebase/app';
import 'firebase/auth';
import axios from 'axios';
import { getApi, getErrors } from '../../utils';
import { isEmpty } from 'lodash';

import Snackbar from '../snackbar/Snackbar.vue';
import Loading from '../loading/Loading.vue';

export default {
    name: 'LoginPage',
    components: { Snackbar, Loading },
    data() {
        return {
            loading: false,
            inputs: [ 
                { 
                    name: 'email', label: 'email', type: 'text', color: '#FFF', required: true, value: '',
                    appendIcon: { hasIcon: false, iconOn: '', iconOff: '' },
                    counter: 50,
                    rules: [ 
                            v => !!v || this.getMessage('REQUIRED_EMAIL'), 
                            v => /.+@.+\..+/.test(v) || this.getMessage('VALID_EMAIL'),
                        ]
                },
                {   
                    name: 'password', label: 'password', type: 'password', color: '#FFF', required: true, 
                    show: false, value: '',
                    counter: 20,
                    appendIcon: { hasIcon: true, iconOn: 'mdi-eye', iconOff: 'mdi-eye-off' },
                   // rules: [ v => !!v || 'A Senha é obrigatória', v => (v && v.length <= 15) || 'A senha deve ter no máximo 15 caracteres',]
                }
            ],
            languages: [
                { name: 'portuguese', label: 'Português (Brasil)', type: 'pt-BR', language: 'pt' },
                { name: 'english', label: 'English', type: 'en-US', language: 'en' }
            ]
        }
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
        changeLanguage(language) {
            this.$i18n.locale = language;
        },
        getMessage(type) {
            switch(type) {
                case 'REQUIRED_EMAIL':
                    return this.$i18n.locale === 'en' ? `Email address is mandatory` : 'O email é obrigatório'
                case 'VALID_EMAIL':
                    return this.$i18n.locale === 'en' ? 'It must be a valid email address' : 'Deve ser um email válido'
                default:
                    return ''
            }
        },
        login() {
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
                            const { data : { email, name, roles, token: { scope, access_token, feature_collections, tenant_id } } } = response.data;
                            localStorage.setItem('crimeradarToken', access_token);
                            sessionStorage.setItem('featureCollections', JSON.stringify(feature_collections));
                            sessionStorage.setItem('tenantId', tenant_id);
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