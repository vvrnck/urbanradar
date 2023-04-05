<template>
  <div>
    <div v-if="isMobile" class="nav">
      <v-app-bar
        app
        height="56px"
      >
        <v-app-bar-nav-icon 
          v-show="hasMenu"
          @click.stop="drawer = !drawer"
        />

        <v-toolbar-title>
          <div class="navbar-toolbar-mobile">
            <img src="../../assets/images/logo-small.png" width="40px" />
            <div style="margin-left: 10px;">{{ $t(title) }}</div>
            <v-menu
              right
              bottom              
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

        <v-spacer></v-spacer>

        <div class="navbar-email">
          <v-icon>mdi-account-circle</v-icon>
        </div>
        
        <v-menu
          left
          bottom
          @click:outside="() => {}"
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
          class="global-overlap-index mobile-drawer"
        >
            <v-list-item>
                <v-list-item-avatar>
                    <v-avatar color="#52FFEE" class="black--text">
                      {{ getUser().email.split("")[0].toUpperCase() }}
                    </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title>{{ getUser().email }}</v-list-item-title>
                </v-list-item-content>

                <v-btn icon fab small @click="closeDrawer()">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense>
                <v-list-item 
                  link 
                  v-for="item in sectionItems" 
                  :key="item.id" 
                  @click="openLayerOptions(item)"
                >
                    <v-list-item-icon>
                      <v-icon color="#52FFEE">{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ getLabel(item, $i18n.locale) }}</v-list-item-title>
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

            <LayerMenu :layer="layerOptions" :close="() => closeLayerOptions()" />

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


    <div v-if="!isMobile" class="nav">
      <v-navigation-drawer
        v-model="drawer"
        mini-variant
        permanent
        style="transition: all 0.7s ease-in-out 0s;"
        data-v-step="navbar"
      >
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-avatar color="#52FFEE" class="black--text">
              {{ getUser().email.split("")[0].toUpperCase() }}
            </v-avatar>
          </v-list-item-avatar>

          <v-list-item-title>{{ getUser().email }}</v-list-item-title>

          <v-btn
            icon
            @click.stop="mini = !mini"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list dense>
          <v-list-item
            v-for="item in items"
            :key="item.name"
            link
            :data-v-step="'navbar-item-' + item.name"
            v-show="hasScopes(item.scopes)"
            @click="goToPage(item)"
          >
            <v-list-item-icon>
              <v-tooltip right style="z-index: 9999;">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ item.icon }}
                  </v-icon>
                </template>
                <span>
                  {{ $t(item.name) }}
                </span>
              </v-tooltip>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ $t(item.name) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-divider></v-divider>
          <v-list-item link @click="logout()" data-v-step="navbar-item-logout">
               <v-tooltip right style="z-index: 9999;">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-logout
                  </v-icon>
                </template>
                <span>
                  {{ $t('logout') }}
                </span>
              </v-tooltip>

              <v-list-item-content>
                  <v-list-item-title>Logout</v-list-item-title>
              </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
        </v-list>

      
        <v-list dense style="position: fixed; bottom: 0; width: 100%">
 
          <v-menu offset-x z-index="9999">
            <template v-slot:activator="{ on, attrs }" disabled>
                <v-list-item link v-bind="attrs" v-on="on" data-v-step="navbar-item-language">
                  
                  <v-tooltip right style="z-index: 9999;">
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        v-bind="attrs"
                        v-on="on"
                      >
                        mdi-translate
                      </v-icon>
                    </template>
                    <span>
                      {{$t("change_language")}}
                    </span>
                  </v-tooltip>

                  <v-list-item-content>
                    <v-list-item-title>{{$t("change_language")}}</v-list-item-title>
                  </v-list-item-content>
                  
                </v-list-item>
            </template>

            <v-list dense>
              <v-list-item
                v-for="(language, j) in languages"
                :key="j"
                link
              >
                <v-list-item-content @click="changeLanguage(language.language)">
                  <v-list-item-title>{{ language.name }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-menu>
 


          <v-list-item link @click="changeTheme()" data-v-step="navbar-item-theme">
            <v-list-item-icon>
              <v-tooltip right style="z-index: 9999;">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-theme-light-dark
                  </v-icon>
                </template>
                <span>
                  {{$t("change_theme")}}
                </span>
              </v-tooltip>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{$t("change_theme")}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item link @click="startTour()" data-v-step="navbar-item-tour">
            <v-list-item-icon>
              <v-tooltip right style="z-index: 9990;">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-earth
                  </v-icon>
                </template>
                <span>
                  {{$t("tour")}}
                </span>
              </v-tooltip>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{$t("change_theme")}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <div class="logo-wrapper">
                <img src="../../assets/images/logo-medium.png" class="logo">
              </div>
            </v-list-item-content>
          </v-list-item>
        </v-list>

      </v-navigation-drawer>
    </div>
  </div>
</template>

<script src="./navbar.js"></script>

<style lang="scss">
    @import "./navbar.scss";
</style>