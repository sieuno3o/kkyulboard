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

                const collapsedCommentId = `collapse-comments-${idx}`

                // user name
                const tdUserName = document.createElement('td');
                tdUserName.textContent = comment.username;

                // comments
                const tdComments = document.createElement('td');

                // div content
                const divContent = document.createElement('div')
                divContent.classList.add('collapse')
                divContent.classList.add('show')
                divContent.id = collapsedCommentId
                divContent.textContent = comment.comments

                const divUpdate = document.createElement('div')
                divUpdate.classList.add('collapse')
                divUpdate.id = collapsedCommentId
                const form = document.createElement('form')

                const textArea = document.createElement('textarea')
                textArea.id = 'update-comment-text'
                textArea.classList.add('form-control')
                textArea.rows = 3
                textArea.textContent = comment.comments

                const input = document.createElement('input')
                input.type = 'hidden'
                input.id = 'update-comment-id'
                input.value = comment.comment_id

                const btnUpdateFinish = document.createElement('button')
                btnUpdateFinish.type = 'submit'
                btnUpdateFinish.classList.add('btn')
                btnUpdateFinish.classList.add('btn-primary')
                btnUpdateFinish.classList.add('comment-update-btn')
                btnUpdateFinish.textContent = '수정 완료'

                form.appendChild(textArea)
                form.appendChild(input)
                form.appendChild(btnUpdateFinish)

                divUpdate.appendChild(form)
                tdComments.appendChild(divContent)
                tdComments.appendChild(divUpdate)

                //Date, Buttons
                const tdDateAndButton = document.createElement('td');
                tdDateAndButton.textContent = comment.updated_at;

                if (comment.is_login && (comment.current_user_id === comment.user_id)) {
                    const updateBtnId = `btn-update-comment${idx}`;
                    const deleteBtnId = `btn-delete-comment${idx}`;
                    const btnUpdate = createButton('수정', updateBtnId);
                    btnUpdate.setAttribute('data-bs-toggle', 'collapse')
                    btnUpdate.setAttribute('data-bs-target', `#${collapsedCommentId}`)

                    const btnDelete = createButton('삭제', deleteBtnId);

                    tdDateAndButton.appendChild(btnUpdate);
                    tdDateAndButton.appendChild(btnDelete);

                    addDeleteButtonListener(btnDelete, postId, comment.comment_id);
                }

                tr.appendChild(tdUserName);
                tr.appendChild(tdComments);
                tr.appendChild(tdDateAndButton);

                tbody.appendChild(tr)
                idx++
            });
            comment.init(postId)
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

// 데이터 전송 객체 생성!
var comment = {
    // 이벤트 등록
    init: function (postId) {
        var _this = this;

        // 수정 버튼 변수화
        const updateBtns = document.querySelectorAll('.comment-update-btn');
        // 모든 수정 버튼별, 이벤트 등록
        updateBtns.forEach(function (item) {
            item.addEventListener('click', function () { // 클릭 이벤트 발생시,
                var form = this.closest('form'); // 클릭 이벤트가 발생한 버튼에 제일 가까운 폼을 찾고,
                _this.update(form, postId); // 해당 폼으로, 업데이트 수행한다!
            });
        });
    },

    // 댓글 수정
    update: function (form, postId) {
        var data = {
            id: form.querySelector('#update-comment-id').value,
            content: form.querySelector('#update-comment-text').value,
        };

        fetch('/board/update_comment', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then(data => {
            refreshCommentList(postId);
        })
    }
}