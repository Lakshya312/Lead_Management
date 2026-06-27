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

    // Auto-open modal container structure if summary details populate on refresh
    if (modal && document.querySelector('.import-summary-matrix')) {
        modal.style.display = 'flex';
    }

    function purgePreviousImportSummary() {
        if (modal) {
            const summaryReport = modal.querySelector('.import-summary-matrix');
            if (summaryReport) summaryReport.remove();
        }
    }

    if (openBtn && modal && closeBtn) {
        openBtn.addEventListener('click', () => modal.style.display = 'flex');
        closeBtn.addEventListener('click', () => { 
            modal.style.display = 'none'; 
            purgePreviousImportSummary(); 
            resetFileState(); 
        });
        modal.addEventListener('click', (e) => { 
            if (e.target === modal) { 
                modal.style.display = 'none'; 
                purgePreviousImportSummary(); 
                resetFileState(); 
            } 
        });
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
                // Matches layout precisely using Lead Theme Color #818cf8
                uploadText.innerHTML = `Selected: <span style="color: #818cf8; font-weight: 600;">${this.files[0].name}</span>`;
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
            uploadText.textContent = "Drop CSV/Excel lead pipeline schema file here or click to browse";
            uploadText.style.color = '#94a3b8';
        }
        if (clearBtn) clearBtn.style.display = 'none';
    }

    // ==========================================
    // 4. INTERCEPT EDIT BUTTON CLICK (LIVE FLIP)
    // ==========================================
    const addProductForm = document.getElementById('add-product-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const submitFormBtn = addProductForm?.querySelector('.submit-core-action-btn');
    const formTitle = document.querySelector('.form-title-block h3');

    const inputNameField = document.querySelector('[name="productname"]');
    const selectCategoryField = document.querySelector('[name="categoryid"]');
    const checkActiveField = document.querySelector('[name="is_active"]');

    document.addEventListener('click', function(e) {
        const editBtn = e.target.closest('.single-edit-btn');
        if (!editBtn) return;

        const id = editBtn.getAttribute('data-id');
        const name = editBtn.getAttribute('data-name');
        const category = editBtn.getAttribute('data-category');
        const active = editBtn.getAttribute('data-active');

        addProductForm.setAttribute('data-mode', 'edit');
        addProductForm.setAttribute('action', `/products/edit/${id}/`);
        if (formTitle) formTitle.innerHTML = `<i class="bi bi-pencil-square color-edit"></i> Edit Product #${id}`;
        if (submitFormBtn) {
            submitFormBtn.textContent = "Commit Asset Updates";
            submitFormBtn.classList.add('modify-theme-btn');
        }
        if (cancelEditBtn) cancelEditBtn.style.display = 'block';

        if (inputNameField) inputNameField.value = name;
        if (selectCategoryField) selectCategoryField.value = category;
        if (checkActiveField) {
            checkActiveField.checked = (active === '1' || active === 'True');
        }
        
        addProductForm.scrollIntoView({ behavior: 'smooth' });
    });

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function(e) { e.preventDefault(); resetFormState(); });
    }

    function resetFormState() {
        if (!addProductForm) return;
        addProductForm.setAttribute('data-mode', 'add');
        addProductForm.setAttribute('action', '/products/add/');
        if (formTitle) formTitle.innerHTML = `<i class="bi bi-plus-circle-fill color-add"></i> Add Product`;
        if (submitFormBtn) {
            submitFormBtn.textContent = "Push New Asset";
            submitFormBtn.classList.remove('modify-theme-btn');
        }
        cancelEditBtn.style.display = 'none';
        addProductForm.reset();
    }

    // ==========================================
    // 5. ASYNC FORM CREATION & UPDATES (POST ENGINE)
    // ==========================================
    if (addProductForm) {
        addProductForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const targetUrl = this.getAttribute('action');
            const currentMode = this.getAttribute('data-mode');

            fetch(targetUrl, { method: 'POST', body: formData, headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (currentMode === 'edit') {
                        const targetRow = document.querySelector(`tr[data-row-id="${data.product.id}"]`);
                        if (targetRow) {
                            targetRow.querySelector('.product-name-txt').textContent = data.product.name;
                            targetRow.querySelector('.category-tag-pill').textContent = data.product.category;
                            
                            const rowEditBtn = targetRow.querySelector('.single-edit-btn');
                            if (rowEditBtn) {
                                rowEditBtn.setAttribute('data-name', data.product.name);
                                rowEditBtn.setAttribute('data-category', selectCategoryField.value);
                                rowEditBtn.setAttribute('data-active', data.product.is_active);
                            }
                            resetFormState();
                        }
                    } else {
                        window.location.reload();
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
        const productId = deleteBtn.getAttribute('data-id');
        if (!confirm("Permanently delete this record?")) return;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/products/delete/${productId}/`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const targetRow = document.querySelector(`tr[data-row-id="${productId}"]`);
                if (targetRow) targetRow.remove();
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
            selectedCountTxt.textContent = `${selectedCount} Asset${selectedCount > 1 ? 's' : ''} Selected`;
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
            if (!confirm(`Delete ${selectedIds.length} records?`)) return;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/products/bulk-delete/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify({ 'product_ids': selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) { window.location.reload(); }
            });
        });
    }

    // ==========================================
    // 8. ASYNC BULK UPLOAD ENGINE
    // ==========================================
    const bulkUploadForm = document.getElementById('bulk-upload-form');
    const bulkSubmitBtn = bulkUploadForm?.querySelector('.bulk-execute-btn');
    const originalSubmitHtml = bulkSubmitBtn ? bulkSubmitBtn.innerHTML : '';

    if (bulkUploadForm) {
        bulkUploadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!filePicker || !filePicker.files.length) {
                alert('Please select a pipeline asset spreadsheet file.');
                return;
            }

            bulkSubmitBtn.disabled = true;
            bulkSubmitBtn.innerHTML = `<i class="bi bi-arrow-clockwise" style="display:inline-block; animation: spin 1s linear infinite;"></i> Processing...`;
            if (clearBtn) clearBtn.style.pointerEvents = 'none';

            const formData = new FormData(this);
            const targetUrl = this.action || window.location.origin + '/leads/bulk-upload/';

            fetch(targetUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(data => {
                        if (!response.ok) throw new Error(data.error || 'Data intake validation processing error.');
                        return data;
                    });
                } else {
                    return response.text().then(htmlText => {
                        console.error('Server layout rendering exception:', htmlText);
                        throw new Error(`Server returned HTML (Status ${response.status}).`);
                    });
                }
            })
            .then(data => {
                window.location.reload();
            })
            .catch(error => {
                console.error('Pipeline Execution Critical Failure:', error);
                alert(`Ingestion processing faulted: ${error.message}`);
                
                bulkSubmitBtn.disabled = false;
                bulkSubmitBtn.innerHTML = originalSubmitHtml;
                if (clearBtn) clearBtn.style.pointerEvents = 'auto';
            });
        });
    }

    setupExportSystem();
});

function setupExportSystem() {
    const menuTrigger = document.getElementById('exportMenuTrigger');
    const dropdownMenu = document.getElementById('exportDropdownMenu');
    const exportOptions = document.querySelectorAll('.export-option-link');

    if (menuTrigger && dropdownMenu) {
        menuTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', function() { dropdownMenu.style.display = 'none'; });
    }

    exportOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault(); e.stopPropagation();
            if (dropdownMenu) dropdownMenu.style.display = 'none';

            const selectedFormat = this.getAttribute('data-format');
            const staticTable = document.querySelector('table');
            if (!staticTable) return;

            const virtualTable = staticTable.cloneNode(true);
            const targetRows = virtualTable.querySelectorAll('tr');
            const filename = `${document.title.replace(/\s+/g, '_').toLowerCase()}_export`;

            virtualTable.querySelectorAll('.empty-fallback-state').forEach(el => el.closest('tr').remove());

            targetRows.forEach(row => {
                const cells = row.querySelectorAll('th, td');
                cells.forEach((cell, idx) => {
                    if (idx === 0 || idx === (cells.length - 1)) { cell.remove(); } 
                    else { cell.textContent = cell.textContent.replace(/\s+/g, ' ').trim(); }
                });
            });

            if (selectedFormat === 'xlsx') {
                if (typeof XLSX !== 'undefined') {
                    const workSheet = XLSX.utils.table_to_sheet(virtualTable);
                    const workBook = XLSX.utils.book_new();
                    XLSX.utils.book_append_sheet(workBook, workSheet, "Data Ledger");
                    XLSX.writeFile(workBook, `${filename}.xlsx`);
                }
            } else if (selectedFormat === 'csv') {
                let csvContent = [];
                virtualTable.querySelectorAll('tr').forEach(r => {
                    let rowData = [];
                    r.querySelectorAll('th, td').forEach(c => {
                        let txt = c.textContent.replace(/"/g, '""');
                        if (txt.includes(',') || txt.includes('"')) txt = `"${txt}"`;
                        rowData.push(txt);
                    });
                    if (rowData.length > 0) csvContent.push(rowData.join(','));
                });
                const csvBlob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' });
                const downloadLink = document.createElement('a');
                downloadLink.href = URL.createObjectURL(csvBlob);
                downloadLink.setAttribute('download', `${filename}.csv`);
                document.body.appendChild(downloadLink); downloadLink.click(); document.body.removeChild(downloadLink);
            }
        });
    });
}