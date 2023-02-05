const maleButton = document.querySelector("#id_gender_0")
const femaleButton = document.querySelector("#id_gender_1")
const form = document.querySelector("#form")

function submitForm(e) {
  form.submit()
}

console.log(maleButton && femaleButton)

if (maleButton && femaleButton) {
  femaleButton.addEventListener("click", submitForm);
  maleButton.addEventListener("click", submitForm)
}
