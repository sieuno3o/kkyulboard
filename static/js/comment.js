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
                tdComments.classList.add('changeComments')
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

function addCommentEventHandler() {
    console.log('called-2')
        //수정시 동적으로 변경하는 작업
    document.querySelectorAll('.changeComments').forEach(function (element) {
        element.addEventListener('click', function () {
            console.log('called')
            // 기존 텍스트 내용 선택
            const range = document.createRange();
            range.selectNodeContents(this);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            const currentValue = this.textContent.trim();
            const textareaElement = document.createElement('textarea');
            // 클릭한 요소의 내용을 textarea로 교체
            textareaElement.textContent = currentValue;

            // 기존 요소를 숨기고 입력 요소를 추가
            this.style.display = 'none';
            this.parentNode.insertBefore(textareaElement, this.nextSibling);

            // textarea에 포커스 주기
            textareaElement.focus();
            textareaElement.select();

            // textarea에서 엔터 키 누르면 수정 완료
            textareaElement.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    const updatedValue = textareaElement.value.trim();
                    if (updatedValue !== '') {
                        element.textContent = updatedValue;
                        console.log('Updated value:', updatedValue);
                    } else {
                        element.textContent = currentValue;
                    }
                    // 입력 요소 제거 및 기존 요소 다시 표시
                    textareaElement.parentNode.removeChild(textareaElement);
                    element.style.display = 'inline';
                }
            });

            // 포커스를 잃으면 수정 취소
            textareaElement.addEventListener('blur', function () {
                // 수정된 값이 비어있는 경우 현재 값으로 복원
                if (textareaElement.value.trim() === '') {
                    element.textContent = currentValue;
                }
                // 포커스를 잃은 경우 수정 취소
                else {
                    // 수정된 값을 해당 요소에 적용
                    element.textContent = textareaElement.value.trim();
                }

                // 입력 요소 제거 및 기존 요소 다시 표시
                textareaElement.parentNode.removeChild(textareaElement);
                element.style.display = 'inline';
            });
        });
    })
}
