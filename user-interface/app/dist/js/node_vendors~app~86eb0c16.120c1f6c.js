(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["node_vendors~app~86eb0c16"],{"0698":function(t,e,i){"use strict";var r=i("2cf4"),n=i("6d8b"),a=i("21a1"),s=i("6fd3"),o=i("3437"),l=i("5210"),h=i("9850"),d=i("4bc4"),c=i("726e");function _(t,e,i){var r=c["d"].createCanvas(),n=e.getWidth(),a=e.getHeight(),s=r.style;return s&&(s.position="absolute",s.left="0",s.top="0",s.width=n+"px",s.height=a+"px",r.setAttribute("data-zr-dom-id",t)),r.width=n*i,r.height=a*i,r}var f=function(t){function e(e,i,a){var s,o=t.call(this)||this;o.motionBlur=!1,o.lastFrameAlpha=.7,o.dpr=1,o.virtual=!1,o.config={},o.incremental=!1,o.zlevel=0,o.maxRepaintRectCount=5,o.__dirty=!0,o.__firstTimePaint=!0,o.__used=!1,o.__drawIndex=0,o.__startIndex=0,o.__endIndex=0,o.__prevStartIndex=null,o.__prevEndIndex=null,a=a||r["e"],"string"===typeof e?s=_(e,i,a):n["A"](e)&&(s=e,e=s.id),o.id=e,o.dom=s;var l=s.style;return l&&(n["j"](s),s.onselectstart=function(){return!1},l.padding="0",l.margin="0",l.borderWidth="0"),o.painter=i,o.dpr=a,o}return Object(a["a"])(e,t),e.prototype.getElementCount=function(){return this.__endIndex-this.__startIndex},e.prototype.afterBrush=function(){this.__prevStartIndex=this.__startIndex,this.__prevEndIndex=this.__endIndex},e.prototype.initContext=function(){this.ctx=this.dom.getContext("2d"),this.ctx.dpr=this.dpr},e.prototype.setUnpainted=function(){this.__firstTimePaint=!0},e.prototype.createBackBuffer=function(){var t=this.dpr;this.domBack=_("back-"+this.id,this.painter,t),this.ctxBack=this.domBack.getContext("2d"),1!==t&&this.ctxBack.scale(t,t)},e.prototype.createRepaintRects=function(t,e,i,r){if(this.__firstTimePaint)return this.__firstTimePaint=!1,null;var n,a=[],s=this.maxRepaintRectCount,o=!1,l=new h["a"](0,0,0,0);function c(t){if(t.isFinite()&&!t.isZero())if(0===a.length){var e=new h["a"](0,0,0,0);e.copy(t),a.push(e)}else{for(var i=!1,r=1/0,n=0,d=0;d<a.length;++d){var c=a[d];if(c.intersect(t)){var _=new h["a"](0,0,0,0);_.copy(c),_.union(t),a[d]=_,i=!0;break}if(o){l.copy(t),l.union(c);var f=t.width*t.height,u=c.width*c.height,p=l.width*l.height,v=p-f-u;v<r&&(r=v,n=d)}}if(o&&(a[n].union(t),i=!0),!i){e=new h["a"](0,0,0,0);e.copy(t),a.push(e)}o||(o=a.length>=s)}}for(var _=this.__startIndex;_<this.__endIndex;++_){var f=t[_];if(f){var u=f.shouldBePainted(i,r,!0,!0),p=f.__isRendered&&(f.__dirty&d["a"]||!u)?f.getPrevPaintRect():null;p&&c(p);var v=u&&(f.__dirty&d["a"]||!f.__isRendered)?f.getPaintRect():null;v&&c(v)}}for(_=this.__prevStartIndex;_<this.__prevEndIndex;++_){f=e[_],u=f.shouldBePainted(i,r,!0,!0);if(f&&(!u||!f.__zr)&&f.__isRendered){p=f.getPrevPaintRect();p&&c(p)}}do{n=!1;for(_=0;_<a.length;)if(a[_].isZero())a.splice(_,1);else{for(var y=_+1;y<a.length;)a[_].intersect(a[y])?(n=!0,a[_].union(a[y]),a.splice(y,1)):y++;_++}}while(n);return this._paintRects=a,a},e.prototype.debugGetPaintRects=function(){return(this._paintRects||[]).slice()},e.prototype.resize=function(t,e){var i=this.dpr,r=this.dom,n=r.style,a=this.domBack;n&&(n.width=t+"px",n.height=e+"px"),r.width=t*i,r.height=e*i,a&&(a.width=t*i,a.height=e*i,1!==i&&this.ctxBack.scale(i,i))},e.prototype.clear=function(t,e,i){var r=this.dom,a=this.ctx,s=r.width,h=r.height;e=e||this.clearColor;var d=this.motionBlur&&!t,c=this.lastFrameAlpha,_=this.dpr,f=this;d&&(this.domBack||this.createBackBuffer(),this.ctxBack.globalCompositeOperation="copy",this.ctxBack.drawImage(r,0,0,s/_,h/_));var u=this.domBack;function p(t,i,r,s){if(a.clearRect(t,i,r,s),e&&"transparent"!==e){var h=void 0;if(n["x"](e)){var p=e.global||e.__width===r&&e.__height===s;h=p&&e.__canvasGradient||Object(o["a"])(a,e,{x:0,y:0,width:r,height:s}),e.__canvasGradient=h,e.__width=r,e.__height=s}else n["y"](e)&&(e.scaleX=e.scaleX||_,e.scaleY=e.scaleY||_,h=Object(l["c"])(a,e,{dirty:function(){f.setUnpainted(),f.__painter.refresh()}}));a.save(),a.fillStyle=h||e,a.fillRect(t,i,r,s),a.restore()}d&&(a.save(),a.globalAlpha=c,a.drawImage(u,t,i,r,s),a.restore())}!i||d?p(0,0,s,h):i.length&&n["k"](i,(function(t){p(t.x*_,t.y*_,t.width*_,t.height*_)}))},e}(s["a"]),u=f,p=i("98b7"),v=i("22d1"),y=1e5,g=314159,w=.01,b=.001;function x(t){return!!t&&(!!t.__builtin__||"function"===typeof t.resize&&"function"===typeof t.refresh)}function m(t,e){var i=document.createElement("div");return i.style.cssText=["position:relative","width:"+t+"px","height:"+e+"px","padding:0","margin:0","border-width:0"].join(";")+";",i}var L=function(){function t(t,e,i,a){this.type="canvas",this._zlevelList=[],this._prevDisplayList=[],this._layers={},this._layerConfig={},this._needsManuallyCompositing=!1,this.type="canvas";var s=!t.nodeName||"CANVAS"===t.nodeName.toUpperCase();this._opts=i=n["m"]({},i||{}),this.dpr=i.devicePixelRatio||r["e"],this._singleCanvas=s,this.root=t;var l=t.style;l&&(n["j"](t),t.innerHTML=""),this.storage=e;var h=this._zlevelList;this._prevDisplayList=[];var d=this._layers;if(s){var c=t,_=c.width,f=c.height;null!=i.width&&(_=i.width),null!=i.height&&(f=i.height),this.dpr=i.devicePixelRatio||1,c.width=_*this.dpr,c.height=f*this.dpr,this._width=_,this._height=f;var p=new u(c,this,this.dpr);p.__builtin__=!0,p.initContext(),d[g]=p,p.zlevel=g,h.push(g),this._domRoot=t}else{this._width=Object(o["b"])(t,0,i),this._height=Object(o["b"])(t,1,i);var v=this._domRoot=m(this._width,this._height);t.appendChild(v)}}return t.prototype.getType=function(){return"canvas"},t.prototype.isSingleCanvas=function(){return this._singleCanvas},t.prototype.getViewportRoot=function(){return this._domRoot},t.prototype.getViewportRootOffset=function(){var t=this.getViewportRoot();if(t)return{offsetLeft:t.offsetLeft||0,offsetTop:t.offsetTop||0}},t.prototype.refresh=function(t){var e=this.storage.getDisplayList(!0),i=this._prevDisplayList,r=this._zlevelList;this._redrawId=Math.random(),this._paintList(e,i,t,this._redrawId);for(var n=0;n<r.length;n++){var a=r[n],s=this._layers[a];if(!s.__builtin__&&s.refresh){var o=0===n?this._backgroundColor:null;s.refresh(o)}}return this._opts.useDirtyRect&&(this._prevDisplayList=e.slice()),this},t.prototype.refreshHover=function(){this._paintHoverList(this.storage.getDisplayList(!1))},t.prototype._paintHoverList=function(t){var e=t.length,i=this._hoverlayer;if(i&&i.clear(),e){for(var r,n={inHover:!0,viewWidth:this._width,viewHeight:this._height},a=0;a<e;a++){var s=t[a];s.__inHover&&(i||(i=this._hoverlayer=this.getLayer(y)),r||(r=i.ctx,r.save()),Object(l["a"])(r,s,n,a===e-1))}r&&r.restore()}},t.prototype.getHoverLayer=function(){return this.getLayer(y)},t.prototype.paintOne=function(t,e){Object(l["b"])(t,e)},t.prototype._paintList=function(t,e,i,r){if(this._redrawId===r){i=i||!1,this._updateLayerStatus(t);var n=this._doPaintList(t,e,i),a=n.finished,s=n.needsRefreshHover;if(this._needsManuallyCompositing&&this._compositeManually(),s&&this._paintHoverList(t),a)this.eachLayer((function(t){t.afterBrush&&t.afterBrush()}));else{var o=this;Object(p["a"])((function(){o._paintList(t,e,i,r)}))}}},t.prototype._compositeManually=function(){var t=this.getLayer(g).ctx,e=this._domRoot.width,i=this._domRoot.height;t.clearRect(0,0,e,i),this.eachBuiltinLayer((function(r){r.virtual&&t.drawImage(r.dom,0,0,e,i)}))},t.prototype._doPaintList=function(t,e,i){for(var r=this,a=[],s=this._opts.useDirtyRect,o=0;o<this._zlevelList.length;o++){var l=this._zlevelList[o],h=this._layers[l];h.__builtin__&&h!==this._hoverlayer&&(h.__dirty||i)&&a.push(h)}for(var d=!0,c=!1,_=function(n){var o,l=a[n],h=l.ctx,_=s&&l.createRepaintRects(t,e,f._width,f._height),u=i?l.__startIndex:l.__drawIndex,p=!i&&l.incremental&&Date.now,v=p&&Date.now(),y=l.zlevel===f._zlevelList[0]?f._backgroundColor:null;if(l.__startIndex===l.__endIndex)l.clear(!1,y,_);else if(u===l.__startIndex){var g=t[u];g.incremental&&g.notClear&&!i||l.clear(!1,y,_)}-1===u&&(console.error("For some unknown reason. drawIndex is -1"),u=l.__startIndex);var w=function(e){var i={inHover:!1,allClipped:!1,prevEl:null,viewWidth:r._width,viewHeight:r._height};for(o=u;o<l.__endIndex;o++){var n=t[o];if(n.__inHover&&(c=!0),r._doPaintEl(n,l,s,e,i,o===l.__endIndex-1),p){var a=Date.now()-v;if(a>15)break}}i.prevElClipPaths&&h.restore()};if(_)if(0===_.length)o=l.__endIndex;else for(var b=f.dpr,x=0;x<_.length;++x){var m=_[x];h.save(),h.beginPath(),h.rect(m.x*b,m.y*b,m.width*b,m.height*b),h.clip(),w(m),h.restore()}else h.save(),w(),h.restore();l.__drawIndex=o,l.__drawIndex<l.__endIndex&&(d=!1)},f=this,u=0;u<a.length;u++)_(u);return v["a"].wxa&&n["k"](this._layers,(function(t){t&&t.ctx&&t.ctx.draw&&t.ctx.draw()})),{finished:d,needsRefreshHover:c}},t.prototype._doPaintEl=function(t,e,i,r,n,a){var s=e.ctx;if(i){var o=t.getPaintRect();(!r||o&&o.intersect(r))&&(Object(l["a"])(s,t,n,a),t.setPrevPaintRect(o))}else Object(l["a"])(s,t,n,a)},t.prototype.getLayer=function(t,e){this._singleCanvas&&!this._needsManuallyCompositing&&(t=g);var i=this._layers[t];return i||(i=new u("zr_"+t,this,this.dpr),i.zlevel=t,i.__builtin__=!0,this._layerConfig[t]?n["I"](i,this._layerConfig[t],!0):this._layerConfig[t-w]&&n["I"](i,this._layerConfig[t-w],!0),e&&(i.virtual=e),this.insertLayer(t,i),i.initContext()),i},t.prototype.insertLayer=function(t,e){var i=this._layers,r=this._zlevelList,n=r.length,a=this._domRoot,s=null,o=-1;if(!i[t]&&x(e)){if(n>0&&t>r[0]){for(o=0;o<n-1;o++)if(r[o]<t&&r[o+1]>t)break;s=i[r[o]]}if(r.splice(o+1,0,t),i[t]=e,!e.virtual)if(s){var l=s.dom;l.nextSibling?a.insertBefore(e.dom,l.nextSibling):a.appendChild(e.dom)}else a.firstChild?a.insertBefore(e.dom,a.firstChild):a.appendChild(e.dom);e.__painter=this}},t.prototype.eachLayer=function(t,e){for(var i=this._zlevelList,r=0;r<i.length;r++){var n=i[r];t.call(e,this._layers[n],n)}},t.prototype.eachBuiltinLayer=function(t,e){for(var i=this._zlevelList,r=0;r<i.length;r++){var n=i[r],a=this._layers[n];a.__builtin__&&t.call(e,a,n)}},t.prototype.eachOtherLayer=function(t,e){for(var i=this._zlevelList,r=0;r<i.length;r++){var n=i[r],a=this._layers[n];a.__builtin__||t.call(e,a,n)}},t.prototype.getLayers=function(){return this._layers},t.prototype._updateLayerStatus=function(t){function e(t){o&&(o.__endIndex!==t&&(o.__dirty=!0),o.__endIndex=t)}if(this.eachBuiltinLayer((function(t,e){t.__dirty=t.__used=!1})),this._singleCanvas)for(var i=1;i<t.length;i++){var r=t[i];if(r.zlevel!==t[i-1].zlevel||r.incremental){this._needsManuallyCompositing=!0;break}}var a,s,o=null,l=0;for(s=0;s<t.length;s++){r=t[s];var h=r.zlevel,c=void 0;a!==h&&(a=h,l=0),r.incremental?(c=this.getLayer(h+b,this._needsManuallyCompositing),c.incremental=!0,l=1):c=this.getLayer(h+(l>0?w:0),this._needsManuallyCompositing),c.__builtin__||n["G"]("ZLevel "+h+" has been used by unkown layer "+c.id),c!==o&&(c.__used=!0,c.__startIndex!==s&&(c.__dirty=!0),c.__startIndex=s,c.incremental?c.__drawIndex=-1:c.__drawIndex=s,e(s),o=c),r.__dirty&d["a"]&&!r.__inHover&&(c.__dirty=!0,c.incremental&&c.__drawIndex<0&&(c.__drawIndex=s))}e(s),this.eachBuiltinLayer((function(t,e){!t.__used&&t.getElementCount()>0&&(t.__dirty=!0,t.__startIndex=t.__endIndex=t.__drawIndex=0),t.__dirty&&t.__drawIndex<0&&(t.__drawIndex=t.__startIndex)}))},t.prototype.clear=function(){return this.eachBuiltinLayer(this._clearLayer),this},t.prototype._clearLayer=function(t){t.clear()},t.prototype.setBackgroundColor=function(t){this._backgroundColor=t,n["k"](this._layers,(function(t){t.setUnpainted()}))},t.prototype.configLayer=function(t,e){if(e){var i=this._layerConfig;i[t]?n["I"](i[t],e,!0):i[t]=e;for(var r=0;r<this._zlevelList.length;r++){var a=this._zlevelList[r];if(a===t||a===t+w){var s=this._layers[a];n["I"](s,i[t],!0)}}}},t.prototype.delLayer=function(t){var e=this._layers,i=this._zlevelList,r=e[t];r&&(r.dom.parentNode.removeChild(r.dom),delete e[t],i.splice(n["r"](i,t),1))},t.prototype.resize=function(t,e){if(this._domRoot.style){var i=this._domRoot;i.style.display="none";var r=this._opts,n=this.root;if(null!=t&&(r.width=t),null!=e&&(r.height=e),t=Object(o["b"])(n,0,r),e=Object(o["b"])(n,1,r),i.style.display="",this._width!==t||e!==this._height){for(var a in i.style.width=t+"px",i.style.height=e+"px",this._layers)this._layers.hasOwnProperty(a)&&this._layers[a].resize(t,e);this.refresh(!0)}this._width=t,this._height=e}else{if(null==t||null==e)return;this._width=t,this._height=e,this.getLayer(g).resize(t,e)}return this},t.prototype.clearLayer=function(t){var e=this._layers[t];e&&e.clear()},t.prototype.dispose=function(){this.root.innerHTML="",this.root=this.storage=this._domRoot=this._layers=null},t.prototype.getRenderedCanvas=function(t){if(t=t||{},this._singleCanvas&&!this._compositeManually)return this._layers[g].dom;var e=new u("image",this,t.pixelRatio||this.dpr);e.initContext(),e.clear(!1,t.backgroundColor||this._backgroundColor);var i=e.ctx;if(t.pixelRatio<=this.dpr){this.refresh();var r=e.dom.width,n=e.dom.height;this.eachLayer((function(t){t.__builtin__?i.drawImage(t.dom,0,0,r,n):t.renderToCanvas&&(i.save(),t.renderToCanvas(i),i.restore())}))}else for(var a={inHover:!1,viewWidth:this._width,viewHeight:this._height},s=this.storage.getDisplayList(!0),o=0,h=s.length;o<h;o++){var d=s[o];Object(l["a"])(i,d,a,o===h-1)}return e.dom},t.prototype.getWidth=function(){return this._width},t.prototype.getHeight=function(){return this._height},t}();e["a"]=L},3437:function(t,e,i){"use strict";function r(t){return isFinite(t)}function n(t,e,i){var n=null==e.x?0:e.x,a=null==e.x2?1:e.x2,s=null==e.y?0:e.y,o=null==e.y2?0:e.y2;e.global||(n=n*i.width+i.x,a=a*i.width+i.x,s=s*i.height+i.y,o=o*i.height+i.y),n=r(n)?n:0,a=r(a)?a:1,s=r(s)?s:0,o=r(o)?o:0;var l=t.createLinearGradient(n,s,a,o);return l}function a(t,e,i){var n=i.width,a=i.height,s=Math.min(n,a),o=null==e.x?.5:e.x,l=null==e.y?.5:e.y,h=null==e.r?.5:e.r;e.global||(o=o*n+i.x,l=l*a+i.y,h*=s),o=r(o)?o:.5,l=r(l)?l:.5,h=h>=0&&r(h)?h:.5;var d=t.createRadialGradient(o,l,0,o,l,h);return d}function s(t,e,i){for(var r="radial"===e.type?a(t,e,i):n(t,e,i),s=e.colorStops,o=0;o<s.length;o++)r.addColorStop(s[o].offset,s[o].color);return r}function o(t,e){if(t===e||!t&&!e)return!1;if(!t||!e||t.length!==e.length)return!0;for(var i=0;i<t.length;i++)if(t[i]!==e[i])return!0;return!1}function l(t){return parseInt(t,10)}function h(t,e,i){var r=["width","height"][e],n=["clientWidth","clientHeight"][e],a=["paddingLeft","paddingTop"][e],s=["paddingRight","paddingBottom"][e];if(null!=i[r]&&"auto"!==i[r])return parseFloat(i[r]);var o=document.defaultView.getComputedStyle(t);return(t[n]||l(o[r])||l(t.style[r]))-(l(o[a])||0)-(l(o[s])||0)|0}i.d(e,"a",(function(){return s})),i.d(e,"c",(function(){return o})),i.d(e,"b",(function(){return h}))},5210:function(t,e,i){"use strict";i.d(e,"c",(function(){return b})),i.d(e,"b",(function(){return W})),i.d(e,"a",(function(){return M}));var r=i("19eb"),n=i("20c8"),a=i("5e76"),s=i("3437"),o=i("cbe5"),l=i("0da8"),h=i("dd4f"),d=i("6d8b"),c=i("8d1d"),_=i("4bc4"),f=i("726e"),u=new n["a"](!0);function p(t){var e=t.stroke;return!(null==e||"none"===e||!(t.lineWidth>0))}function v(t){return"string"===typeof t&&"none"!==t}function y(t){var e=t.fill;return null!=e&&"none"!==e}function g(t,e){if(null!=e.fillOpacity&&1!==e.fillOpacity){var i=t.globalAlpha;t.globalAlpha=e.fillOpacity*e.opacity,t.fill(),t.globalAlpha=i}else t.fill()}function w(t,e){if(null!=e.strokeOpacity&&1!==e.strokeOpacity){var i=t.globalAlpha;t.globalAlpha=e.strokeOpacity*e.opacity,t.stroke(),t.globalAlpha=i}else t.stroke()}function b(t,e,i){var r=Object(a["a"])(e.image,e.__image,i);if(Object(a["c"])(r)){var n=t.createPattern(r,e.repeat||"repeat");if("function"===typeof DOMMatrix&&n&&n.setTransform){var s=new DOMMatrix;s.translateSelf(e.x||0,e.y||0),s.rotateSelf(0,0,(e.rotation||0)*d["a"]),s.scaleSelf(e.scaleX||1,e.scaleY||1),n.setTransform(s)}return n}}function x(t,e,i,r){var n,a=p(i),o=y(i),l=i.strokePercent,h=l<1,d=!e.path;e.silent&&!h||!d||e.createPathProxy();var f=e.path||u,v=e.__dirty;if(!r){var x=i.fill,m=i.stroke,L=o&&!!x.colorStops,C=a&&!!m.colorStops,k=o&&!!x.image,I=a&&!!m.image,B=void 0,R=void 0,P=void 0,O=void 0,S=void 0;(L||C)&&(S=e.getBoundingRect()),L&&(B=v?Object(s["a"])(t,x,S):e.__canvasFillGradient,e.__canvasFillGradient=B),C&&(R=v?Object(s["a"])(t,m,S):e.__canvasStrokeGradient,e.__canvasStrokeGradient=R),k&&(P=v||!e.__canvasFillPattern?b(t,x,e):e.__canvasFillPattern,e.__canvasFillPattern=P),I&&(O=v||!e.__canvasStrokePattern?b(t,m,e):e.__canvasStrokePattern,e.__canvasStrokePattern=P),L?t.fillStyle=B:k&&(P?t.fillStyle=P:o=!1),C?t.strokeStyle=R:I&&(O?t.strokeStyle=O:a=!1)}var D,H,T=e.getGlobalScale();f.setScale(T[0],T[1],e.segmentIgnoreThreshold),t.setLineDash&&i.lineDash&&(n=Object(c["a"])(e),D=n[0],H=n[1]);var z=!0;(d||v&_["b"])&&(f.setDPR(t.dpr),h?f.setContext(null):(f.setContext(t),z=!1),f.reset(),e.buildPath(f,e.shape,r),f.toStatic(),e.pathUpdated()),z&&f.rebuildPath(t,h?l:1),D&&(t.setLineDash(D),t.lineDashOffset=H),r||(i.strokeFirst?(a&&w(t,i),o&&g(t,i)):(o&&g(t,i),a&&w(t,i))),D&&t.setLineDash([])}function m(t,e,i){var r=e.__image=Object(a["a"])(i.image,e.__image,e,e.onload);if(r&&Object(a["c"])(r)){var n=i.x||0,s=i.y||0,o=e.getWidth(),l=e.getHeight(),h=r.width/r.height;if(null==o&&null!=l?o=l*h:null==l&&null!=o?l=o/h:null==o&&null==l&&(o=r.width,l=r.height),i.sWidth&&i.sHeight){var d=i.sx||0,c=i.sy||0;t.drawImage(r,d,c,i.sWidth,i.sHeight,n,s,o,l)}else if(i.sx&&i.sy){d=i.sx,c=i.sy;var _=o-d,f=l-c;t.drawImage(r,d,c,_,f,n,s,o,l)}else t.drawImage(r,n,s,o,l)}}function L(t,e,i){var r,n=i.text;if(null!=n&&(n+=""),n){t.font=i.font||f["a"],t.textAlign=i.textAlign,t.textBaseline=i.textBaseline;var a=void 0,s=void 0;t.setLineDash&&i.lineDash&&(r=Object(c["a"])(e),a=r[0],s=r[1]),a&&(t.setLineDash(a),t.lineDashOffset=s),i.strokeFirst?(p(i)&&t.strokeText(n,i.x,i.y),y(i)&&t.fillText(n,i.x,i.y)):(y(i)&&t.fillText(n,i.x,i.y),p(i)&&t.strokeText(n,i.x,i.y)),a&&t.setLineDash([])}}var C=["shadowBlur","shadowOffsetX","shadowOffsetY"],k=[["lineCap","butt"],["lineJoin","miter"],["miterLimit",10]];function I(t,e,i,n,a){var s=!1;if(!n&&(i=i||{},e===i))return!1;if(n||e.opacity!==i.opacity){A(t,a),s=!0;var o=Math.max(Math.min(e.opacity,1),0);t.globalAlpha=isNaN(o)?r["b"].opacity:o}(n||e.blend!==i.blend)&&(s||(A(t,a),s=!0),t.globalCompositeOperation=e.blend||r["b"].blend);for(var l=0;l<C.length;l++){var h=C[l];(n||e[h]!==i[h])&&(s||(A(t,a),s=!0),t[h]=t.dpr*(e[h]||0))}return(n||e.shadowColor!==i.shadowColor)&&(s||(A(t,a),s=!0),t.shadowColor=e.shadowColor||r["b"].shadowColor),s}function B(t,e,i,r,n){var a=E(e,n.inHover),s=r?null:i&&E(i,n.inHover)||{};if(a===s)return!1;var o=I(t,a,s,r,n);if((r||a.fill!==s.fill)&&(o||(A(t,n),o=!0),v(a.fill)&&(t.fillStyle=a.fill)),(r||a.stroke!==s.stroke)&&(o||(A(t,n),o=!0),v(a.stroke)&&(t.strokeStyle=a.stroke)),(r||a.opacity!==s.opacity)&&(o||(A(t,n),o=!0),t.globalAlpha=null==a.opacity?1:a.opacity),e.hasStroke()){var l=a.lineWidth,h=l/(a.strokeNoScale&&e.getLineScale?e.getLineScale():1);t.lineWidth!==h&&(o||(A(t,n),o=!0),t.lineWidth=h)}for(var d=0;d<k.length;d++){var c=k[d],_=c[0];(r||a[_]!==s[_])&&(o||(A(t,n),o=!0),t[_]=a[_]||c[1])}return o}function R(t,e,i,r,n){return I(t,E(e,n.inHover),i&&E(i,n.inHover),r,n)}function P(t,e){var i=e.transform,r=t.dpr||1;i?t.setTransform(r*i[0],r*i[1],r*i[2],r*i[3],r*i[4],r*i[5]):t.setTransform(r,0,0,r,0,0)}function O(t,e,i){for(var r=!1,n=0;n<t.length;n++){var a=t[n];r=r||a.isZeroArea(),P(e,a),e.beginPath(),a.buildPath(e,a.shape),e.clip()}i.allClipped=r}function S(t,e){return t&&e?t[0]!==e[0]||t[1]!==e[1]||t[2]!==e[2]||t[3]!==e[3]||t[4]!==e[4]||t[5]!==e[5]:!(!t&&!e)}var D=1,H=2,T=3,z=4;function j(t){var e=y(t),i=p(t);return!(t.lineDash||!(+e^+i)||e&&"string"!==typeof t.fill||i&&"string"!==typeof t.stroke||t.strokePercent<1||t.strokeOpacity<1||t.fillOpacity<1)}function A(t,e){e.batchFill&&t.fill(),e.batchStroke&&t.stroke(),e.batchFill="",e.batchStroke=""}function E(t,e){return e&&t.__hoverStyle||t.style}function W(t,e){M(t,e,{inHover:!1,viewWidth:0,viewHeight:0},!0)}function M(t,e,i,r){var n=e.transform;if(!e.shouldBePainted(i.viewWidth,i.viewHeight,!1,!1))return e.__dirty&=~_["a"],void(e.__isRendered=!1);var a=e.__clipPaths,d=i.prevElClipPaths,c=!1,f=!1;if(d&&!Object(s["c"])(a,d)||(d&&d.length&&(A(t,i),t.restore(),f=c=!0,i.prevElClipPaths=null,i.allClipped=!1,i.prevEl=null),a&&a.length&&(A(t,i),t.save(),O(a,t,i),c=!0),i.prevElClipPaths=a),i.allClipped)e.__isRendered=!1;else{e.beforeBrush&&e.beforeBrush(),e.innerBeforeBrush();var u=i.prevEl;u||(f=c=!0);var p=e instanceof o["b"]&&e.autoBatch&&j(e.style);c||S(n,u.transform)?(A(t,i),P(t,e)):p||A(t,i);var v=E(e,i.inHover);e instanceof o["b"]?(i.lastDrawType!==D&&(f=!0,i.lastDrawType=D),B(t,e,u,f,i),p&&(i.batchFill||i.batchStroke)||t.beginPath(),x(t,e,v,p),p&&(i.batchFill=v.fill||"",i.batchStroke=v.stroke||"")):e instanceof h["a"]?(i.lastDrawType!==T&&(f=!0,i.lastDrawType=T),B(t,e,u,f,i),L(t,e,v)):e instanceof l["a"]?(i.lastDrawType!==H&&(f=!0,i.lastDrawType=H),R(t,e,u,f,i),m(t,e,v)):e.getTemporalDisplayables&&(i.lastDrawType!==z&&(f=!0,i.lastDrawType=z),F(t,e,i)),p&&r&&A(t,i),e.innerAfterBrush(),e.afterBrush&&e.afterBrush(),i.prevEl=e,e.__dirty=0,e.__isRendered=!0}}function F(t,e,i){var r=e.getDisplayables(),n=e.getTemporalDisplayables();t.save();var a,s,o={prevElClipPaths:null,prevEl:null,allClipped:!1,viewWidth:i.viewWidth,viewHeight:i.viewHeight,inHover:i.inHover};for(a=e.getCursor(),s=r.length;a<s;a++){var l=r[a];l.beforeBrush&&l.beforeBrush(),l.innerBeforeBrush(),M(t,l,o,a===s-1),l.innerAfterBrush(),l.afterBrush&&l.afterBrush(),o.prevEl=l}for(var h=0,d=n.length;h<d;h++){l=n[h];l.beforeBrush&&l.beforeBrush(),l.innerBeforeBrush(),M(t,l,o,h===d-1),l.innerAfterBrush(),l.afterBrush&&l.afterBrush(),o.prevEl=l}e.clearTemporalDisplayables(),e.notClear=!0,t.restore()}},"8d1d":function(t,e,i){"use strict";i.d(e,"a",(function(){return a}));var r=i("6d8b");function n(t,e){return t&&"solid"!==t&&e>0?"dashed"===t?[4*e,2*e]:"dotted"===t?[e]:Object(r["z"])(t)?[t]:Object(r["t"])(t)?t:null:null}function a(t){var e=t.style,i=e.lineDash&&e.lineWidth>0&&n(e.lineDash,e.lineWidth),a=e.lineDashOffset;if(i){var s=e.strokeNoScale&&t.getLineScale?t.getLineScale():1;s&&1!==s&&(i=Object(r["H"])(i,(function(t){return t/s})),a/=s)}return[i,a]}}}]);