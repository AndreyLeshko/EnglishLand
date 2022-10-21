let ajax = new XMLHttpRequest()

const train_id = document.querySelector('#train_id').value
let href = '/words/trains/change-status/' + train_id + '/'
const markAsStudiedBtn = document.querySelector('.mark-as-studied-btn')
const returnToStudyBtn = document.querySelector('.return-to-study-btn')


function change_train_status_request() {
    ajax.open('GET', href, true)
    ajax.send()
    ajax.addEventListener('readystatechange', function () {
        if (this.readyState == 4 && this.status == 201) {
            console.log('Success', this.readyState)
            markAsStudiedBtn.classList.toggle('hidden')
            returnToStudyBtn.classList.toggle('hidden')
            ajax = new XMLHttpRequest()
        }
    })
}


document.querySelector('.mark-as-studied-btn').addEventListener('click', change_train_status_request)
document.querySelector('.return-to-study-btn').addEventListener('click', change_train_status_request)


    



