'use strict';

function collectItems($thumbnails) {
    var items = [];
    $thumbnails.each(function() {
        var $img = $(this).children('img').first();
        var item = {
            src: $(this).attr('href'),
            msrc: $img.attr('src'),
            title: $img.data('description'),
            w: $img.data('fullWidth'),
            h: $img.data('fullHeight')
        };
        items.push(item);
    });
    return items;
}

function initPhotoSwipe() {
    var pswp = document.querySelector('.pswp')
    var $thumbnails = $('.thumbnail');
    var items = collectItems($thumbnails);

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

$(function() {
    $('.album').justifiedGallery({
        rowHeight: 150,
        margins: 10,
        border: 15,
        waitThumbnailsLoad: false,
        refreshTime: 500
    })
    initPhotoSwipe()
});
