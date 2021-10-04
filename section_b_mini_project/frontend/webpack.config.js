const CopyWebpackPlugin = require('copy-webpack-plugin');
const webpack = require('webpack');
const path = require('path');

module.exports = {
    mode: 'development',
    entry: './src/app.js',
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [{
                test: /\.js$/,
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.(svg|gif|html|png|eot|woff|ttf)$/,
                use: [
                    'url-loader',
                ],
            },
        ]
    },
    devServer: {
        contentBase: './dist',
        overlay: true,
        hot: true,
        port: 8081
    },
    plugins: [
        new CopyWebpackPlugin({
            patterns: ['index.html']
        }),
        new webpack.HotModuleReplacementPlugin()
    ]
};