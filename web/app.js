document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    const complaintInput = document.getElementById('complaint-input');
    const triageBoard = document.getElementById('triage-board');
    const timeline = document.getElementById('timeline');
    const resultCard = document.getElementById('result-card');
    const finalDecision = document.getElementById('final-decision');

    submitBtn.addEventListener('click', async () => {
        const complaint = complaintInput.value.trim();
        if(!complaint) return;

        // Reset UI
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Processing...</span><span class="loader"></span>';
        timeline.innerHTML = '';
        resultCard.style.display = 'none';
        triageBoard.style.display = 'block';

        try {
            const response = await fetch('/api/triage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ complaint })
            });

            const data = await response.json();
            
            if(data.status === 'success') {
                renderTrace(data.result.trace, data.result.final_decision);
            } else {
                alert("Error from server: " + data.detail);
            }
        } catch (error) {
            console.error(error);
            alert("Network error occurred.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<span>Initialize Triage</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
        }
    });

    async function renderTrace(traceArr, finalStr) {
        for(let i=0; i<traceArr.length; i++) {
            const step = traceArr[i];
            
            // Skip the final trace since we render it big
            if(step.action === "Final Routing Decision") continue;

            const node = document.createElement('div');
            node.className = 'trace-node';
            
            // Emoji mapping based on agent
            let icon = '⚙️';
            if(step.agent === 'SymptomAgent') icon = '🔍';
            if(step.agent === 'TriageAgent') icon = '📊';

            node.innerHTML = `
                <div class="node-icon">${icon}</div>
                <div class="node-content">
                    <div class="node-header">
                        <span class="node-agent">${step.agent}</span>
                        <span class="node-action">${step.action}</span>
                    </div>
                    <div class="node-data">${JSON.stringify(step.data, null, 2)}</div>
                </div>
            `;
            timeline.appendChild(node);
            
            // Delay for aesthetic cascade effect
            await new Promise(r => setTimeout(r, 600));
        }

        // Show Final Decision
        finalDecision.textContent = finalStr;
        
        // Color code based on emergency text
        resultCard.style.borderColor = 'var(--card-border)';
        resultCard.style.background = 'rgba(0,0,0,0.2)';
        resultCard.querySelector('h4').style.color = '#fff';

        if(finalStr.includes("EMERGENCY")) {
            resultCard.style.borderColor = 'rgba(239, 68, 68, 0.5)';
            resultCard.style.background = 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(0,0,0,0.2))';
            resultCard.querySelector('h4').style.color = 'var(--health-high)';
        } else if (finalStr.includes("URGENT")) {
            resultCard.style.borderColor = 'rgba(245, 158, 11, 0.5)';
            resultCard.style.background = 'linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(0,0,0,0.2))';
            resultCard.querySelector('h4').style.color = 'var(--health-medium)';
        } else {
            resultCard.style.borderColor = 'rgba(16, 185, 129, 0.5)';
            resultCard.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(0,0,0,0.2))';
            resultCard.querySelector('h4').style.color = 'var(--health-low)';
        }

        resultCard.style.display = 'block';
    }
});
