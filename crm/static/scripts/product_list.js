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

    // INTERACTIVE AUTO-OPEN: If Django template reports a summary exists, force modal layout to show instantly
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
        closeBtn.addEventListener('click', () => { modal.style.display = 'none'; purgePreviousImportSummary(); resetFileState(); });
        modal.addEventListener('click', (e) => { if (e.target === modal) { modal.style.display = 'none'; purgePreviousImportSummary(); resetFileState(); } });
    }

    // ==========================================
    // 3. FILE PICKER FILENAME TRACKER (UPDATED)
    // ==========================================
    const filePicker = document.querySelector('.native-file-picker');
    const uploadText = document.querySelector('.upload-placeholder-txt');
    const clearBtn = document.getElementById('clear-file-btn');

    if (filePicker && uploadText && clearBtn) {
        filePicker.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                // Wrap filename cleanly in strong tag match per requirement
                uploadText.innerHTML = `<strong>Selected:</strong> ${this.files[0].name}`;
                uploadText.style.color = '#10b981';
                clearBtn.style.display = 'flex'; // Handles updated block alignment layout
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
            uploadText.textContent = "Drop inventory CSV/Excel file here or click to browse";
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
        cancelEditBtn.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormState();
        });
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
    const tableBody = document.querySelector('table tbody');

    if (addProductForm) {
        addProductForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const targetUrl = this.action || window.location.origin + '/products/bulk-upload/';
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

                            const badgeCell = targetRow.querySelector('.indicator-badge');
                            if (data.product.is_active == 1) {
                                badgeCell.className = "indicator-badge state-online";
                                badgeCell.innerHTML = `<i class="bi bi-shield-check"></i> Active`;
                            } else {
                                badgeCell.className = "indicator-badge state-offline";
                                badgeCell.innerHTML = `<i class="bi bi-shield-slash"></i> Inactive`;
                            }
                            
                            targetRow.style.background = 'rgba(16, 185, 129, 0.15)';
                            setTimeout(() => { targetRow.style.transition = 'background 0.5s'; targetRow.style.background = ''; }, 400);
                            resetFormState();
                        }
                    } else {
                        const emptyFallback = document.querySelector('.empty-fallback-state');
                        if (emptyFallback) emptyFallback.closest('tr').remove();

                        const newRow = document.createElement('tr');
                        newRow.setAttribute('data-row-id', data.product.id);
                        newRow.innerHTML = `
                            <td style="text-align: center;"><input type="checkbox" class="row-select-checkbox" value="${data.product.id}"></td>
                            <td class="id-token">#${data.product.id}</td>
                            <td>
                                <div class="product-identity-cell">
                                    <div class="product-avatar"><i class="bi bi-box-seam-fill"></i></div>
                                    <span class="product-name-txt">${data.product.name}</span>
                                </div>
                            </td>
                            <td><span class="category-tag-pill">${data.product.category}</span></td>
                            <td>
                                <span class="indicator-badge ${data.product.is_active ? 'state-online' : 'state-offline'}">
                                    <i class="bi ${data.product.is_active ? 'bi-shield-check' : 'bi-shield-slash'}"></i> ${data.product.is_active ? 'Active' : 'Inactive'}
                                </span>
                            </td>
                            <td class="user-meta-txt"><i class="bi bi-person-fill-check"></i> ${data.product.added_by}</td>
                            <td class="chrono-stamp">${data.product.added_dts}</td>
                            <td>
                                <div class="action-buttons-group">
                                    <button type="button" class="action-trigger-btn edit-trigger single-edit-btn" data-id="${data.product.id}" data-name="${data.product.name}" data-category="${selectCategoryField.value}" data-active="${data.product.is_active}">
                                        <i class="bi bi-pencil-square"></i>
                                    </button>
                                    <button type="button" class="action-trigger-btn delete-trigger single-delete-btn" data-id="${data.product.id}"><i class="bi bi-trash3-fill"></i></button>
                                </div>
                            </td>
                        `;
                        tableBody.appendChild(newRow);
                        addProductForm.reset();
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
                if (data.success) {
                    selectedIds.forEach(id => { const r = document.querySelector(`tr[data-row-id="${id}"]`); if (r) r.remove(); });
                    masterCheckbox.checked = false; updateBulkActionBar();
                }
            });
        });
    }

    // ==========================================
    // 8. ASYNC BULK UPLOAD SUBMISSION ENGINE (REFINED)
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

            // Lock controls & present processing status UI
            bulkSubmitBtn.disabled = true;
            bulkSubmitBtn.innerHTML = `<i class="bi bi-arrow-clockwise" style="display:inline-block; animation: spin 1s linear infinite;"></i> Mapping Spatial Schema...`;
            if (clearBtn) clearBtn.style.pointerEvents = 'none';

            const formData = new FormData(this);
            
            // TARGET ALIGNMENT: Read from the form's action property, or fall back explicitly to bulk-upload
            const targetUrl = this.action || window.location.origin + '/regions/bulk-upload/';

            fetch(targetUrl, {
                method: 'POST',
                body: formData
                // No XMLHttpRequest header wrapper needed here either!
            })
            .then(response => {
                const contentType = response.headers.get('content-type');
                
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(data => {
                        if (!response.ok) throw new Error(data.error || 'Spatial data ingestion error.');
                        return data;
                    });
                } else {
                    return response.text().then(htmlText => {
                        console.error('Server unexpected rendering pipeline response:', htmlText);
                        throw new Error(`Server returned HTML (Status ${response.status}) at route: "${targetUrl}".`);
                    });
                }
            })
            .then(data => {
                // Hard reload lets Django template catch context changes safely 
                window.location.reload();
            })
            .catch(error => {
                console.error('Regional Processing Failure Logged:', error);
                alert(`Ingestion processing faulted: ${error.message}`);
                
                // Roll back state locks
                bulkSubmitBtn.disabled = false;
                bulkSubmitBtn.innerHTML = originalSubmitHtml;
                if (clearBtn) clearBtn.style.pointerEvents = 'auto';
            });
        });
    }

    // ==========================================
    // 9. SINGLE BUTTON DUAL EXPORT ENGINE (EXCEL & CSV)
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