var gulp = require('gulp'),
    concat = require('gulp-concat');

var dest = 'kaleidoscope/assets/vendor/'

/* Copy JS from libraries */
gulp.task('js', function () {
    gulp.src([
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/justifiedGallery/dist/js/jquery.justifiedGallery.min.js',
        'bower_components/photoswipe/dist/photoswipe.min.js',
        'bower_components/photoswipe/dist/photoswipe-ui-default.min.js'])
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest(dest));
});

/* Copy CSS from libraries */
gulp.task('css', function () {
    gulp.src([
        'bower_components/justifiedGallery/dist/css/justifiedGallery.min.css',
        'bower_components/photoswipe/dist/photoswipe.css',
        'bower_components/photoswipe/dist/default-skin/default-skin.css'])
        .pipe(concat('style.css'))
        .pipe(gulp.dest(dest));
});

/* Copy images from libraries */
gulp.task('images', function () {
    gulp.src([
        'bower_components/photoswipe/dist/default-skin/default-skin.png',
        'bower_components/photoswipe/dist/default-skin/default-skin.svg',
        'bower_components/photoswipe/dist/default-skin/preloader.gif'])
        .pipe(gulp.dest(dest));
});

gulp.task('default', ['js', 'css', 'images']);
