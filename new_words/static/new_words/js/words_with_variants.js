const HtmlObjNextButton = document.querySelector('.next-btn')
const HtmlObjMarkAsStudiedBtn = document.querySelector('.mark-as-studied-btn')
const HtmlObjReturnToStudyBtn = document.querySelector('.return-to-study-btn')
let HtmlObjVariantsDiv = document.querySelector('.variants')
let HtmlObjLoadContainer = document.querySelector('.container.load')
let HtmlObjQuestionContainer = document.querySelector('.container.question')
let HtmlObjWordDiv = document.querySelector('.word')
let HtmlObjVariantButtons = null

const params = new URLSearchParams(window.location.href)
const mode = params.get('mode')
const lang = params.get('lang')

let questionData = null
let variantsData = null
let wordEn = ''
let wordRu = ''
let variantsList = []
let isAnswered = false
let request = new XMLHttpRequest()


main()
function main() {
    loadQuestion()

    HtmlObjNextButton.addEventListener('click', function() {
        if (isAnswered == true) {
            HtmlObjLoadContainer.classList.remove('hidden')
            HtmlObjQuestionContainer.classList.add('hidden')
            loadQuestion()
        }
    })

    HtmlObjMarkAsStudiedBtn.addEventListener('click', change_train_status_request)
    HtmlObjReturnToStudyBtn.addEventListener('click', change_train_status_request)

}


function loadQuestion() {
    request = new XMLHttpRequest()
    request.open("GET", "/words/api/train-object/?&mode="+mode, true)
    request.send()
    request.addEventListener('readystatechange', function () {
        if (this.readyState == 4 && this.status == 200) {
                questionData = JSON.parse(this.responseText)
                loadVariants()       
        } 
    })
}


function loadVariants() {
    wordEn = questionData['train']['word']['english']
    const keys = Object.keys(questionData['train']['word']['russian'])
    wordRu = keys[Math.floor(Math.random()*keys.length)]

    request = new XMLHttpRequest()
    request.open("GET", `/words/api/get-variants/3/?&en=${wordEn}&ru=${wordRu}`, true)
    request.send()
    request.addEventListener('readystatechange', function () {
        if (this.readyState == 4 && this.status == 200) {
                variantsData = JSON.parse(this.responseText)
                createVariantsList()
                updateQuestionContainerContent()                
        } 
    })
}


function createVariantsList() {
    variantsList = []
    if (lang == 'en-ru') {
        variantsList.push(wordRu)
        for (let variant of variantsData['variants']['ru']) {
            variantsList.push(variant)
        }
    } else if (lang == 'ru-en') {
        variantsList.push(wordEn)
        for (let variant of variantsData['variants']['en']) {
            variantsList.push(variant)
        }
    }
    variantsList = shuffle(variantsList)
}


function shuffle(arr){
	var j, temp;
	for(var i = arr.length - 1; i > 0; i--){
		j = Math.floor(Math.random()*(i + 1));
		temp = arr[j];
		arr[j] = arr[i];
		arr[i] = temp;
	}
	return arr;
}


function updateQuestionContainerContent() {
    isAnswered = false
    HtmlObjVariantsDiv.textContent = ''

    if (mode == 'study') {
        HtmlObjMarkAsStudiedBtn.classList.remove('hidden')
        HtmlObjReturnToStudyBtn.classList.add('hidden')
    } else if (mode == 'repeat') {
        HtmlObjMarkAsStudiedBtn.classList.add('hidden')
        HtmlObjReturnToStudyBtn.classList.remove('hidden')
    }

    if (lang == 'ru-en') {
        HtmlObjWordDiv.textContent = wordRu[0].toUpperCase() + wordRu.slice(1)
    } else if (lang == 'en-ru') {
        HtmlObjWordDiv.textContent = wordEn[0].toUpperCase() + wordEn.slice(1)
    }


    for (let variant of variantsList) {
        let variantDiv = document.createElement('div')
        variantDiv.className = 'variant'
        variantDiv.textContent = variant
        HtmlObjVariantsDiv.append(variantDiv)
    }
    HtmlObjLoadContainer.classList.add('hidden')
    HtmlObjQuestionContainer.classList.remove('hidden')

    HtmlObjVariantButtons = document.querySelectorAll('.variant')
    addEventListenersForVariantsButtons()
}


function addEventListenersForVariantsButtons() {
    HtmlObjVariantButtons.forEach(element => {
        element.addEventListener('click', function() {
            if (isAnswered == false) {
                if (element.textContent == wordRu && lang == 'en-ru' || element.textContent == wordEn && lang == 'ru-en') {
                    element.style.backgroundColor = 'rgba(0, 255, 0, 0.6)'
                    sendIncreaseAnswerCounterRequest(true)
                } else {
                    element.style.backgroundColor = 'rgba(255, 0, 0, 0.5)'
                    showRightAnswer()
                    sendIncreaseAnswerCounterRequest(false)
                }
                isAnswered = true
            }
        })
    })
}


function showRightAnswer() {
    HtmlObjVariantButtons.forEach(element => {
        if (element.textContent == wordRu && lang == 'en-ru' || element.textContent == wordEn && lang == 'ru-en') {
            element.style.backgroundColor = 'rgba(0, 255, 0, 0.6)'
        }
    })
}


function change_train_status_request() {
    let href = '/words/trains/change-status/' + questionData['train']['id'] + '/'
    let ajax = new XMLHttpRequest()
    ajax.open('GET', href, true)
    ajax.send()
    ajax.addEventListener('readystatechange', function () {
        if (this.readyState == 4 && this.status == 201) {
            HtmlObjMarkAsStudiedBtn.classList.toggle('hidden')
            HtmlObjReturnToStudyBtn.classList.toggle('hidden')
        }
    })
}


function sendIncreaseAnswerCounterRequest (isRightAnswer) {
    let path = `/words/trains/increase-attempt-counter/${questionData['train']['id']}/${isRightAnswer}/`
    let increaseAnswerCounterRequest = new XMLHttpRequest()
    increaseAnswerCounterRequest.open("GET", path, true)
    increaseAnswerCounterRequest.send()
    console.log('increase')
}


