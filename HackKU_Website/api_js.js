console.log("running")

let button = document.getElementById("mybutton")

button.addEventListener("click", do_operation, false)

function do_operation() {
    let a = "hello world"
    console.log(a)

    let obj = document.getElementById("test")
    obj.innerHTML = a;
    // console.log(a)
}

