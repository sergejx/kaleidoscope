'use strict';

function collectItems($thumbnails) {
    var items = [];
    $thumbnails.each(function() {
        var $img = $(this).children('img').first();
        var item = {
            src: $(this).attr('href'),
            msrc: $img.attr('src'),
            title: $img.attr('title'),
            w: $img.data('fullWidth'),
            h: $img.data('fullHeight')
        };
        items.push(item);
    });
    return items;
}

function initPhotoSwipe() {
    var $pswp = $('<div class="pswp" tabindex="-1" role="dialog" aria-hidden="true"><div class="pswp__bg"></div><div class="pswp__scroll-wrap"><div class="pswp__container"><div class="pswp__item"></div><div class="pswp__item"></div><div class="pswp__item"></div></div><div class="pswp__ui pswp__ui--hidden"><div class="pswp__top-bar"><div class="pswp__counter"></div><button class="pswp__button pswp__button--close" title="Close (Esc)"></button><button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button><button class="pswp__button pswp__button--zoom" title="Zoom in/out"></button><div class="pswp__preloader"><div class="pswp__preloader__icn"><div class="pswp__preloader__cut"><div class="pswp__preloader__donut"></div></div></div></div></div><div class="pswp__share-modal pswp__share-modal--hidden pswp__single-tap"><div class="pswp__share-tooltip"></div></div><button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)"></button><button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)"></button><div class="pswp__caption"><div class="pswp__caption__center"></div></div></div></div></div>');
    $pswp.appendTo("body");
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

        var photoSwipe = new PhotoSwipe($pswp.get(0), PhotoSwipeUI_Default, items, options);
        photoSwipe.init();
    });
}

$(function() {
    $('.album').justifiedGallery({
        rowHeight: 120,
        maxRowHeight: 300,
        margins: 10,
        waitThumbnailsLoad: false,
        rel: 'album'
    }).on('jg.complete', initPhotoSwipe);
});