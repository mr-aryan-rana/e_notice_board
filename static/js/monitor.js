let currentNoticeIndex = 0;
let notices = [];
let noticeInterval;

function startNoticeCycle(monitorId, isActive) {
    if (!isActive) {
        showBlockedMonitor();
        return;
    }

    fetchNotices(monitorId);

    // Refresh notices every 1 minute
    setInterval(() => {
        fetchNotices(monitorId);
    }, 60000);
}

function fetchNotices(monitorId) {
    fetch(`/monitor/api/display/${monitorId}`)
        .then(response => {
            if (response.status === 403) {
                // Monitor blocked
                showBlockedMonitor();
                return [];
            }
            return response.json();
        })
        .then(data => {
            notices = data;
            if (!notices || notices.length === 0) {
                showNoNotice();
            } else {
                currentNoticeIndex = 0;
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

    clearTimeout(noticeInterval);
    noticeInterval = setTimeout(() => {
        currentNoticeIndex = (currentNoticeIndex + 1) % notices.length;
        displayNotice(currentNoticeIndex);
    }, notice.display_duration * 1000); // ensure milliseconds
}


function showNoNotice() {
    const container = document.getElementById('notice-container');
    container.innerHTML = `
        <h1>No notices to display</h1>
        <p>Monitor is active but has no assigned notices.</p>
    `;
}


function showBlockedMonitor() {
    const container = document.getElementById('notice-container');
    container.innerHTML = `
        <div class="alert alert-danger">
            <h1>Monitor Blocked</h1>
            <p>This monitor is currently blocked. Notices cannot be displayed.</p>
        </div>
    `;
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
