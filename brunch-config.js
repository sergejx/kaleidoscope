module.exports = {
    paths: {
        public: 'kaleidoscope/assets',
        watched: ['frontend']
    },
    files: {
        javascripts: {joinTo: 'kaleidoscope.js'},
        stylesheets: {joinTo: 'kaleidoscope.css'}
    },
    modules: {
        autoRequire: {
            'kaleidoscope.js': ['frontend/kaleidoscope']
        }
    },
    npm: {
        styles: {
            photoswipe: [
                'dist/photoswipe.css',
                'dist/default-skin/default-skin.css'
            ]
        }
    },
    plugins: {
        copyfilemon: {
            ".": [
                'node_modules/photoswipe/dist/default-skin/default-skin.png',
                'node_modules/photoswipe/dist/default-skin/default-skin.svg',
                'node_modules/photoswipe/dist/default-skin/preloader.gif'
            ]
        }
    }
}
