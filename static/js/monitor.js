let currentNoticeIndex = 0;
let notices = [];
let noticeInterval;
let fetchInterval;

function startNoticeCycle(monitorId, isActive) {
    if (!isActive) {
        showBlockedMonitor();
        return;
    }

    // Initial fetch
    fetchNotices(monitorId);

    // Refresh notices every 60 seconds
    fetchInterval = setInterval(() => {
        fetchNotices(monitorId);
    }, 60000); // 60,000 ms = 60 sec
}

function fetchNotices(monitorId) {
    fetch(`/monitor/api/display/${monitorId}`)
        .then(response => {
            if (response.status === 403) {
                showBlockedMonitor();
                return [];
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                notices = [];
                showNoNotice();
            } else {
                const currentId = notices[currentNoticeIndex]?.id;
                notices = data;

                // Maintain current notice if still available
                const newIndex = notices.findIndex(n => n.id === currentId);
                currentNoticeIndex = newIndex >= 0 ? newIndex : 0;

                displayNotice(currentNoticeIndex);
            }
        })
        .catch(error => {
            console.error('Error fetching notices:', error);
            showNoNotice();
        });
}

function displayNotice(index) {
    if (notices.length === 0) {
        showNoNotice();
        return;
    }

    const notice = notices[index];
    const container = document.getElementById('notice-container');

    container.innerHTML = '';

    const titleEl = document.createElement('div');
    titleEl.className = `notice-title priority-${getPriorityClass(notice.priority)}`;
    titleEl.textContent = notice.title;

    const contentEl = document.createElement('div');
    contentEl.className = 'notice-content';
    contentEl.innerHTML = notice.content.replace(/\n/g, '<br>');

    container.style.justifyContent = getPositionStyle(notice.position);

    container.appendChild(titleEl);
    container.appendChild(contentEl);

    // Rotate to next notice after display_duration (seconds)
    clearTimeout(noticeInterval);
    noticeInterval = setTimeout(() => {
        currentNoticeIndex = (currentNoticeIndex + 1) % notices.length;
        displayNotice(currentNoticeIndex);
    }, notice.display_duration * 1000); // convert seconds to ms
}

function showNoNotice() {
    const container = document.getElementById('notice-container');
    container.innerHTML = `
        <h1>No notices to display</h1>
        <p>Monitor is active but has no assigned notices.</p>
    `;
    clearTimeout(noticeInterval);
}

function showBlockedMonitor() {
    const container = document.getElementById('notice-container');
    container.innerHTML = `
        <div class="alert alert-danger">
            <h1>Monitor Blocked</h1>
            <p>This monitor is currently blocked. Notices cannot be displayed.</p>
        </div>
    `;
    clearTimeout(noticeInterval);
    clearInterval(fetchInterval);
}

function getPriorityClass(priority) {
    switch(priority) {
        case 3: return 'high';
        case 2: return 'medium';
        default: return 'low';
    }
}

function getPositionStyle(position) {
    switch(position) {
        case 'top': return 'flex-start';
        case 'bottom': return 'flex-end';
        case 'middle': 
        default: return 'center';
    }
}
