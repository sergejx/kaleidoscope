var gulp = require('gulp'),
    concat = require('gulp-concat');

var dest = 'kaleidoscope/assets/vendor/'

/* Copy JS from libraries */
gulp.task('js', function () {
    gulp.src([
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/justifiedGallery/dist/js/jquery.justifiedGallery.min.js',
        'node_modules/photoswipe/dist/photoswipe.min.js',
        'node_modules/photoswipe/dist/photoswipe-ui-default.min.js'])
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest(dest));
});

/* Copy CSS from libraries */
gulp.task('css', function () {
    gulp.src([
        'node_modules/justifiedGallery/dist/css/justifiedGallery.min.css',
        'node_modules/photoswipe/dist/photoswipe.css',
        'node_modules/photoswipe/dist/default-skin/default-skin.css'])
        .pipe(concat('style.css'))
        .pipe(gulp.dest(dest));
});

/* Copy images from libraries */
gulp.task('images', function () {
    gulp.src([
        'node_modules/photoswipe/dist/default-skin/default-skin.png',
        'node_modules/photoswipe/dist/default-skin/default-skin.svg',
        'node_modules/photoswipe/dist/default-skin/preloader.gif'])
        .pipe(gulp.dest(dest));
});

gulp.task('default', ['js', 'css', 'images']);
