//console.log('Hello Tekin')
const url = window.location.href
//console.log(url)
window['example'] = null;
const quizBox = document.getElementById('quiz-box')
const resultBox = document.getElementById('result-box')
const scoreBox = document.getElementById('score-box')
// let data

$.ajax({
  type: 'GET',
  url: `${url}data`,
  success: function(response){
    const data = response.data

    data.forEach(function (el, i) {
      for(const [question, values] of Object.entries(el)){
        quizBox.innerHTML += `
            <hr>
            <div class="mb-2">
              <b>${i+1}. ${question}</b>
             </div>
        `

        values[0].forEach(el => {
            for (const [key, value] of Object.entries(el)) {
//              console.log("Key: ",key);
//              console.log("Value: ", value);
              if(question == key && value != 0) {
                   quizBox.innerHTML += `
                       <hr>
                       <div class="mb-2">
                         <img src=${value} width="360px;" height="220px;"/>
                       </div>
                   `
            }
            }

        }
        )

        values[1].forEach(answer=>{
                  quizBox.innerHTML += `
                  <div>
                    <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for="${question}">${answer}</label>
                  </div>
                  `
                })
      }
    })

  },
  error: function(error){
    console.log(error)
  }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
     const elements = [...document.getElementsByClassName('ans')]
     const data ={}
     data['csrfmiddlewaretoken'] = csrf[0].value
     elements.forEach(el=>{
         if(el.checked){
             data[el.name] = el.value
         } else{
             if(!data[el.name]){
                 data[el.name] = null
             }
         }
     })

     $.ajax({
         type: 'POST',
         url: `${url}save/`,
         data: data,
         success: function(response){
            console.log(response)
//            console.log(response)
            const results = response.results
            console.log(results)
            quizForm.classList.add('not-visible')
            scoreBox.innerHTML += `Nəticə ${response.score}% ! <p></p>`
            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for(const [question, resp] of Object.entries(res)){
//                    console.log(question)
//                    console.log(resp)
//                    console.log('********')
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)
                    const correct = resp['correct_answer']
                    if(resp == 'not answered'){
                        resDiv.innerHTML += `<p></p> <i>* Cavab verilməyib`
                        resDiv.classList.add('bg-warning')
                    }
                    else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if(answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` <p></p> <i>* Doğru cavab: ${answer} </i>`
                        }
                        else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` <p></p> <i>* Doğru cavab: ${correct} </i> <p></p>`
                            resDiv.innerHTML += ` <i>* Verilmiş cavab: ${answer} </i>`
                        }
                    }
               }
//                const body = document.getElementsByTagName('BODY')[0]
//                body.append(resDiv)
              resultBox.append(resDiv)
            })
         },
         error: function(error){
             console.log(error)
         }
     })
 }

quizForm.addEventListener('submit', e=>{
     e.preventDefault()
     sendData()
 })








