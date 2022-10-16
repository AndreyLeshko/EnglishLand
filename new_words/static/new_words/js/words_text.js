let HtmlObjWord = document.querySelector(".word")
let HtmlObjTranslateInput = document.querySelector(".translate-input")
let HtmlObjCheckButton = document.querySelector('.check-btn')
let HtmlObjNextButton = document.querySelector('.next-btn')
let HtmlObjLoadContainer = document.querySelector('.container.load')
let HtmlObjQuestionContainer = document.querySelector('.container.question')
let HtmlObjResultContainer = document.querySelector('.container.result')

const params = new URLSearchParams(window.location.href)
const mode = params.get('mode')
const lang = params.get('lang')

let questionData = null
let isRightAnswer = false
let questionWord = ''
let trainId = null
let translateInput = null
let translates = []
let request = new XMLHttpRequest()


function loadQuestion() {
    request = new XMLHttpRequest()
    request.open("GET", "/words/api/train-object/?&mode="+mode, true)
    request.send()
    request.addEventListener('readystatechange', function () {
        if (this.readyState == 4 && this.status == 200) {
                questionData = JSON.parse(this.responseText)
                console.log(questionData)
                updateQuestionVariables()
                updateQuestionContainerContent()
                
        } 
    })
}


function updateQuestionVariables() {
    isRightAnswer = false
    trainId = questionData['train']['id']
    if (lang == 'en-ru') {
        questionWord = questionData['train']['word']['english']
        translates = []
        for (let translate in questionData['train']['word']['russian']) {
            translates.push(translate)
        }
    } else if (lang == 'ru-en') {
        const keys = Object.keys(questionData['train']['word']['russian'])
        questionWord = keys[Math.floor(Math.random()*keys.length)]
        translates = questionData['train']['word']['russian'][questionWord]
    }
}


function updateQuestionContainerContent() {
    HtmlObjWord.textContent = questionWord
    HtmlObjTranslateInput.value = ''
    HtmlObjLoadContainer.classList.add('hidden')
    HtmlObjQuestionContainer.classList.remove('hidden')
    HtmlObjResultContainer.classList.add('hidden')
}


function updateResultContainerContent() {
    document.querySelector('.question-word').textContent = questionWord
    document.querySelector('.translate-attempt').textContent = translateInput
    if (isRightAnswer == true) {
        document.querySelector('.verdict').textContent = 'Верно'
        document.querySelector('.verdict').classList.remove('wrong')
        document.querySelector('.verdict').classList.add('right')
        document.querySelector('.right-ans').textContent = ''
        let otherTranslates = translates.filter(translate => translate != translateInput)
        if (otherTranslates.length > 0) {
            document.querySelector('.other-translates').textContent = 'Другие переводы: ' + otherTranslates.join('; ') 
        }
    } else {
        const rightTranslate = translates.shift()
        document.querySelector('.verdict').textContent = 'Неверно'
        document.querySelector('.verdict').classList.remove('right')
        document.querySelector('.verdict').classList.add('wrong')
        document.querySelector('.right-ans').textContent = 'Правильный ответ - ' + translates.pop()
        if (translates.length > 0) {
            document.querySelector('.other-translates').textContent = 'Другие переводы: ' + translates.join('; ') 
        }
    }
}


function checkAnswer() {
    if (document.querySelector('.translate-input').value == '') {
        alert('Введите перевод')
    } else {
        translateInput = document.querySelector('.translate-input').value.trim().toLowerCase()
        if (translates.indexOf(translateInput) != -1) {
            isRightAnswer = true
        }
        updateResultContainerContent()
        sendIncreaseAnswerCounterRequest()
        HtmlObjQuestionContainer.classList.add('hidden')
        HtmlObjResultContainer.classList.remove('hidden')
    }

}


function sendIncreaseAnswerCounterRequest () {
    let path = `/words/trains/increase-attempt-counter/${trainId}/${isRightAnswer}/`
    request = new XMLHttpRequest()
    request.open("GET", path, true)
    request.send()
}



loadQuestion()

HtmlObjCheckButton.addEventListener('click', checkAnswer)
HtmlObjNextButton.addEventListener('click', function() {
    loadQuestion()
    HtmlObjQuestionContainer.classList.toggle('hidden')
    HtmlObjResultContainer.classList.toggle('hidden')
})

