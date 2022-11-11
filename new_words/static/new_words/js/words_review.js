const questionImgSrc = '/static/base/img/question_mark.png'
const studyingImgSrc = '/static/base/img/studying.png'
const completedImgSrc = '/static/base/img/completed.png'


let $table = document.querySelector('#words-table')
let $paginator = document.querySelector('#paginator')
const $filtersApplyBtn = document.querySelector('.fitters-button')

let wordsArray = null
let pageData = null 
let currentPageNum = 1

function main() {
    requestData()
    $filtersApplyBtn.addEventListener('click', () => {currentPageNum = 1; requestData()})
}
main()

function requestData() {
    let url = getUrl()
    fetch(url).then((response) => {
        return response.json()
        }).then(response => {
            wordsArray = response['words']
            pageData = response['pagination']
            updateTable()
            updatePaginator()
        })
}

function getUrl() {
    let url = `/words/api/words/?page=${currentPageNum}`

    let status = document.querySelector('#status').value
    if (status != 'all') {
        url += `&status=${status}`
    }
    
    let category = document.querySelector('#categories').value
    if (category != 'all') {
        url += `&categories=${category}`
    }
    return url
}

function updateTable() {
    $table.innerHTML = ''

    const categoryNames = {
        'noun': 'существительное',
        'verb': 'глагол',
        'adjective': 'прилагательное',
        'adverb': 'наречие',
        'pronoun': 'местоимение',
        'other': 'другая',
        'unknown': '???',
    }

    let headersRow = document.createElement('tr')
    headersRow.innerHTML = `
        <th>Статус</th>
        <th>Слово</th>
        <th>Переводы</th>
        <th>Категории</th>
        `
    $table.appendChild(headersRow)

    for (wordData of wordsArray) {
        let row = document.createElement('tr')

        const translates = []
        const categories = []
        for (let translate of wordData['vocabulary']) {
            translates.push(translate['russian']['russian'])
            if (categories.indexOf(categoryNames[translate['category']]) == -1) {
                categories.push(categoryNames[translate['category']])
            }
        }

        let img_src = questionImgSrc
        if (wordData['status'] == 'on_study') {
            img_src = studyingImgSrc
        } else if (wordData['status'] == 'studied') {
            img_src = completedImgSrc
        }

        row.innerHTML = `
            <td class='status-label'>
                <img src='${img_src}' height=18px>
                <input type='hidden' class='word-id' value='${wordData['id']}'>
                <input type='hidden' class='word-status' value='${wordData['status']}'>
            </td>
            <td>${wordData['english']}</td>
            <td>${translates.join('; ')}</td>
            <td>${categories.join('; ')}</td>
        `
        let wordStatusLabel = row.querySelector('.status-label')
        wordStatusLabel.addEventListener('click', changeStatus)
        $table.appendChild(row)
    }
}

function changeStatus() {
    let wordId = this.querySelector('.word-id').value
    let wordStatus = this.querySelector('.word-status').value

    let cookies = document.cookie.split(';')
    let token = null
    for (let cookie of cookies) {
        key = cookie.split('=')[0]
        value = cookie.split('=')[1]
        if (key == 'csrftoken') {
            token = value
            break
        }
    }
    if (wordStatus === 'null') {
        url = '/words/api/add-word-to-train/'
        fetch(url, {
            method: 'post',
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'word_id': wordId})
        }).then(response => {
            this.querySelector('img').src=studyingImgSrc
            this.querySelector('.word-status').value = 'on_study'
        })
    }
}

function updatePaginator() {
    $paginator.innerHTML = ''
    let curPage = pageData['cur_page']
    for (let pageNum = 1; pageNum <= pageData['number_of_pages']; pageNum++) {
        if (pageNum == 1 || pageNum == pageData['number_of_pages'] || Math.abs(pageNum - curPage) <= 3) {
            let pageLink = document.createElement('a')
            pageLink.href = `?page=${pageNum}`
            pageLink.classList.add('page-link')
            pageLink.textContent = pageNum
            pageLink.addEventListener('click', changePage)
            $paginator.appendChild(pageLink)
            if (pageNum == currentPageNum) {
                pageLink.classList.add('active-page')
            }
        } else if (Math.abs(pageNum - curPage) == 4) {
            let missingPages = document.createElement('span')
            missingPages.textContent = '.....'
            $paginator.appendChild(missingPages)
        }
    }
}

function changePage(ev) {
    ev.preventDefault()
    currentPageNum = this.textContent
    requestData()
}