// admin.js - Admin Dashboard controller scripts

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dashboard Analytics Chart (via Chart.js)
    const ctx = document.getElementById('dashboardChart');
    if (ctx) {
        fetch('/api/analytics/dashboard-metrics')
            .then(res => res.json())
            .then(data => {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Page Views',
                                data: data.views,
                                borderColor: '#2563eb',
                                backgroundColor: 'rgba(37, 99, 235, 0.05)',
                                fill: true,
                                tension: 0.3
                            },
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top' }
                        },
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            })
            .catch(err => console.error("Error loading metrics: ", err));
    }

    // 2. Mark notifications as read
    const notifBell = document.getElementById('notifBell');
    if (notifBell) {
        notifBell.addEventListener('click', () => {
            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch('/api/notifications/mark-read', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const badge = notifBell.querySelector('.notif-badge');
                    if (badge) badge.remove();
                }
            });
        });
    }

    // 3. Drag and Drop Layout Reordering (HTML5 Drag & Drop)
    const listContainer = document.getElementById('section-list-container');
    if (listContainer) {
        let draggedItem = null;

        listContainer.querySelectorAll('.section-item-card').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                draggedItem = item;
                e.dataTransfer.effectAllowed = 'move';
                setTimeout(() => item.style.opacity = '0.5', 0);
            });

            item.addEventListener('dragend', () => {
                draggedItem.style.opacity = '1';
                draggedItem = null;
                saveSectionOrder();
            });

            item.addEventListener('dragover', (e) => {
                e.preventDefault();
                const bounding = item.getBoundingClientRect();
                const offset = bounding.y + (bounding.height / 2);
                if (e.clientY - offset > 0) {
                    item.after(draggedItem);
                } else {
                    item.before(draggedItem);
                }
            });
        });

        function saveSectionOrder() {
            const order = [];
            listContainer.querySelectorAll('.section-item-card').forEach(item => {
                order.push(parseInt(item.getAttribute('data-id')));
            });

            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch('/api/sections/reorder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                },
                body: JSON.stringify({ order: order })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Show small confirmation popup/toast
                    console.log("Sections reordered!");
                }
            })
            .catch(err => console.error("Reorder failed: ", err));
        }
    }

    // 4. Drag & Drop File Upload Dropzone in Media Manager
    const dropzone = document.getElementById('dropzone');
    if (dropzone) {
        const fileInput = document.getElementById('file-upload-input');
        
        dropzone.addEventListener('click', () => fileInput.click());

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#2563eb';
            dropzone.style.backgroundColor = '#eff6ff';
        });

        ['dragleave', 'dragend'].forEach(type => {
            dropzone.addEventListener(type, () => {
                dropzone.style.borderColor = '#cbd5e1';
                dropzone.style.backgroundColor = 'transparent';
            });
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#cbd5e1';
            dropzone.style.backgroundColor = 'transparent';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileUpload(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                handleFileUpload(fileInput.files[0]);
            }
        });

        function handleFileUpload(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            const albumId = dropzone.getAttribute('data-album-id');
            if (albumId) formData.append('album_id', albumId);

            const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            dropzone.innerHTML = `<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x mb-2 text-primary"></i><p class="m-0">Uploading file...</p></div>`;

            fetch('/api/media/upload', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert("Upload failed: " + data.message);
                    window.location.reload();
                }
            })
            .catch(err => {
                console.error("Upload error: ", err);
                alert("Upload failed.");
                window.location.reload();
            });
        }
    }
});
