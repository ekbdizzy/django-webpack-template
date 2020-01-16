const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: './main/static/js/index.js',
    output: {
        // publicPath: "http://127.0.0.1:8080"
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {sourceMap: true}
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            config: {
                                path: './postcss.config.js'
                            }
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {sourceMap: true}
                    }
                ]
            },
        ],
    },
    devServer: {
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
    },
    watch: true,
    watchOptions: {
        ignored: [
            '/node_modules/'
        ]
    },

    plugins: [
        new CopyWebpackPlugin([
            {from: `dist/admin`, to: `../admin`},
        ])
    ]


};