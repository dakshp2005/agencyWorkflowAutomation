document.addEventListener('DOMContentLoaded', () => {
    const approveBtns = document.querySelectorAll('.btn-approve');
    const rejectBtns = document.querySelectorAll('.btn-reject');

    approveBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const type = btn.dataset.type;
            const id = btn.dataset.id;

            try {
                await apiCall(btn, `/api/approve/${type}/${id}`, 'POST');
                Toast.success(`Approved successfully.`);
                const card = btn.closest('.approval-card');
                if (card) {
                    card.style.opacity = 0.5;
                    setTimeout(() => card.remove(), 300);
                } else {
                    window.location.reload();
                }
            } catch (err) { }
        });
    });

    rejectBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const type = btn.dataset.type;
            const id = btn.dataset.id;

            try {
                await apiCall(btn, `/api/reject/${type}/${id}`, 'POST');
                Toast.info(`Rejected.`);
                const card = btn.closest('.approval-card');
                if (card) {
                    card.style.opacity = 0.5;
                    setTimeout(() => card.remove(), 300);
                } else {
                    window.location.reload();
                }
            } catch (err) { }
        });
    });
});
