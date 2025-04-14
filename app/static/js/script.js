// JavaScript for Fauxmots SMTP Server

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Update SMTP status indicator
    function updateSmtpStatus() {
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                const statusElement = document.getElementById('smtp-status');
                if (statusElement) {
                    statusElement.innerHTML = `<span class="badge bg-success">SMTP Server: Running (${data.smtp_host}:${data.smtp_port})</span>`;
                }
            })
            .catch(error => {
                const statusElement = document.getElementById('smtp-status');
                if (statusElement) {
                    statusElement.innerHTML = `<span class="badge bg-danger">SMTP Server: Error</span>`;
                }
                console.error('Error fetching SMTP status:', error);
            });
    }
    
    // Call once on page load
    updateSmtpStatus();
    
    // Setup periodic refresh of status
    setInterval(updateSmtpStatus, 60000); // Every minute
    
    // Handle HTMX after-swap event for reinitializing components
    document.body.addEventListener('htmx:afterSwap', function(event) {
        // Reinitialize tooltips after content is updated via HTMX
        var newTooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var newTooltipList = newTooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });
});
