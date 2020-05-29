const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require('terser-webpack-plugin');

//development
module.exports = {
    mode: "production",
    devtool: "inline-source-map",
    performance: {
        hints: false
    },
    entry: {
        '/metro_park_production/static/js/pack/main': "./src/main/production_main.js",
    },
    output: {
        path: path.join(__dirname),
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                            plugins: [
                                ['@babel/plugin-proposal-object-rest-spread'],
                                ["component",
                                    {
                                        "libraryName": "element-ui",
                                        "styleLibraryName": "theme-chalk"
                                    }],
                            ]
                        }

                    }

                ],

            },

            {
                test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 10000,
                        name:'[name]-[hash:8].[ext]',
                        publicPath: '/metro_park_base/static/js/pack/',
                        outputPath: './metro_park_base/static/js/pack/'
                    }
                }]
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            publicPath: '../',
                            hmr: process.env.NODE_ENV === 'development',
                        }
                    },
                    'css-loader'
                ],
            },
            {test: /\.handlebars$/, loader: "handlebars-loader"}

        ]
    },
    plugins: [

        new MiniCssExtractPlugin({
            filename: '[name].css'
        }),

    ],

    resolve: {
        extensions: ['.js', '.json', '.vue', '.scss', '.css']
    },

    optimization: {
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    warnings: false,
                    parse: {},
                    compress: {},
                    mangle: {
                        reserved: ['require'],
                    }, // Note `mangle.properties` is `false` by default.
                    output: null,
                    toplevel: false,
                    nameCache: null,
                    ie8: false,
                    keep_fnames: false,

                },
            }),
        ],
        splitChunks: {
            chunks: 'all',
            minSize: 30000,
            maxSize: 0,
            minChunks: 1,
            maxAsyncRequests: 5,
            maxInitialRequests: 3,
            automaticNameDelimiter: '~',
            name: '/metro_park_base/static/js/pack/common',
            cacheGroups: {
                common: {
                    test: /[\\/]node_modules[\\/]/,
                    priority: -10
                },
                default: {
                    minChunks: 2,
                    priority: -20,
                    reuseExistingChunk: true
                }
            }
        }

    },


};