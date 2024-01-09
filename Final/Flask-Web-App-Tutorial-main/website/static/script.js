function markTaskAsCompleted(taskId) {
    const checkbox = document.getElementById(`task_${taskId}`);
    if (checkbox.checked) {
        // Send an AJAX request to mark the task as completed
        fetch(`/mark_task_completed/${taskId}`)
            .then(response => {
                if (response.ok) {
                    // Move the task card to the "Done Tasks" section
                    const taskCard = checkbox.closest('.task-card');
                    document.getElementById('done-tasks').appendChild(taskCard);
                } else {
                    // Handle the error
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}
