# App Funtamentals

* The system relies on layers;
* A layer can have one or more features;
* A feature is anything that plots on map (polygons, markers, points, etc);

## Config

To configure the first user and the map, access ```/config```.

The crendentials can be found on ```account.txt``` file.

> For futher information, relate to root README.md


## Mobile

The mobile application is a another project inside crimeradar. The project detects if an user is on a desktop or mobile, and then shows the interface accordingly.

Mobile version has a goal to be more intuitive for the final user, thus easier and with less options. Mainly focused on a field user with a single clicks away to get the expected result.

Its componets can be found under the ```mobile``` folder.

Since the API services are the same, some endpoints might have a few extra options there are only used on mobile project.

To disable the mobile project interface, just go to ```main.js``` file and remove the ```isMobile()``` condition. If performance is a goal, then simples delete the mobile folder and fix imports.

## Map

The project uses [leaflet](https://leafletjs.com/) as it maps, the basic function to make it work are on ```utils``` folder.
> Any other map engine can be extended with a few modifications


## API

* API calls are made with the ```getApi``` function, it receives an url and parameters;
* ```getErrors``` is a function that should be called to catch any errors on requests. It also makes the token refresh on expiration;


## Expected responses

For futher explanation, refer to [backend project readme](https://github.com/igarape/crimeradar-api).

### ```/layer```

```
    [
        {
            id: number,
            icon: string,
            order: number,
            label: {
                en: string,
                pt: string
            },
            layers: [
                {
                    active: boolean,
                    configurable: boolean,
                    editable: boolean,
                    filters: array,
                    id: number,
                    label: {
                        en: string,
                        pt: string
                    },
                    name: string,
                    order: number
                    selected: boolean,
                    style: {
                        color: string,
                        colorScale: string[],
                        extra_props: {
                            icon: string,
                            image: string
                        },
                        texture: {
                            options: string[],
                            value: string
                        },
                        types: [
                            {
                                icon: string,
                                label: string,
                                name: string,
                                value: boolean
                            }
                        ]
                    }
                }
            ],
            
        }
    ]
```

* ```active```: Determine if a layer is currently active. If false, does not appear on layers list.
* ```configurable```: Determine if a layer can be customized by user.
* ```editable```: Determine if is possible to add custom features to a layer. Currently only support marker features.
* ```filters```: Determine if a layer can use filters.
```
[
    {
        "id": number,
        "items": [
            {
                "id": number,
                "label": {
                    "en": string,
                    "pt": string
                },
                "selected": boolean,
                "text": string
            },
        ],
        "label": null,
        "mobileItems": [
            {
                "id": number,
                "label": {
                    "en": string,
                    "pt": string
                },
                "selected": boolean,
                "text": string
            },
        ],
        "name": string,
        "order": number,
        "tags": number[] || null,
        "type": null,
        "value": string,
        "values": string[],
        "visible": boolean
    },  
]
```
<sub><sup>For futher explanation refer to [backend documentation](https://github.com/igarape/crimeradar-api) or the mobile topic:</sub></sup>

> 1. ```item``` and ```mobileItems``` are different because the mobile version is a different project with a specific behavior.
> 2. The same occours to ```values``` x ```value```

* ```selected```: Determine if a layers is selected. Can also be used to load a layer once the map is opened.
* ```order```: Define in which order the layers will be displayed.
* ```color```: Define the color to plot items. It is used when the layer type ```hexagon``` is true.
* ```colorsScale```: Define which colors will be used as a color scale. It is applicable when layer type ```scale``` is true.  
```
[
    "hsl(240, 100%, 50%)",
    "hsl(180, 100%, 50%)",
    "hsl(120, 100%, 50%)",
    "hsl(60, 100%, 50%)",
    "hsl(0, 100%, 50%)"
]
```
* ```types```: Define how the layer will be displayed; Follow the example bellow to clarification.
```
types: [
    {
        "icon": "mdi-format-color-fill",
        "label": "scale",
        "name": "scale",
        "value": true
    },
    {
        "icon": "mdi-hexagon",
        "label": "hexagon",
        "name": "hexagon",
        "value": false
    },
    {
        "icon": "mdi-star-circle",
        "label": "icon",
        "name": "icon",
        "value": false
    },
    {
        "icon": "mdi-map-marker",
        "label": "marker",
        "name": "marker",
        "value": false
    },
    {
        "icon": "mdi-brightness-1",
        "label": "point",
        "name": "point",
        "value": false
    }
]
```
> 1. ```icon```: mdi icon.
> 2. ```label```: i18n label configurable in ```/public/locales```.
> 3. ```name```: unique name.
> 4. ```value```: whereas is selected or not.

* ```texture```: Define polygon texture. Value can be ```NONE```, ```HORIZONTAL```or ```VERTICAL```. Only appear if the layer is ```configurable```.
````
{
    "options": [
        "NONE",
        "HORIZONTAL",
        "VERTICAL"
    ],
    "value": "NONE"
}
````

### ```/feature```

````
{
    "features": [
        {
            "fields": [
                {
                    "extra_props": {
                        "image": string
                    },
                    "field_config_id": number,
                    "id": number,
                    "key": string,
                    "value": number
                }
            ],
            "geometry": array[],
            "id": number,
            "label": null,
            "name": string,
            "properties": {
                "id": number,
                "image": null
            },
            "style": {
                "color": string,
                "fillColor": string,
                "fillOpacity": number,
                "opacity": number,
                "weight": number
            },
            "type": string
        },
    ],
    "items": {
        "image_overlay": object[],
        "marker": object[],
        "point": object[],
        "polygon": object[]
    }
}
````

* ```fields```: Feature fields properties. Bellow a few catches:
> *On ```IMAGE OVERLAY``` feature type, ```key``` should have the image name on AWS bucket url to display* <br><br>
> <sub><sup> __*Its imperative that the image is under a folder called ```media``` and the image name is uppercased.*__</sup></sub> <br><br>
> <sub><sup>__*Refer to README.md bucket ```.env``` section.*__</sup></sub>
> 1. Another way to doing so is to use ```image``` on ```extra_props``` - needs to be implemented;
> 2. On ```IMAGE OVERLAY``` only 1 filter will be returned;
> 3. On ```IMAGE OVERLAY```, value will be provided to be used with the scale color; <br><br>
> <sub><sup>Refer to [backend documentation](https://github.com/igarape/crimeradar-api) for futher explanation. 


* ```geometry```: Leafet geometry.
* ```properties```: Feature properties. Can be different accordly to feature type. Image is only used to ```marker``` feature.

````
{
    "id": 221181,
    "image": null
}
````
> *If a ```image``` is provided, it will overwrite the ```icon``` under ```style```*.

* ```style```: Style properties. Can be different accordly to feature type:

__*[MARKER](https://leafletjs.com/reference.html#marker)*__
````
{
    "icon": "pin"
}
````
> 1. ```icon``` refers to the marker image that will show under the ```/assets/icons``` folder.
> 2. If a ```image``` is provided under feature ```properties```, the pin will then show it over the icon.

__*[POLYGON](https://leafletjs.com/reference.html#polygon) AND [IMAGE OVERLAY](https://leafletjs.com/reference.html#imageoverlay)*__
````
{
    "color": "hsl(240, 100%, 50%)",
    "fillColor": "hsl(240, 100%, 50%)",
    "fillOpacity": 0.7,
    "opacity": 1,
    "weight": 1
}
```` 

__*[POINT](https://leafletjs.com/reference.html#circle)*__

````
{
    "color": "hsl(120, 100%, 50%)",
    "fillColor": "hsl(91, 59%, 62%)",
    "fillOpacity": 0.6,
    "opacity": 0.6,
    "radius": 3,
    "stroke": false
}
````

### ```/chart```

* Charts display UI can be done by inline styling with grid css;
* You can use [echarts documentation](https://echarts.apache.org/en/index.html) as a playground to make charts exactly how desired.

<sub><sup>Refer to [backend documentation](https://github.com/igarape/crimeradar-api) for futher explanation on charts behavior.</sub></sup> 


## i18n

* i18n can be configured in ```i18n``` folder and ```main.js``` file;
* The replaced labels are on ```/public/locales```;
* Only ```en``` (English) and ```pt``` (Brazilian Portuguese) are currently supported;
* Some third party libraries does not support multilanguage, so the project relies on custom functions/i18n to display labels accordingly.


## RBAC

1. RBAC is implemented in both frontend and backend;
2. On the frontend, the project do not render components UI if an user is missing scopes;
3. ```getUserScopes``` handles that verification;
4. If a bad intentioned user tries to auto inject scopes permissions, the backend will not allow any actions.

## PWA

* Workbox can be configured over ```registerService.js```, ```vue.config.js``` and ```main.js```;
* ```manifest.json``` is over the ```/public``` folder;
* Images are under ```/public/img/icons```;
* ```VUE_APP_NODE_ENV``` must be ```production``` to enable it.

## Common Issues

* The ```overlay image``` layer has a workaround to load the svg file. If there isnt a geojson loaded, it will result in an error on request a layer of this particular type (```default.geojson``` loads to prevent it).



