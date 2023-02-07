const maleButton = document.querySelector("#id_gender_0")
const femaleButton = document.querySelector("#id_gender_1")
const symptomInput = document.querySelector("#id_symptom")
const form = document.querySelector("#form")
const suggestions = document.querySelector(".suggestions")


function submitForm(e) {
  form.submit()
}


const symptoms = []
fetch('/assessment/get-symptoms')
  .then(res => res.json())
  .then(data => symptoms.push(...data))
  .catch(err => console.log(err))


function findMatches(wordToMatch, symptoms) {
  console.log(wordToMatch)
  return wordToMatch.length > 2 ? symptoms.filter(symptom => {
    const regex = new RegExp(wordToMatch, 'gi');
    return symptom.Name.match(regex)
  }) : [];
}

function displayMatches() {
  const matchArray = findMatches(this.value, symptoms);
  const html = matchArray.map(symptom => {
    const regex = new RegExp(this.value, 'gi');
    const symptomName = symptom.Name.replace(regex, `<span class="hl">${this.value}</span>`);
    return `
      <li >
        <a href="/assessment/issues/${symptom.ID}/${symptomInput.dataset.pronoun}"><span class="name">${symptomName}</span></a>
      </li >
    `;
  }).join('');
  html ? suggestions.innerHTML = html :
    suggestions.innerHTML = `
    <li>
      <span class="nf">Symptom not found</span>
    </li>
  `
    ;
}


console.log(symptoms)
console.log(symptomInput)

if (maleButton && femaleButton) {
  femaleButton.addEventListener("click", submitForm);
  maleButton.addEventListener("click", submitForm)
}

if (symptomInput) {
  symptomInput.addEventListener("change", displayMatches)
  symptomInput.addEventListener("keyup", displayMatches)
}
