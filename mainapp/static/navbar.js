const navEl = document.querySelector('.nav');
const hamburgerEl = document.querySelector('.hamburger');
hamburgerEl.addEventListener("click",()=>{
    navEl.classList.toggle("nav--open");
    hamburgerEl.classList.toggle('hamburger--open');
});
document.querySelector('.nav a').addEventListener("click",()=>{
    navEl.classList.remove("nav--open");
    hamburgerEl.classList.remove("hamburger--open");
});

$(".upl_btn").click(function(){
    $(".popup-change-bg").removeClass("hidden");
  });
$(".close_input_btn").click(function(){
    $(".popup-change-bg").addClass("hidden");
  });