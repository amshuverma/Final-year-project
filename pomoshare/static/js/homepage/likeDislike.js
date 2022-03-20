document.body.addEventListener('htmx:configRequest', (event) => {
    let input = document.querySelector('.comment-input')
    let commentBtn = document.querySelector('.comment-btn')

    commentBtn.addEventListener('click', () => {
        console.log(input.value)
    })
})