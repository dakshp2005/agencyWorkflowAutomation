document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const target = document.getElementById(tab.dataset.target);
            if (target) target.classList.add('active');
        });
    });

    const generateProposalBtn = document.getElementById('btn-generate-proposal');
    if (generateProposalBtn) {
        generateProposalBtn.addEventListener('click', async (e) => {
            const clientId = generateProposalBtn.dataset.client;
            try {
                await apiCall(generateProposalBtn, '/api/documents/generate', 'POST', {
                    client_id: clientId,
                    doc_type: 'proposal'
                });
                Toast.success('Proposal generation started.');
                setTimeout(() => window.location.reload(), 1000);
            } catch (err) { }
        });
    }

    const generateEmailBtn = document.getElementById('btn-generate-email');
    if (generateEmailBtn) {
        generateEmailBtn.addEventListener('click', async (e) => {
            const clientId = generateEmailBtn.dataset.client;
            try {
                await apiCall(generateEmailBtn, '/api/outreach/generate', 'POST', {
                    client_id: clientId,
                    type: 'outreach'
                });
                Toast.success('Email outreach drafted.');
                setTimeout(() => window.location.reload(), 1000);
            } catch (err) { }
        });
    }
});
