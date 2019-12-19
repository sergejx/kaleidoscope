import PhotoSwipe from "photoswipe/dist/photoswipe";
import PhotoSwipeUI_Default from "photoswipe/dist/photoswipe-ui-default";

export default {
    init: init
};

function init(thumbnails) {
    var items = collectItems(thumbnails);
    var pswp = document.querySelector('.pswp');
    for (var i = 0; i < thumbnails.length; i++) {
        bind(thumbnails, i, items, pswp);
    }
}

function collectItems(thumbnails) {
    return Array.prototype.map.call(thumbnails, function(thumbnail) {
        var img = thumbnail.firstElementChild;
        return {
            src: thumbnail.getAttribute('href'),
            msrc: img.getAttribute('src'),
            title: img.dataset.description,
            w: img.dataset.fullWidth,
            h: img.dataset.fullHeight
        }
    });
}

function bind(thumbnails, i, items, pswp) {
    thumbnails[i].addEventListener('click', function (event) {
        event.preventDefault();
        var options = {
            index: i,
            bgOpacity: 0.85,
            getThumbBoundsFn: function (index) {
                return {
                    x: thumbnails[index].offsetLeft,
                    y: thumbnails[index].offsetTop,
                    w: thumbnails[index].offsetWidth
                }
            }
        };
        new PhotoSwipe(pswp, PhotoSwipeUI_Default, items, options).init();
    })
}
