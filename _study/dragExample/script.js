document.addEventListener('DOMContentLoaded', (event) => {
    const items = document.querySelectorAll('#itemList li');
    const dropZone = document.getElementById('droppedList');
    let draggedItem = null;

    items.forEach(item => {
        item.addEventListener('dragstart', function (e) {
            draggedItem = this;
            setTimeout(() => {
                this.style.display = 'none';
            }, 0);
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', this.innerHTML);
        });

        item.addEventListener('dragend', function (e) {
            setTimeout(() => {
                this.style.display = 'block';
                draggedItem = null;
            }, 0);
        });

        item.addEventListener('dragover', function (e) {
            e.preventDefault();
        });

        item.addEventListener('dragenter', function (e) {
            e.preventDefault();
            this.classList.add('placeholder');
        });

        item.addEventListener('dragleave', function (e) {
            this.classList.remove('placeholder');
        });

        item.addEventListener('drop', function (e) {
            e.stopPropagation();
            if (draggedItem != this) {
                this.parentNode.insertBefore(draggedItem, this.nextSibling);
            }
            this.classList.remove('placeholder');
        });
    });

    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    });

    dropZone.addEventListener('dragenter', function (e) {
        e.preventDefault();
        dropZone.classList.add('highlight'); // Drop zone 강조
    });

    dropZone.addEventListener('dragleave', function (e) {
        dropZone.classList.remove('highlight'); // Drop zone 강조 해제
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropZone.classList.remove('highlight'); // Drop zone 강조 해제
        if (draggedItem) {
            dropZone.appendChild(draggedItem);
            draggedItem.style.display = 'block';
            draggedItem = null;
        }
    });
});
