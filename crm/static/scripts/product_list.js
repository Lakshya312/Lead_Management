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
    // 2. MODAL WINDOW CONTROLLER
    // ==========================================
    const modal = document.getElementById('bulkImportModal');
    const openBtn = document.getElementById('open-bulk-modal');
    const closeBtn = document.getElementById('close-bulk-modal');

    function purgePreviousImportSummary() {
        if (modal) {
            const summaryReport = modal.querySelector('.import-summary-matrix');
            if (summaryReport) summaryReport.remove();
        }
    }

    if (openBtn && modal && closeBtn) {
        openBtn.addEventListener('click', () => modal.style.display = 'flex');
        closeBtn.addEventListener('click', () => { modal.style.display = 'none'; purgePreviousImportSummary(); });
        modal.addEventListener('click', (e) => { if (e.target === modal) { modal.style.display = 'none'; purgePreviousImportSummary(); } });
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
                uploadText.textContent = `Selected: ${this.files[0].name}`;
                uploadText.style.color = 'var(--glow-product)';
                clearBtn.style.display = 'block';
            }
        });
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault(); e.stopPropagation();
            filePicker.value = '';
            uploadText.textContent = "Drop CSV/Excel file here or click to browse";
            uploadText.style.color = 'var(--text-slate)';
            clearBtn.style.display = 'none';
        });
    }

    // ==========================================
    // 4. INTERCEPT EDIT BUTTON CLICK (LIVE FLIP)
    // ==========================================
    const addProductForm = document.getElementById('add-product-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const submitFormBtn = addProductForm?.querySelector('.submit-core-action-btn');
    const formTitle = document.querySelector('.form-title-block h3');

    // Select the exact elements mapped inside form paragraph outputs dynamically
    const inputNameField = document.querySelector('[name="productname"]');
    const selectCategoryField = document.querySelector('[name="categoryid"]');
    const checkActiveField = document.querySelector('[name="is_active"]');

    document.addEventListener('click', function(e) {
        const editBtn = e.target.closest('.single-edit-btn');
        if (!editBtn) return;

        // Extract metadata attributes out of row instantly
        const id = editBtn.getAttribute('data-id');
        const name = editBtn.getAttribute('data-name');
        const category = editBtn.getAttribute('data-category');
        const active = editBtn.getAttribute('data-active');

        // Swap sidebar configuration states to Edit mode
        addProductForm.setAttribute('data-mode', 'edit');
        addProductForm.setAttribute('action', `/products/edit/${id}/`); // Rewrites submission route link on the fly
        if (formTitle) formTitle.innerHTML = `<i class="bi bi-pencil-square color-edit"></i> Edit Product #${id}`;
        if (submitFormBtn) {
            submitFormBtn.textContent = "Commit Asset Updates";
            submitFormBtn.classList.add('modify-theme-btn');
        }
        if (cancelEditBtn) cancelEditBtn.style.display = 'block';

        // Inject row values straight into input fields
        if (inputNameField) inputNameField.value = name;
        if (selectCategoryField) selectCategoryField.value = category;
        if (checkActiveField) {
            checkActiveField.checked = (active === '1' || active === 'True');
        }
        
        // Scroll smoothly to sidebar view on mobile sizes
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
                        // Live Update Existing HTML Node without redraws
                        const targetRow = document.querySelector(`tr[data-row-id="${data.product.id}"]`);
                        if (targetRow) {
                            targetRow.querySelector('.product-name-txt').textContent = data.product.name;
                            targetRow.querySelector('.category-tag-pill').textContent = data.product.category;
                            
                            // Update attributes stored on the edit trigger button itself
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
                        // Live Append Row to end of table
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
});