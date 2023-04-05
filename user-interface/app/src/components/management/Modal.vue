<template>
    <v-row justify="space-around">
        <v-col cols="auto">
        <v-dialog
            max-width="600"
            v-model="modal.open"
            @click:outside="() => close()"
        >
            <template>
                <v-card>
                    <v-toolbar
                        color="primary"
                        dark
                    >
                        <div class="text-h5">{{ $t(modal.type.title) }}</div>
                    </v-toolbar>
                    <Loading :color="color" type="linear" v-if="loading" />
                    <v-card-text class="card-wrapper">
                        <div class="text pt-10">
                            <div v-if="modal.type.type === 'users'">
                                <div v-if="modal.mode === 'create'">
                                    <v-row>
                                        <v-col cols="12" sm="12">
                                            <v-text-field
                                                v-model="data.user.email"
                                                :label="$t('label_email')"
                                                hide-details="auto"
                                                dense
                                                outlined
                                            ></v-text-field>
                                        </v-col>


                                        <v-col cols="12" sm="12">
                                            <v-text-field
                                                v-model="data.user.name"
                                                :label="$t('label_name')"
                                                hide-details="auto"
                                                dense
                                                outlined
                                            ></v-text-field>
                                        </v-col>

                                        <v-col cols="12" sm="12">
                                            <v-autocomplete
                                                v-model="data.user.roles"
                                                :items="listItems"
                                                outlined
                                                dense
                                                
                                                hide-details="auto"
                                                small-chips
                                                :label="$t('label_role')"
                                                multiple
                                            ></v-autocomplete>
                                        </v-col>

                                        <v-col
                                            cols="12"
                                            sm="6"
                                            >
                                            <v-text-field
                                                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                                                :rules="[rules.required, rules.min]"
                                                :type="show1 ? 'text' : 'password'"
                                                name="input-10-2"
                                                :label="$t('label_password')"
                                                :hint="$t('min_char')"
                                                v-model="data.user.password"
                                                hide-details="auto"
                                                outlined
                                                dense
                                                @click:append="show1 = !show1"
                                            ></v-text-field>
                                        </v-col>

                                            <v-col
                                            cols="12"
                                            sm="6"
                                            >
                                            <v-text-field
                                                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                                                :rules="[rules.required, rules.min]"
                                                :type="show2 ? 'text' : 'password'"
                                                name="input-10-2"
                                                :label="$t('label_confirm_password')"
                                                :hint="$t('min_char')"
                                                v-model="data.user.confirmPassword"
                                                hide-details="auto"
                                                dense
                                                outlined
                                                @click:append="show2 = !show2"
                                            ></v-text-field>
                                            </v-col>


                                    </v-row>
                                </div>

                                 <div v-if="modal.mode === 'edit'">
                                    <v-row>
                                        <v-col cols="12" sm="12">
                                            <v-text-field
                                                v-model="editingData.email"
                                                :label="$t('label_email')"
                                                hide-details="auto"
                                                dense
                                                outlined
                                            ></v-text-field>
                                        </v-col>


                                        <v-col cols="12" sm="12">
                                            <v-text-field
                                                v-model="editingData.name"
                                                :label="$t('label_name')"
                                                hide-details="auto"
                                                dense
                                                outlined
                                            ></v-text-field>
                                        </v-col>

                                        <v-col cols="12" sm="12">
                                            <v-autocomplete
                                                v-model="editingData.roles"
                                                :items="listItems"
                                                outlined
                                                dense
                                                chips
                                                hide-details="auto"
                                                small-chips
                                                :label="$t('label_role')"
                                                multiple
                                            ></v-autocomplete>
                                        </v-col>
                                    </v-row>
                                </div>
                            </div>
                           
                            
                            
                            
                            <div v-if="modal.type.type === 'role'">
                                <div class="role" v-if="modal.mode === 'create'">
                                    <v-text-field
                                        v-model="data.role.name"
                                        :label="$t('label_name')"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    ></v-text-field>
                                    
                                    <v-autocomplete
                                        v-model="data.role.scopes"
                                        chips
                                        small-chips
                                        multiple
                                        outlined
                                        :items="listItems"
                                        :label="$t('scopes')"
                                    >
                                        <template v-slot:selection="data">
                                            <v-chip
                                                v-bind="data.attrs"
                                                :input-value="data.selected"
                                                close
                                                small
                                                @click="data.select"
                                                @click:close="(e) => remove(e, data.item)"
                                            >
                                                {{ data.item }}
                                            </v-chip>
                                        </template>
                                    
                                    </v-autocomplete>
                                </div>

                                <div class="role" v-if="modal.mode === 'edit'">
                                     <v-text-field
                                        v-model="editingData.name"
                                        :label="$t('label_name')"
                                        hide-details="auto"
                                        dense
                                        outlined
                                    ></v-text-field>
                                    
                                    <v-autocomplete
                                        v-model="editingData.scopes"
                                        chips
                                        small-chips
                                        multiple
                                        outlined
                                        :items="listItems"
                                        :label="$t('scopes')"
                                    />

                                </div>

                            </div>
                        </div>
                    </v-card-text>
                    <v-card-actions class="justify-end">
                        <v-btn
                            :color="color"
                            @click="() => closeModal()"
                            text
                            ripple
                            width="75"
                        >{{$t('dialog_close')}}</v-btn>
                        
                        <v-btn
                            v-if="modal.mode === 'edit'"
                            color="green darken-1"
                            @click="confirmModal(editingData)"
                            filled
                            :disabled="loading"
                            ripple
                            width="75"
                        >{{$t('dialog_edit')}}</v-btn>

                        <v-btn
                            v-if="modal.mode === 'create'"
                            color="green darken-1"
                            @click="confirmModal(data)"
                            filled
                            :disabled="loading"
                            ripple
                            width="75"
                        >{{$t('dialog_save')}}</v-btn>

                        
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
import axios from 'axios';
import Loading from '../loading/Loading.vue'

export default {
    name: 'Modal',
    components: { Loading },
    props: ['modal', 'close', 'loading', 'color', 'save', 'editingData', 'listItems'],
    data() {
        return {
            data: { 
                role: { name: '', scopes: [] }, 
                user: { name: '', roles: [], email: '', password: '', confirmPassword: '' },
            },
            show1: false,
            show2: false,
            rules: {
                required: value => !!value || this.getMessage('REQUIRED'),
                min: v => v.length >= 6 || this.getMessage('MIN_CHAR')
            },
            scopes: [],
            roles: [],
        }
    },
    methods: {
        closeModal() {
            this.clearData().then(() => this.close());
        },       
        confirmModal(data) {
            this.save(data);
        },
        remove (e, item) {      
            const index = this.data.role.scopes.indexOf(item)
            if (index >= 0) this.data.role.scopes.splice(index, 1)
        },
        getMessage(type) {
            switch(type) {
                case 'REQUIRED':
                    return this.$i18n.locale === 'en' ? 'Required' : 'Obrigatório';
                case 'MIN_CHAR':
                    return this.$i18n.locale === 'en' ? 'Min 6 characters' : 'Mínimo de 6 caracteres';
                default:
                    return ''
            }
        },
        async clearData() {
            this.data = { 
                role: { name: '', scopes: [] }, 
                user: { name: '', roles: [], email: '', password: '', confirmPassword: '' },
            }
        }
    }
}
</script>

<style lang="scss">
.card-wrapper {
    min-height: 200px;
    .role {
        display: grid;
        grid-auto-flow: row;
        grid-gap: 25px;
    }
}

</style>