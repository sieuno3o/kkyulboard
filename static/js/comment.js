function createButton(text, id) {
    const btn = document.createElement('button');
    btn.id = id;
    btn.type = 'submit';
    btn.classList.add('btn');
    btn.classList.add('btn-primary');
    btn.textContent = text;
    return btn
}

function refreshCommentList(postId) {
    fetch(`/board/get_comments?post_id=${postId}`)
        .then(response => response.json())
        .then(comments => {
            const commentCountText = document.getElementById('comment-count');
            commentCountText.innerHTML = comments.length

            const tbody = document.getElementById('comment-table-body');
            tbody.innerHTML = '';

            const textComments = document.getElementById('text-comments')
            if (textComments) {
                textComments.value = '';
            }
            let idx = 0
            comments.forEach(comment => {
                const tr = document.createElement('tr');
                const tdUserName = document.createElement('td');
                const tdComments = document.createElement('td');
                const tdUpdateDate = document.createElement('td');

                tdUserName.textContent = comment.username;
                tdComments.textContent = comment.comments;
                tdUpdateDate.textContent = comment.updated_at;

                if (comment.is_login && (comment.current_user_id === comment.user_id)) {
                    const updateBtnId = `btn-update-comment${idx}`;
                    const deleteBtnId = `btn-delete-comment${idx}`;
                    const btnUpdate = createButton('수정', updateBtnId);
                    const btnDelete = createButton('삭제', deleteBtnId);

                    tdUpdateDate.appendChild(btnUpdate);
                    tdUpdateDate.appendChild(btnDelete);

                    addDeleteButtonListener(btnDelete, postId, comment.comment_id);
                }

                tr.appendChild(tdUserName);
                tr.appendChild(tdComments);
                tr.appendChild(tdUpdateDate);

                tbody.appendChild(tr)
                idx++
            });
        });
}

function addDeleteButtonListener(btnDelete, postId, commentId) {
    btnDelete.addEventListener('click', function () {
        const result = confirm('댓글을 삭제하시겠습니까?');
        if (result) {
            fetch(`/board/delete_comment/${commentId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({comment_id: commentId})
            })
                .then(response => response.json())
                .then(data => {
                    refreshCommentList(postId);
                })
        }
    });
}

function addEventListenersToElements(postId) {
    document.getElementById('comment-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        formData.append('post_id', postId)
        fetch('/board/add_comment', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                refreshCommentList(postId);
            });
    });

    document.getElementById('text-comments').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            document.getElementById('btn-register').click();
        }
    })
}
