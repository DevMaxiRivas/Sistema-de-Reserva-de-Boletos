const header = document.querySelector("header")


// Fijamos el Header
window.addEventListener("scroll", () => {
    header.classList.toggle("sticky", window.scrollY > 60)
})

let menu = document.querySelector("#menu-icon");
let navbar = document.querySelector(".navbar");

menu.onclick = () => {
    menu.classList.toggle("bx-x");
    navbar.classList.toggle("open");
}