document.addEventListener('DOMContentLoaded', () => {
    const automationBtn = document.getElementById('run-automation-btn');
    const closureBtn = document.getElementById('run-closure-automation-btn');
    const statusContainer = document.getElementById('automation-status');
    const resultDetails = document.getElementById('automation-results');

    if (!automationBtn || !closureBtn) return;

    const runAutomation = async (btn, endpoint, label) => {
        // Estado de Carregamento
        btn.disabled = true;
        const originalHTML = btn.innerHTML;
        const originalClasses = [...btn.classList];
        
        btn.innerHTML = `
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processando...
        `;
        
        // Desativar cores de hover/gradiente durante o loading
        btn.classList.add('bg-slate-400', 'cursor-not-allowed');
        btn.classList.remove('hover:scale-[1.02]', 'hover:from-blue-700', 'hover:from-emerald-700');

        statusContainer.classList.remove('hidden');
        resultDetails.innerHTML = `<p class="text-sm text-slate-500 animate-pulse">Executando fluxo: ${label}...</p>`;

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const result = await response.json();

            if (result.success) {
                const summary = result.summary;
                const closedBadge = summary.closed ? 
                    '<span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">Ciclo Encerrado</span>' : '';
                
                resultDetails.innerHTML = `
                    <div class="bg-emerald-50 border border-emerald-100 rounded-lg p-4">
                        <div class="flex items-start">
                            <div class="flex-shrink-0 mt-0.5">
                                <svg class="h-5 w-5 text-emerald-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            <div class="ml-3">
                                <h3 class="text-sm font-medium text-emerald-800 flex items-center">
                                    Sucesso na Automação! ${closedBadge}
                                </h3>
                                <div class="mt-2 text-sm text-emerald-700">
                                    <ul class="list-disc pl-5 space-y-1">
                                        <li><strong>ID PAT:</strong> ${summary.id_pat}</li>
                                        <li><strong>ID Demanda:</strong> ${summary.id_demanda_pat}</li>
                                        <li><strong>ID Tarefa:</strong> ${summary.id_tarefa}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                throw new Error(result.error || 'Erro desconhecido na automação');
            }
        } catch (error) {
            resultDetails.innerHTML = `
                <div class="bg-rose-50 border border-rose-100 rounded-lg p-4 text-sm text-rose-800">
                    <p class="font-bold">Falha na execução:</p>
                    <p class="mt-1">${error.message}</p>
                </div>
            `;
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
            btn.className = originalClasses.join(' ');
        }
    };

    automationBtn.addEventListener('click', () => 
        runAutomation(automationBtn, '/api/v1/automation/pat-full-cycle', 'Criação -> Atividade')
    );

    closureBtn.addEventListener('click', () => 
        runAutomation(closureBtn, '/api/v1/automation/pat-complete-closure', 'Criação -> Encerramento Total')
    );
});
