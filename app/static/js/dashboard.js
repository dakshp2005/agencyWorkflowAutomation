document.addEventListener('DOMContentLoaded', () => {
    // Pipeline bars visual animation
    const segments = document.querySelectorAll('.pipeline-segment');
    segments.forEach(seg => {
        const targetWidth = seg.dataset.width;
        seg.style.width = '0%';
        setTimeout(() => {
            seg.style.width = targetWidth + '%';
        }, 100);
    });

    // Fetch replies button AJAX
    const fetchRepliesBtn = document.getElementById('btn-fetch-replies');
    if (fetchRepliesBtn) {
        fetchRepliesBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const res = await apiCall(fetchRepliesBtn, '/api/replies/fetch', 'POST');
                Toast.success(`Processed ${res.count} new replies.`);
                setTimeout(() => window.location.reload(), 1500);
            } catch (err) {
                // error handled in apiCall
            }
        });
    }

    // Auto-refresh pending loop
    setInterval(async () => {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();
            const badge = document.getElementById('pending-badge');
            if (badge) {
                badge.textContent = data.pending_approvals;
                badge.style.display = data.pending_approvals > 0 ? 'inline-flex' : 'none';
            }
        } catch (e) {
            console.error("Failed to poll stats", e);
        }
    }, 60000);
});
