document.addEventListener("DOMContentLoaded", function() {

    // ==========================================
    // 1. FORM FIELD CYBER STYLING INITIALIZER
    // ==========================================
    const formElements = document.querySelectorAll('.django-injected-form-wrapper p input, .django-injected-form-wrapper p select');
    formElements.forEach(element => {
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.classList.add('premium-cyber-input-element');
        }
    });

    // ==========================================
    // 2. MODAL WINDOW CONTROLLER (INTERACTIVE)
    // ==========================================
    const modal = document.getElementById('bulkImportModal');
    const openBtn = document.getElementById('open-bulk-modal');
    const closeBtn = document.getElementById('close-bulk-modal');

    // INTERACTIVE AUTO-OPEN: If template reports a summary exists, force modal layout to show instantly
    if (modal && document.querySelector('.import-summary-matrix')) {
        modal.style.display = 'flex';
    }

    function purgePreviousImportSummary() {
        if (modal) {
            const summaryReport = document.querySelector('.import-summary-matrix');
            if (summaryReport) summaryReport.remove();
        }
    }

    if (openBtn && modal && closeBtn) {
        openBtn.addEventListener('click', () => modal.style.display = 'flex');
        closeBtn.addEventListener('click', () => { modal.style.display = 'none'; purgePreviousImportSummary(); resetFileState(); });
        modal.addEventListener('click', (e) => { if (e.target === modal) { modal.style.display = 'none'; purgePreviousImportSummary(); resetFileState(); } });
    }

    // ==========================================
    // 3. FILE PICKER FILENAME TRACKER
    // ==========================================
    const filePicker = document.querySelector('.native-file-picker');
    const uploadText = document.querySelector('.upload-placeholder-txt');
    const clearBtn = document.getElementById('clear-file-btn');

    if (filePicker && uploadText && clearBtn) {
        filePicker.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                uploadText.innerHTML = `<strong>Selected:</strong> ${this.files[0].name}`;
                uploadText.style.color = '#06b6d4'; // Cyan UI themed highlight match
                clearBtn.style.display = 'flex';
            } else {
                resetFileState();
            }
        });
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault(); e.stopPropagation();
            resetFileState();
        });
    }

    function resetFileState() {
        if (filePicker) filePicker.value = '';
        if (uploadText) {
            uploadText.textContent = "Drop CSV/Excel region schema file here or click to browse";
            uploadText.style.color = '#94a3b8';
        }
        if (clearBtn) clearBtn.style.display = 'none';
    }

    // ==========================================
    // 4. INTERCEPT EDIT BUTTON CLICK (LIVE FLIP)
    // ==========================================
    const addRegionForm = document.getElementById('add-product-form'); // Matches the form element ID in region template
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const submitFormBtn = addRegionForm?.querySelector('.submit-core-action-btn');
    const formTitle = document.querySelector('.form-title-block h3');

    // Mapped straight to regional database entity column names
    const inputNameField = document.querySelector('[name="regionname"]');

    document.addEventListener('click', function(e) {
        const editBtn = e.target.closest('.single-edit-btn');
        if (!editBtn) return;

        const id = editBtn.getAttribute('data-id');
        const name = editBtn.getAttribute('data-name');

        addRegionForm.setAttribute('data-mode', 'edit');
        addRegionForm.setAttribute('action', `/regions/edit/${id}/`); 
        if (formTitle) formTitle.innerHTML = `<i class="bi bi-pencil-square color-edit"></i> Edit Region #${id}`;
        if (submitFormBtn) {
            submitFormBtn.textContent = "Commit Region Updates";
            submitFormBtn.classList.add('modify-theme-btn');
        }
        if (cancelEditBtn) cancelEditBtn.style.display = 'block';

        if (inputNameField) inputNameField.value = name;
        
        addRegionForm.scrollIntoView({ behavior: 'smooth' });
    });

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormState();
        });
    }

    function resetFormState() {
        if (!addRegionForm) return;
        addRegionForm.setAttribute('data-mode', 'add');
        addRegionForm.setAttribute('action', '/regions/add/');
        if (formTitle) formTitle.innerHTML = `<i class="bi bi-plus-circle-fill color-add"></i> Create Region`;
        if (submitFormBtn) {
            submitFormBtn.textContent = "Push New Region";
            submitFormBtn.classList.remove('modify-theme-btn');
        }
        cancelEditBtn.style.display = 'none';
        addRegionForm.reset();
    }

    // ==========================================
    // 5. ASYNC FORM CREATION & UPDATES (POST ENGINE)
    // ==========================================
    const tableBody = document.querySelector('table tbody');

    if (addRegionForm) {
        addRegionForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const targetUrl = this.getAttribute('action');
            const currentMode = this.getAttribute('data-mode');

            fetch(targetUrl, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (currentMode === 'edit') {
                        const targetRow = document.querySelector(`tr[data-row-id="${data.region.id}"]`);
                        if (targetRow) {
                            targetRow.querySelector('.region-name-txt').textContent = data.region.name;
                            
                            const rowEditBtn = targetRow.querySelector('.single-edit-btn');
                            if (rowEditBtn) {
                                rowEditBtn.setAttribute('data-name', data.region.name);
                            }
                            
                            targetRow.style.background = 'rgba(6, 182, 212, 0.15)';
                            setTimeout(() => { targetRow.style.transition = 'background 0.5s'; targetRow.style.background = ''; }, 400);
                            resetFormState();
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
                        tableBody.appendChild(newRow);
                        addRegionForm.reset();
                    }
                } else { alert('Error: ' + data.error); }
            });
        });
    }

    // ==========================================
    // 6. SINGLE INLINE ROW ASYNC DELETE
    // ==========================================
    document.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.single-delete-btn');
        if (!deleteBtn) return;
        const regionId = deleteBtn.getAttribute('data-id');
        if (!confirm("Permanently delete this territorial record?")) return;
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
    // 7. MULTI-SELECT LEDGER BAR HOOKS
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
            if (!confirm(`Delete ${selectedIds.length} regional records?`)) return;
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
    // 8. ASYNC BULK UPLOAD SUBMISSION ENGINE (FIXED ENDPOINT)
    // ==========================================
    const bulkUploadForm = document.getElementById('bulk-upload-form');
    const bulkSubmitBtn = bulkUploadForm?.querySelector('.bulk-execute-btn');
    const originalSubmitHtml = bulkSubmitBtn ? bulkSubmitBtn.innerHTML : '';

    if (bulkUploadForm) {
        bulkUploadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!filePicker || !filePicker.files.length) {
                alert('Please select a file before execution.');
                return;
            }

            bulkSubmitBtn.disabled = true;
            bulkSubmitBtn.innerHTML = `<i class="bi bi-arrow-clockwise" style="display:inline-block; animation: spin 1s linear infinite;"></i> Mapping Spatial Schema...`;
            if (clearBtn) clearBtn.style.pointerEvents = 'none';

            const formData = new FormData(this);
            // TARGET ALIGNMENT: Dynamically hits regional endpoint layout fallback safely
            const targetUrl = this.action || window.location.origin + '/regions/bulk-upload/';

            fetch(targetUrl, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => {
                const contentType = response.headers.get('content-type');
                
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(data => {
                        if (!response.ok) throw new Error(data.error || 'Spatial coordinate pipeline processing failure.');
                        return data;
                    });
                } else {
                    return response.text().then(htmlText => {
                        console.error('Server returned HTML mismatch layer:', htmlText);
                        throw new Error(`Server returned HTML (Status ${response.status}) at route: "${targetUrl}".`);
                    });
                }
            })
            .then(data => {
                window.location.reload();
            })
            .catch(error => {
                console.error('Regional Processing Failure Logged:', error);
                alert(`Ingestion processing faulted: ${error.message}`);
                
                bulkSubmitBtn.disabled = false;
                bulkSubmitBtn.innerHTML = originalSubmitHtml;
                if (clearBtn) clearBtn.style.pointerEvents = 'auto';
            });
        });
    }

    // ==========================================
    // 9. DUAL EXPORT ENGINE (EXCEL & CSV)
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
                e.preventDefault(); e.stopPropagation();
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
                        XLSX.utils.book_append_sheet(workBook, workSheet, "Territory Ledger");
                        XLSX.writeFile(workBook, `${filename}.xlsx`);
                    } else {
                        alert("Export Error: SheetJS library missing.");
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