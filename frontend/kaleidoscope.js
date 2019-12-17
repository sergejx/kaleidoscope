'use strict'

const justifiedLayout = require('justified-layout');
const photoswipe = require('frontend/photoswipe');

const layoutConfig = {
    boxSpacing: 10,
    containerPadding: 15,
    targetRowHeight: 176,
    targetRowHeightTolerance: 0.25
};

function init() {
    const allThumbnails = [];
    const sections = document.querySelectorAll('.album');
    for (const section of sections) {
        const layout = new Layout(section);
        allThumbnails.push(...layout.thumbnails);
    }
    photoswipe.init(allThumbnails);
}

class Layout {
    constructor(section) {
        this.root = section;
        this.thumbnails = section.querySelectorAll('.thumbnail');
        this.imagesInfo = this.collectInfo();
        this.createCaptions();
        this.doLayout();
        window.addEventListener('resize', () => this.doLayout())

    }

    collectInfo() {
        return Array.prototype.map.call(this.thumbnails, function(thumbnail) {
            const img = thumbnail.firstElementChild;
            return {
                width: img.getAttribute('width'),
                height: img.getAttribute('height')
            }
        })
    }

    createCaptions() {
        for (let i = 0; i < this.thumbnails.length; i++) {
            const image = this.thumbnails[i].firstElementChild;
            const text = image.getAttribute('alt');
            if (text !== '') {
                image.insertAdjacentHTML('afterend',
                    '<div class="thumbnail__caption">' + text + '</div>')
            }
        }
    }

    computeLayout(container) {
        layoutConfig.containerWidth = container.offsetWidth;
        const geometry = justifiedLayout(this.imagesInfo, layoutConfig);
        container.style.height = inPx(geometry.containerHeight);
        return geometry;
    }

    setSize(element, box) {
        element.style.width = inPx(box.width);
        element.style.height = inPx(box.height);
    }

    setPosition(element, box, container) {
        element.style.top = inPx(container.offsetTop + box.top);
        element.style.left = inPx(container.offsetLeft + box.left);
    }

    doLayout() {
        const container = this.root;
        let geometry = this.computeLayout(container);
        if (layoutConfig.containerWidth !== container.offsetWidth) {
            geometry = this.computeLayout(container);
        }
        for (var j = 0; j < geometry.boxes.length; j++) {
            var anchor = this.thumbnails[j];
            var image = this.thumbnails[j].firstElementChild;
            var box = geometry.boxes[j];
            this.setPosition(anchor, box, container);
            this.setSize(anchor, box);
            this.setSize(image, box);
            anchor.style.opacity = '1';
        }
    }

}

function inPx(number) {
        return number.toString() + 'px';
    }

document.addEventListener('DOMContentLoaded', init)
