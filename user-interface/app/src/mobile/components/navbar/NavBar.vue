<template>
  <div class="navbar">
     <v-app-bar
      app
      color="black"
      dark
      height="56px"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" v-show="hasMenu"></v-app-bar-nav-icon>

      <v-toolbar-title>
        <div class="navbar-toolbar-desktop">
          {{  $t(title) }}
          <img width="100px" src="../../../assets/images/logo.svg" class="logo-principal" />
        </div>

        <div class="navbar-toolbar-mobile">
          <img src="../../../assets/images/logo.png" width="40px" />
          <div style="margin-left: 10px;">{{ $t(title) }}</div>
          <v-menu
            right
            bottom
            dark
            class="global-overlap-index"
            close-on-click
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-menu-down</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-item
                v-for="item in items"
                :key="item.label"
                @click="() => {}"
              >
                <v-list-item-title @click="goToPage(item)">{{ $t(item.name) }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          
        </div>
        
      </v-toolbar-title>

      
      

      <v-toolbar-items class="ml-5">
        <div class="navbar-toolbar-items">
          <div v-for="item in items" :key="item.label" class="navbar-toolbar-item" @click="goToPage(item)">
            {{ $t(item.name) }}
          </div>
        </div>
      </v-toolbar-items>


      <v-spacer></v-spacer>

      <div class="navbar-email">
        <v-icon dark>mdi-account-circle</v-icon>
        <!-- {{ getUser().email }} -->
      </div>

       <v-menu
        left
        bottom
        @click:outside="() => {}"
        dark
        class="global-overlap-index"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="option in options"
            :key="option.label"
            @click="() => {}"
          >
            <v-list-item-title>{{ option.label }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      

    </v-app-bar>     
       <v-navigation-drawer
          v-model="drawer"
          absolute
          temporary
          dark
          class="global-overlap-index drawer"
          color="#131313"
        >
            <v-list-item>
                <v-list-item-avatar>
                    <v-avatar color="#52FFEE" class="black--text">
                      <!-- {{ getUser().email.split("")[0].toUpperCase() }} -->
                    </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                    <!-- <v-list-item-title>{{ getUser().email }}</v-list-item-title> -->
                </v-list-item-content>

                <v-btn icon fab dark small @click="closeDrawer()">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense>
                <v-list-item link v-for="menuItem in menuItems" :key="menuItem.order" @click="openLayerOptions(menuItem)">
                    <v-list-item-icon>
                      <v-icon color="#52FFEE">mdi-home</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ menuItem.section && menuItem.section.display_name }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
             
                <v-divider></v-divider>
                <v-list-item link @click="logout()">
                    <v-list-item-icon><v-icon>mdi-keyboard-return</v-icon></v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>Sair</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>

            <LayerMenu :layer="layerOptions" :close="() => closeLayerOptions()" :availableDates="availableDates" />

            <div class="drawer-actions-wrapper">
              <div class="drawer-actions-buttons">
              <v-btn rounded dark color="#F44E3B" min-width="105" ripple @click="resetMapConfigs()">
                {{$t("btn_reset")}}
              </v-btn>
              <v-btn rounded dark color="#6DC1B2" min-width="105" ripple @click="getFeatures()">
                {{$t("btn_apply")}}
              </v-btn>
              </div>
            </div>

        </v-navigation-drawer>
  </div>
</template>

<script>
import axios from 'axios';
import firebase from 'firebase/app'
import 'firebase/auth';
import { getApi } from '../../../utils';
import LayerMenu from '../layer-menu/LayerMenu';
import moment from 'moment';
import { mapGetters } from 'vuex';

export default {
    name: "NavBar",
    props: ["user", "title", "loadFeatures", "reset", "hasMenu"],
    components: { LayerMenu },
    data() {
      return {
        drawer: false,
        items: [
          { icon: "mdi-home", name: "map", label: "Map", scopes: [""], route: "map" },
          { icon: "mdi-home", name: "management", label: "Management", scopes: [""], route: "manage" },
          { icon: "mdi-home", name: "feedback", label: "User Feedback", scopes: [""], route: "feedback" },
          { icon: "mdi-home", name: "helper", label: "Helper", scopes: [""], route: "help" },       
        ],   
        options: [
          { icon: "mdi-home", label: "Users", scopes: [""] },
          { icon: "mdi-home", label: "Feedbacks List", scopes: [""] },
          { icon: "mdi-home", label: "Exit", scopes: [""] }
        ],
        layerOptions: {
          show: false,
          sectionName: null,
          options: []
        },
        availableDates: null
      }
    },

    mounted() {
      const url = getApi('layer');
      axios.get(url).then(response => {
        const newData = Object.assign({}, response.data);
        const initialMenuData = Object.assign({}, response.data);
        
        // configs que o back deve enviar
        Object.values(newData).map(section => {
          section.data.map(layer => {
            const date = moment().format('YYYY-MM-DD');
            layer.dates = [date, date]
            layer.colorScale = layer.colorFeat;
            layer.rateScale = [0.1, 0.2, 0.4, 0.6, 0.7, 1];
            layer.types = [
              { name: 'hexagon', value: false },
              { name: 'scale', value: false },
              { name: 'icon', value: false },
              { name: 'marker', value: false },
              { name: 'point', value: false }
            ];
            layer.texture = {
              value: 'NONE',
              options: ['NONE', 'HORIZONTAL', 'VERTICAL']
            }
            layer.open = false;

            layer.filters = [];
            layer.groups.map((g, i) => {
              layer.filters[i] = {
                type: g.type,
                name: g.type,
                label: g.type,
                value: '',
                items: [],
                tags: []
              };
              g.subtype.map(s => {
                layer.filters[i].items.push({
                    'id': s.id,
                    'text': s.name,
                    'toLowerCase': () => s.name.toLowerCase(),
                    'toString': () => s.name
                })
              })
            })
          })
        })

        this.$store.dispatch('updateMenu', newData);
        localStorage.setItem('initialMenuData', JSON.stringify(initialMenuData));
      })  
    },
    methods: {   
      goToPage(item) {
        this.$router.push(item.route).catch(err => console.warn(err));
      },
      resetMapConfigs() {
        this.reset().then(() => {
          const initialMenuData = JSON.parse(localStorage.getItem('initialMenuData'));
          this.$store.dispatch('updateMenu', initialMenuData);
          this.layerOptions = {
            show: false,
            sectionName: null,
            options: []
          }
        })
      }, 
      getFeatures() {
        this.loadFeatures().then(() => {
          this.drawer = false;
          this.$store.dispatch('updateCaption', true);
        })
      },
      closeDrawer() {
        this.drawer = false;
      },  
      openLayerOptions(menuItem) {
        this.layerOptions = {
          show: true,
          name: menuItem.section.name,
          options: menuItem.data
        }
      },
      closeLayerOptions() {
        this.layerOptions.show = false;
      },
      getUser () {
        const currentUser = firebase.auth().currentUser;
        return currentUser;
      },
      changeTheme() {
          this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
      },
      logout() {
        //clearUserSession();
      },
    },
    computed: {
      menuItems() {
        return this.$store.getters.menu;
      }
    }
}
</script>

<style lang="scss">
  .global-overlap-index, .navbar {
    z-index: 99999 !important;
  }

  .map-loading {
    position: absolute;
    top: 56px;
    width: 100%;
  }

  .drawer {
    opacity: 0.90;
    .drawer-actions-wrapper {
      position: absolute;
      bottom: 0;
      justify-content: center;
      align-items: center;
      display: flex;
      padding: 10px;
      width: 100%;
      .drawer-actions-buttons {
        display: grid;
        grid-auto-flow: column;
        grid-gap: 10px;
        margin: auto;
      }
      
    }
  }

  @media (min-width: 960px) {
    .navbar-toolbar-desktop { display: grid; grid-auto-flow: column; grid-gap: 10px; align-items: center; }
    .navbar-toolbar-mobile { display: none; }
    .navbar-toolbar-items {
      display: grid;
      grid-auto-flow: column;
      justify-content: center;
      align-items: center;
      .navbar-toolbar-item {
        font-size: 14px;
        text-transform: uppercase;
        padding: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        height: 100%;
        &:hover {
          background-color: #696969;
        }
      }
    }
    
    .navbar-email {
      font-size: 18px;
    }
    
    .drawer {
      width: 40% !important;
      max-width: 600px !important;
    }
  }

  @media (max-width: 960px) {
    .v-toolbar__title { padding-left: 0 !important; }
    .navbar-toolbar-desktop { display: none; }
    .navbar-toolbar-mobile {
      display: grid; grid-template-columns: 1fr 1fr 5fr; align-items: center
    }
    .navbar-toolbar-items { 
      display: none;
    }

    .navbar-email {
      display: none;
    }

    .drawer {
      width: 100vh !important;
    }
  }
</style>