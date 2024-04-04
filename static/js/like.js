function refreshLike(postId) {
    fetch(`/board/get_like?post_id=${postId}`)
        .then(response => response.json())
        .then(data => {
            let strDom = "";
            if (data.is_login) {
                if (data.is_like) {
                    strDom += `<img id="like-img" src="${data.like_img}" alt="">`;
                } else {
                    strDom += `<img id="like-img" src="${data.not_like_img}" alt="">`
                }
            }
            else {
                strDom += `<img id="like-img" src="${data.not_like_img}" alt="">`
            }
            strDom += `<input type="checkbox" checked autocomplete="off">${data.like_count}`

            var $btnLabel = $("#like-btn-label")
            $btnLabel.empty()
            $btnLabel.append(strDom)

            if (data.is_login) {
                const likeImg = document.getElementById('like-img');
                likeImg.addEventListener('click', function () {
                    const like_toggled = !data.is_like
                    const json_data = {
                        is_like: like_toggled,
                        post_id: postId
                    };
                    fetch('/board/set_like', {
                        method: 'POST',
                        body: JSON.stringify(json_data),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then(response => response.json()).then(data => {
                        refreshLike(postId);
                    })
                });
            }
        });
}

function addEventListenersToElements_like(postId) {
}