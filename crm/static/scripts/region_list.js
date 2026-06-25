document.addEventListener("DOMContentLoaded", function() {

    // ==========================================
    // 1. FORM FIELD CYBER STYLING INITIALIZER
    // ==========================================
    const formElements = document.querySelectorAll(
        '.django-injected-form-wrapper p input, .django-injected-form-wrapper p select'
    );

    formElements.forEach(element => {
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.classList.add('premium-cyber-input-element');
        }
    });

    // ==========================================
    // 2. REGION NAME BLUR VALIDATION
    // ==========================================
    const regionInput = document.getElementById('regionname');

    if (regionInput) {
        regionInput.addEventListener('input', function () {
            this.setCustomValidity('');
        });

        regionInput.addEventListener('blur', function () {
            if (this.value.trim() === '') return;
            if (!this.checkValidity()) {
                this.reportValidity();
                return;
            }

            fetch(`/check-regionname/?regionname=${encodeURIComponent(this.value)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        this.setCustomValidity('Region with this name already exists.');
                    } else {
                        this.setCustomValidity('');
                    }
                    this.reportValidity();
                });
        });
    }

    // ==========================================
    // 3. INTERCEPT INLINE EDIT CLICKS (STATE SWITCH)
    // ==========================================
    const regionForm = document.getElementById('add-product-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const submitFormBtn = regionForm?.querySelector('.submit-core-action-btn');
    const formTitleBlock = document.querySelector('.form-title-block');
    const inputNameField = document.querySelector('[name="regionname"]');

    document.addEventListener('click', function(e) {
        const editTrigger = e.target.closest('.single-edit-btn');
        if (!editTrigger) return;

        const id = editTrigger.getAttribute('data-id');
        const name = editTrigger.getAttribute('data-name');

        regionForm.setAttribute('data-mode', 'edit');
        regionForm.setAttribute('action', `/regions/edit/${id}/`);
        
        if (formTitleBlock) {
            formTitleBlock.innerHTML = `
                <h3><i class="bi bi-pencil-square color-edit"></i> Modify Zone</h3>
                <p>Altering existing territorial database rows parameters.</p>
            `;
        }
        if (submitFormBtn) {
            submitFormBtn.textContent = "Commit Zone Updates";
            submitFormBtn.classList.add('modify-theme-btn');
        }
        if (cancelEditBtn) cancelEditBtn.style.display = 'block';

        if (inputNameField) inputNameField.value = name;

        regionForm.scrollIntoView({ behavior: 'smooth' });
    });

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function(e) {
            e.preventDefault();
            resetRegionFormState();
        });
    }

    function resetRegionFormState() {
        if (!regionForm) return;
        regionForm.setAttribute('data-mode', 'add');
        regionForm.setAttribute('action', '/regions/add/');
        if (formTitleBlock) {
            formTitleBlock.innerHTML = `
                <h3><i class="bi bi-plus-circle-fill color-add"></i> Create Region</h3>
                <p>Append a new geographic division constraint row.</p>
            `;
        }
        if (submitFormBtn) {
            submitFormBtn.textContent = "Push New Region";
            submitFormBtn.classList.remove('modify-theme-btn');
        }
        cancelEditBtn.style.display = 'none';
        regionForm.reset();
    }

    // ==========================================
    // 4. TRANSACTION ENGINE: ASYNC ADD & UPDATE
    // ==========================================
    const tableBody = document.querySelector('table tbody');

    if (regionForm) {
        regionForm.addEventListener('submit', function(e) {
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
                        const targetRow = document.querySelector(`tr[data-row-id="${data.region.id}"]`);
                        if (targetRow) {
                            targetRow.querySelector('.region-name-txt').textContent = data.region.name;
                            
                            const editBtn = targetRow.querySelector('.single-edit-btn');
                            if (editBtn) {
                                editBtn.setAttribute('data-name', data.region.name);
                            }

                            targetRow.style.background = 'rgba(16, 185, 129, 0.15)';
                            setTimeout(() => { targetRow.style.transition = 'background 0.5s'; targetRow.style.background = ''; }, 400);
                            resetRegionFormState();
                        }
                    } else {
                        const emptyFallback = document.querySelector('.empty-fallback-state');
                        if (emptyFallback) emptyFallback.closest('tr').remove();

                        const newRow = document.createElement('tr');
                        newRow.setAttribute('data-row-id', data.region.id);
                        newRow.innerHTML = `
                            <td style="text-align: center;"><input type="checkbox" class="row-select-checkbox" value="${data.region.id}"></td>
                            <td class="id-token">#${data.region.id}</td>
                            <td>
                                <div class="region-identity-cell">
                                    <div class="region-avatar"><i class="bi bi-geo-alt-fill"></i></div>
                                    <span class="region-name-txt">${data.region.name}</span>
                                </div>
                            </td>
                            <td class="user-meta-txt"><i class="bi bi-person-fill-check"></i> ${data.region.added_by}</td>
                            <td class="chrono-stamp">${data.region.added_dts}</td>
                            <td>
                                <div class="action-buttons-group">
                                    <button type="button" class="action-trigger-btn edit-trigger single-edit-btn" data-id="${data.region.id}" data-name="${data.region.name}">
                                        <i class="bi bi-pencil-square"></i>
                                    </button>
                                    <button type="button" class="action-trigger-btn delete-trigger single-delete-btn" data-id="${data.region.id}"><i class="bi bi-trash3-fill"></i></button>
                                </div>
                            </td>
                        `;
                        tableBody.appendChild(newRow); // Appends directly to bottom
                        regionForm.reset();
                    }
                } else { alert('Operation Failed: ' + data.error); }
            })
            .catch(err => console.error('Form execution error:', err));
        });
    }

    // ==========================================
    // 5. TRANSACTION ENGINE: SINGLE ASYNC TRASH DELETE
    // ==========================================
    document.addEventListener('click', function(e) {
        const trashBtn = e.target.closest('.single-delete-btn');
        if (!trashBtn) return;
        const regionId = trashBtn.getAttribute('data-id');
        if (!confirm("Are you sure you want to permanently delete this operational territory?")) return;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/regions/delete/${regionId}/`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const targetRow = document.querySelector(`tr[data-row-id="${regionId}"]`);
                if (targetRow) {
                    targetRow.style.transition = 'all 0.3s ease'; targetRow.style.opacity = '0';
                    setTimeout(() => targetRow.remove(), 300);
                }
            }
        });
    });

    // ==========================================
    // 6. MULTI-SELECT LEDGER BAR HOOKS
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
            selectedCountTxt.textContent = `${selectedCount} Region${selectedCount > 1 ? 's' : ''} Selected`;
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
            if (!confirm(`Permanently delete all ${selectedIds.length} selected regions?`)) return;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/regions/bulk-delete/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify({ 'region_ids': selectedIds })
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

    // ==========================================
    // 7. REGIONS MULTI-FORMAT BULK UPLOAD SYSTEM
    // ==========================================
    const modal = document.getElementById('bulkImportModal');
    const openBtn = document.getElementById('open-bulk-modal');
    const closeBtn = document.getElementById('close-bulk-modal');
    const bulkUploadForm = document.getElementById('bulk-upload-form');
    const filePicker = document.querySelector('.native-file-picker');
    const uploadText = document.querySelector('.upload-placeholder-txt');

    function purgePreviousImportSummary() {
        const summaryReport = document.querySelector('.import-summary-matrix');
        if (summaryReport) summaryReport.remove();
    }

    if (openBtn && modal && closeBtn) {
        openBtn.addEventListener('click', () => modal.style.display = 'flex');
        
        closeBtn.addEventListener('click', () => { 
            modal.style.display = 'none'; 
            purgePreviousImportSummary(); 
        });
        
        modal.addEventListener('click', (e) => { 
            if (e.target === modal) { modal.style.display = 'none'; purgePreviousImportSummary(); } 
        });
    }

    if (filePicker && uploadText) {
        filePicker.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                uploadText.textContent = `Staged File: ${this.files[0].name}`;
                uploadText.style.color = 'var(--glow-product)';
            }
        });
    }

    if (bulkUploadForm) {
        bulkUploadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const executeBtn = this.querySelector('.bulk-execute-btn');
            
            if (executeBtn) {
                executeBtn.disabled = true;
                executeBtn.innerHTML = `<i class="bi bi-arrow-repeat animate-spin"></i> Reading Matrix...`;
            }

            fetch('/regions/bulk-upload/', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('Ingestion Disconnect Error: ' + data.error);
                    if (executeBtn) {
                        executeBtn.disabled = false;
                        executeBtn.innerHTML = `<i class="bi bi-terminal-plus"></i> Import`;
                    }
                }
            })
            .catch(err => {
                console.error('Bulk Pipeline Failure Context Exception:', err);
                if (executeBtn) {
                    executeBtn.disabled = false;
                    executeBtn.innerHTML = `<i class="bi bi-terminal-plus"></i> Import`;
                }
            });
        });
    }

    // ==========================================
    // 8. SINGLE BUTTON DUAL EXPORT ENGINE (EXCEL & CSV)
    // ==========================================
    const menuTrigger = document.getElementById('exportMenuTrigger');
    const dropdownMenu = document.getElementById('exportDropdownMenu');
    const exportOptions = document.querySelectorAll('.export-option-link');

    if (menuTrigger && dropdownMenu) {
        menuTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', function() {
            dropdownMenu.style.display = 'none';
        });
    }

    if (exportOptions.length > 0) {
        exportOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (dropdownMenu) dropdownMenu.style.display = 'none';

                const selectedFormat = this.getAttribute('data-format');
                const staticTable = document.querySelector('table');
                if (!staticTable) return;

                const virtualTable = staticTable.cloneNode(true);
                const targetRows = virtualTable.querySelectorAll('tr');
                const pageTitle = document.title.replace(/\s+/g, '_').toLowerCase();
                const dateStamp = new Date().toISOString().slice(0, 10);
                const filename = `${pageTitle}_export_${dateStamp}`;

                virtualTable.querySelectorAll('.empty-fallback-state').forEach(el => el.closest('tr').remove());

                targetRows.forEach(row => {
                    const cells = row.querySelectorAll('th, td');
                    cells.forEach((cell, idx) => {
                        if (idx === 0 || idx === (cells.length - 1)) {
                            cell.remove();
                        } else {
                            cell.textContent = cell.textContent.replace(/\s+/g, ' ').trim();
                        }
                    });
                });

                if (selectedFormat === 'xlsx') {
                    if (typeof XLSX !== 'undefined') {
                        const workSheet = XLSX.utils.table_to_sheet(virtualTable);
                        const workBook = XLSX.utils.book_new();
                        const colWidths = [];
                        for (let col in workSheet) {
                            if (col[0] === '!') continue;
                            const cellValue = workSheet[col].v ? String(workSheet[col].v) : '';
                            const cellLen = cellValue.length + 4;
                            const colIdx = col.replace(/[0-9]/g, '');
                            if (!colWidths[colIdx] || colWidths[colIdx] < cellLen) colWidths[colIdx] = cellLen;
                        }
                        workSheet['!cols'] = Object.keys(colWidths).map(k => ({ wch: colWidths[k] }));
                        XLSX.utils.book_append_sheet(workBook, workSheet, "Data Ledger");
                        XLSX.writeFile(workBook, `${filename}.xlsx`);
                    } else {
                        alert("Export Error: SheetJS library (XLSX) is missing in template header.");
                    }
                } else if (selectedFormat === 'csv') {
                    let csvContent = [];
                    const rows = virtualTable.querySelectorAll('tr');
                    rows.forEach(row => {
                        let rowData = [];
                        const cells = row.querySelectorAll('th, td');
                        cells.forEach(cell => {
                            let cleanText = cell.textContent.replace(/"/g, '""');
                            if (cleanText.includes(',') || cleanText.includes('"') || cleanText.includes('\n')) {
                                cleanText = `"${cleanText}"`;
                            }
                            rowData.push(cleanText);
                        });
                        if (rowData.length > 0) csvContent.push(rowData.join(','));
                    });
                    const csvBlob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' });
                    const downloadLink = document.createElement('a');
                    downloadLink.href = URL.createObjectURL(csvBlob);
                    downloadLink.setAttribute('download', `${filename}.csv`);
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                }
            });
        });
    }
});