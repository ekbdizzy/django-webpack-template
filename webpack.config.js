module.exports = {
    mode: 'development',
    entry: './main/static/js/index.js',
    // output: {
    // publicPath: "http://127.0.0.1:8080/"
    // },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'sass-loader']
            },
        ],
    },
    devServer: {
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
    }
};