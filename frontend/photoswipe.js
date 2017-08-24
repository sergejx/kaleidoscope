'use strict'

var PhotoSwipe = require('photoswipe/dist/photoswipe')
var PhotoSwipeUI_Default = require('photoswipe/dist/photoswipe-ui-default')
var $ = require('jquery')

function init(items) {
    var pswp = document.querySelector('.pswp')
    var $thumbnails = $('.thumbnail');

    $thumbnails.on('click', function(event) {
        event.preventDefault();
        var index = $(this).index();
        var options = {
            index: index,
            bgOpacity: 0.85,
            getThumbBoundsFn: function(index) {
                var $thumbnail = $thumbnails.eq(index);
                var offset = $thumbnail.offset();
                return {x: offset.left, y: offset.top, w: $thumbnail.width()};
            }
        };
        new PhotoSwipe(pswp, PhotoSwipeUI_Default, items, options).init();
    });
}

module.exports = {
    init: init
}
