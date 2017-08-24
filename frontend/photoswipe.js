'use strict'

var PhotoSwipe = require('photoswipe/dist/photoswipe')
var PhotoSwipeUI_Default = require('photoswipe/dist/photoswipe-ui-default')

module.exports = {
    init: init
}

function init(thumbnails) {
    var items = collectItems(thumbnails)
    var pswp = document.querySelector('.pswp')
    for (var i = 0; i < thumbnails.length; i++) {
        bind(thumbnails[i], i, items, pswp)
    }
}

function collectItems(thumbnails) {
    return Array.prototype.map.call(thumbnails, function(thumbnail) {
        var img = thumbnail.firstElementChild
        return {
            src: thumbnail.getAttribute('href'),
            msrc: img.getAttribute('src'),
            title: img.dataset.description,
            w: img.dataset.fullWidth,
            h: img.dataset.fullHeight
        }
    })
}

function bind(thumbnail, index, items, pswp) {
    thumbnail.addEventListener('click', function (event) {
        event.preventDefault()
        var options = {
            index: index,
            bgOpacity: 0.85,
            getThumbBoundsFn: function (index) {
                return {
                    x: thumbnail.offsetLeft,
                    y: thumbnail.offsetTop,
                    w: thumbnail.offsetWidth
                }
            }
        };
        new PhotoSwipe(pswp, PhotoSwipeUI_Default, items, options).init()
    })
}
