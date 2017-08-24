'use strict'

var justifiedLayout = require('justified-layout')
var photoswipe = require('frontend/photoswipe')

var layoutConfig = {
    boxSpacing: 10,
    containerPadding: 15,
    targetRowHeight: 150,
    targetRowHeightTolerance: 0.25
}

var thumbnails = []
var imagesInfo = []


function init() {
    thumbnails = document.querySelectorAll('.thumbnail')
    imagesInfo = collectInfo()
    createCaptions()
    doLayout()
    window.addEventListener('resize', doLayout)
    photoswipe.init(thumbnails)
}

function collectInfo() {
    return Array.prototype.map.call(thumbnails, function(thumbnail) {
        var img = thumbnail.firstElementChild
        return {
            width: img.getAttribute('width'),
            height: img.getAttribute('height')
        }
    })
}

function createCaptions() {
    for (var i = 0; i < thumbnails.length; i++) {
        var image = thumbnails[i].firstElementChild
        var text = image.getAttribute('alt')
        if (text != '') {
            image.insertAdjacentHTML('afterend',
                '<div class="thumbnail__caption">' + text + '</div>')
        }
    }
}

function computeLayout(container) {
    layoutConfig.containerWidth = container.offsetWidth
    var geometry = justifiedLayout(imagesInfo, layoutConfig)
    container.style.height = inPx(geometry.containerHeight)
    return geometry
}

function setSize(element, box) {
    element.style.width = inPx(box.width)
    element.style.height = inPx(box.height)
}

function setPosition(element, box, container) {
    element.style.top = inPx(container.offsetTop + box.top)
    element.style.left = inPx(container.offsetLeft + box.left)
}

function doLayout() {
    var container = document.querySelector('.album')
    var geometry = computeLayout(container)
    if (layoutConfig.containerWidth !== container.offsetWidth) {
        geometry = computeLayout(container)
    }
    for (var i = 0; i < geometry.boxes.length; i++) {
        var anchor = thumbnails[i]
        var image = thumbnails[i].firstElementChild
        var box = geometry.boxes[i]
        setPosition(anchor, box, container)
        setSize(anchor, box)
        setSize(image, box)
        anchor.style.opacity = '1'
    }
}

function inPx(number) {
    return number.toString() + 'px'
}

document.addEventListener('DOMContentLoaded', init)
