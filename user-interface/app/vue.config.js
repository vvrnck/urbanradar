const { GenerateSW } = require("workbox-webpack-plugin");

module.exports = {
    publicPath: process.env.VUE_APP_NODE_ENV === "development" ? "/" : "",
    productionSourceMap: false,
    devServer: {
        disableHostCheck: true
    },
    configureWebpack:{
        plugins: [new GenerateSW()],
        optimization: {
          nodeEnv: 'production',
          minimize: true,
          splitChunks: {
            chunks: 'all',
            minSize: 10000,
            maxSize: 250000,
            cacheGroups: {
              node_vendors: {
                  test: /[\\/]node_modules[\\/]/,
                  chunks: "all",
                  priority: 1
              }
            }
          }
        },
        performance: {
            maxEntrypointSize: 512000,
            maxAssetSize: 512000
        }        
    }
}