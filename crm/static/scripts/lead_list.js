document.addEventListener("DOMContentLoaded", function() {

    // ==========================================
    // 1. FORM FIELD CYBER STYLING INITIALIZER
    // ==========================================
    const formElements = document.querySelectorAll(
        '.django-injected-form-wrapper p input, .django-injected-form-wrapper p select, .django-injected-form-wrapper p textarea'
    );

    formElements.forEach(element => {
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.classList.add('premium-cyber-input-element');
        }
    });


    // ==========================================
    // 2. FIELD INPUT INTERACTIVE VALIDATORS
    // ==========================================
    function registerAsyncValidator(elementId, endpointUrl, trackingParam, errorMsg) {
        const fieldInput = document.getElementById(elementId);
        if (!fieldInput) return;

        fieldInput.addEventListener('input', function() { this.setCustomValidity(''); });
        fieldInput.addEventListener('blur', function() {
            if (this.value.trim() === '') return;
            if (!this.checkValidity()) { this.reportValidity(); return; }

            fetch(`${endpointUrl}?${trackingParam}=${encodeURIComponent(this.value)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) { this.setCustomValidity(errorMsg); } 
                    else { this.setCustomValidity(''); }
                    this.reportValidity();
                })
                .catch(err => console.error(`Validator exception logic loop structural break:`, err));
        });
    }

    registerAsyncValidator('personname', '/check-personname/', 'personname', 'Lead with this name already exists. Add another name.');
    registerAsyncValidator('contactno', '/check-contactno/', 'contactno', 'Lead with this contact number already exists.');
    registerAsyncValidator('email', '/check-email/', 'email', 'Lead with this email already exists.');


    // ==========================================
    // 3. INTERCEPT INLINE EDIT CLICKS (STATE SWITCH)
    // ==========================================
    const leadForm = document.getElementById('add-product-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const submitFormBtn = leadForm?.querySelector('.submit-core-action-btn');
    const formTitleBlock = document.querySelector('.form-title-block');

    // Select elements based on Django form outputs field target rules
    const pName = document.querySelector('[name="personname"]');
    const cName = document.querySelector('[name="companyname"]');
    const cNo = document.querySelector('[name="contactno"]');
    const pId = document.querySelector('[name="productid"]');
    const rId = document.querySelector('[name="regionid"]');
    const sId = document.querySelector('[name="statusid"]');
    const lsId = document.querySelector('[name="leadsourceid"]');

    document.addEventListener('click', function(e) {
        const editTrigger = e.target.closest('.single-edit-btn');
        if (!editTrigger) return;

        const id = editTrigger.getAttribute('data-id');

        // Shift state management to edit processing rules
        leadForm.setAttribute('data-mode', 'edit');
        leadForm.setAttribute('action', `/leads/edit/${id}/`); // Rewrites dynamic fetch path mapping target
        
        if (formTitleBlock) {
            formTitleBlock.innerHTML = `
                <h3><i class="bi bi-pencil-square color-edit"></i> Modify Lead Profile</h3>
                <p>Altering existing pipeline tracking row indices data properties.</p>
            `;
        }
        if (submitFormBtn) {
            submitFormBtn.textContent = "Save Profile Changes";
            submitFormBtn.classList.add('modify-theme-btn');
        }
        if (cancelEditBtn) cancelEditBtn.style.display = 'block';

        // Map string token elements fields directly from metadata data fields properties attributes
        if (pName) pName.value = editTrigger.getAttribute('data-personname');
        if (cName) cName.value = editTrigger.getAttribute('data-companyname');
        if (cNo) cNo.value = editTrigger.getAttribute('data-contactno');
        if (pId) pId.value = editTrigger.getAttribute('data-productid');
        if (rId) rId.value = editTrigger.getAttribute('data-regionid');
        if (sId) sId.value = editTrigger.getAttribute('data-statusid');
        if (lsId) lsId.value = editTrigger.getAttribute('data-leadsourceid');

        leadForm.scrollIntoView({ behavior: 'smooth' });
    });

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function(e) { e.preventDefault(); resetLeadFormState(); });
    }

    function resetLeadFormState() {
        if (!leadForm) return;
        leadForm.setAttribute('data-mode', 'add');
        leadForm.setAttribute('action', '/leads/add/');
        if (formTitleBlock) {
            formTitleBlock.innerHTML = `
                <h3><i class="bi bi-plus-circle-fill color-add"></i> Intake Lead Account</h3>
                <p>Append a new business channel contact into core matrix.</p>
            `;
        }
        if (submitFormBtn) {
            submitFormBtn.textContent = "Append Lead Record";
            submitFormBtn.classList.remove('modify-theme-btn');
        }
        cancelEditBtn.style.display = 'none';
        leadForm.reset();
    }


    // ==========================================
    // 4. TRANSACTION ENGINE: ASYNC ADD & UPDATE
    // ==========================================
    const tableBody = document.querySelector('table tbody');

    if (leadForm) {
        leadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const targetUrl = this.getAttribute('action');
            const mode = this.getAttribute('data-mode');

            fetch(targetUrl, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (mode === 'edit') {
                        // Live Update specific row columns parameters text contents nodes
                        const targetRow = document.querySelector(`tr[data-row-id="${data.lead.id}"]`);
                        if (targetRow) {
                            targetRow.querySelector('.lead-avatar').textContent = data.lead.name.slice(0, 1);
                            targetRow.querySelector('.lead-name-txt').textContent = data.lead.name;
                            targetRow.querySelector('.company-tag').textContent = data.lead.company;
                            targetRow.querySelector('.chrono-stamp').innerHTML = `<i class="bi bi-telephone text-slate"></i> ${data.lead.phone}`;
                            targetRow.querySelector('.fw-semibold').textContent = data.lead.product;
                            targetRow.querySelector('.region-tag').innerHTML = `<i class="bi bi-geo-alt"></i> ${data.lead.region}`;
                            targetRow.querySelector('.status-workflow').innerHTML = `<i class="bi bi-lightning-charge-fill"></i> ${data.lead.status}`;
                            targetRow.querySelector('.user-meta-txt').textContent = data.lead.source;
                            
                            // Sync data back onto attributes for subsequent selections fields edits
                            const editBtn = targetRow.querySelector('.single-edit-btn');
                            if (editBtn) {
                                editBtn.setAttribute('data-personname', data.lead.name);
                                editBtn.setAttribute('data-companyname', data.lead.company);
                                editBtn.setAttribute('data-contactno', data.lead.phone);
                                editBtn.setAttribute('data-productid', pId.value);
                                editBtn.setAttribute('data-regionid', rId.value);
                                editBtn.setAttribute('data-statusid', sId.value);
                                editBtn.setAttribute('data-leadsourceid', lsId.value);
                            }

                            targetRow.style.background = 'rgba(99, 102, 241, 0.15)';
                            setTimeout(() => { targetRow.style.transition = 'background 0.5s'; targetRow.style.background = ''; }, 400);
                            resetLeadFormState();
                        }
                    } else {
                        // Append dynamic newly generated matrix track nodes elements straight to bottom bounds index
                        const emptyFallback = document.querySelector('.empty-fallback-state');
                        if (emptyFallback) emptyFallback.closest('tr').remove();

                        const newRow = document.createElement('tr');
                        newRow.setAttribute('data-row-id', data.lead.id);
                        newRow.innerHTML = `
                            <td style="text-align: center;"><input type="checkbox" class="row-select-checkbox" value="${data.lead.id}"></td>
                            <td class="id-token">#${data.lead.id}</td>
                            <td>
                                <div class="lead-identity-cell">
                                    <div class="lead-avatar">${data.lead.name.slice(0, 1)}</div>
                                    <span class="lead-name-txt">${data.lead.name}</span>
                                </div>
                            </td>
                            <td><span class="badge-tag-pill company-tag">${data.lead.company}</span></td>
                            <td class="chrono-stamp"><i class="bi bi-telephone text-slate"></i> ${data.lead.phone}</td>
                            <td><span class="fw-semibold text-white">${data.lead.product}</span></td>
                            <td><span class="badge-tag-pill region-tag"><i class="bi bi-geo-alt"></i> ${data.lead.region}</span></td>
                            <td><span class="indicator-badge status-workflow"><i class="bi bi-lightning-charge-fill"></i> ${data.lead.status}</span></td>
                            <td class="user-meta-txt">${data.lead.source}</td>
                            <td class="chrono-stamp">${data.lead.date}</td>
                            <td>
                                <div class="action-buttons-group">
                                    <button type="button" class="action-trigger-btn edit-trigger single-edit-btn" 
                                            data-id="${data.lead.id}" data-personname="${data.lead.name}" data-companyname="${data.lead.company}" 
                                            data-contactno="${data.lead.phone}" data-productid="${pId.value}" data-regionid="${rId.value}" 
                                            data-statusid="${sId.value}" data-leadsourceid="${lsId.value}">
                                        <i class="bi bi-pencil-square"></i>
                                    </button>
                                    <button type="button" class="action-trigger-btn delete-trigger single-delete-btn" data-id="${data.lead.id}"><i class="bi bi-trash3-fill"></i></button>
                                </div>
                            </td>
                        `;
                        tableBody.appendChild(newRow);
                        leadForm.reset();
                    }
                } else { alert('Operation Failed: ' + data.error); }
            })
            .catch(err => console.error('Form processing pipeline broke:', err));
        });
    }


    // ==========================================
    // 5. TRANSACTION ENGINE: SINGLE ASYNC TRASH DELETE
    // ==========================================
    document.addEventListener('click', function(e) {
        const trashBtn = e.target.closest('.single-delete-btn');
        if (!trashBtn) return;
        const leadId = trashBtn.getAttribute('data-id');
        if (!confirm("Are you certain you want to permanently drop this contact out of the pipeline trace metrics?")) return;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/leads/delete/${leadId}/`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const targetRow = document.querySelector(`tr[data-row-id="${leadId}"]`);
                if (targetRow) {
                    targetRow.style.transition = 'all 0.3s ease'; targetRow.style.opacity = '0';
                    setTimeout(() => targetRow.remove(), 300);
                }
            }
        });
    });


    // ==========================================
    // 6. MULTI-SELECT LEDGER BAR MATRIX CONTROL HOOKS
    // ==========================================
    const masterCheckbox = document.getElementById('master-select-checkbox');
    const rowCheckboxes = document.getElementsByClassName('row-select-checkbox');
    const bulkActionBar = document.getElementById('bulk-action-bar');
    const selectedCountTxt = document.getElementById('selected-count-txt');
    const bulkDeleteBtn = document.getElementById('execute-bulk-delete-btn');

    function updateBulkActionBar() {
        const checkedRows = document.querySelectorAll('.row-select-checkbox:checked');
        const selectedCount = checkedRows.length;
        if (selectedCount > 0) {
            selectedCountTxt.textContent = `${selectedCount} Lead${selectedCount > 1 ? 's' : ''} Selected`;
            bulkActionBar.style.display = 'flex';
        } else { bulkActionBar.style.display = 'none'; }
        if (masterCheckbox) masterCheckbox.checked = (selectedCount === rowCheckboxes.length && rowCheckboxes.length > 0);
    }

    if (masterCheckbox) {
        masterCheckbox.addEventListener('change', function() {
            for (let cb of rowCheckboxes) cb.checked = this.checked;
            updateBulkActionBar();
        });
        document.addEventListener('change', (e) => { if (e.target.classList.contains('row-select-checkbox')) updateBulkActionBar(); });
        
        bulkDeleteBtn.addEventListener('click', function() {
            const checkedRows = document.querySelectorAll('.row-select-checkbox:checked');
            const selectedIds = Array.from(checkedRows).map(cb => parseInt(cb.value));
            if (!confirm(`Are you absolutely positive you want to execute a bulk wipe operation on all ${selectedIds.length} targeted tracks concurrently?`)) return;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/leads/bulk-delete/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify({ 'lead_ids': selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    selectedIds.forEach(id => { const r = document.querySelector(`tr[data-row-id="${id}"]`); if (r) r.remove(); });
                    masterCheckbox.checked = false; updateBulkActionBar();
                }
            });
        });
    }

});