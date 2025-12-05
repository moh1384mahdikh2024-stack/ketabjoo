const circle = document.getElementById("circle");
const dot = document.getElementById("dot");

let mouseX = 0, mouseY = 0;
let circleX = 0, circleY = 0;
let dotX = 0, dotY = 0;
const radius = 25; // فاصله مجاز نقطه از مرکز (تا خارج نشود)

document.addEventListener("mousemove", e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

function animate() {

    // دایره نرم دنبال موس
    circleX += (mouseX - circleX) * 0.32;
    circleY += (mouseY - circleY) * 0.22;
    circle.style.left = circleX + "px";
    circle.style.top = circleY + "px";

    // 🟡 موقعیت نقطه نسبت به مرکز دایره
    dotX += (mouseX - circleX - dotX - 4) * 0.5
    dotY += (mouseY - circleY - dotY - 4) * 0.5


    // جلوگیری از خروج نقطه بیرون دایره
    const dist = Math.sqrt(dotX * dotX + dotY * dotY)
    if (dist > radius) {
        dotX = (dotX / dist) * radius
        dotY = (dotY / dist) * radius
    }

    dot.style.transform = `translate(${dotX}px , ${dotY}px)`;

    requestAnimationFrame(animate);
}

animate();

document.querySelectorAll("a, button, [role='button'], .clickable")
    .forEach(el => {
        el.addEventListener("mouseenter", () => {
            document.body.classList.add("cursor-hover")
        })
        el.addEventListener("mouseleave", () => {
            document.body.classList.remove("cursor-hover")
        })
    })

document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.auto-dismiss');
    alerts.forEach((alert) => {
        setTimeout(() => {
            // اضافه کردن کلاس fade-out
            alert.classList.remove("show");
            alert.classList.add("hide");

            // حذف کامل بعد از انیمیشن
            setTimeout(() => {
                alert.remove();
            }, 150);
        }, 6000); // 3 ثانیه
    });
});


 // گرفتن مسیر URL فعلی
    const currentPath = window.location.pathname;

    // گرفتن تمام لینک‌های داخل navbar
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    navLinks.forEach(link => {
        // اگر href لینک داخل مسیر فعلی بود → active شود
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
    // گرفتن مسیر URL فعلی
    const currentPathDashboard = window.location.pathname;

    // گرفتن تمام لینک‌های داخل navbar
    const navLinksDashboard = document.querySelectorAll(".nav-hover-banafsh");

    navLinksDashboard.forEach(link => {
        // اگر href لینک داخل مسیر فعلی بود → active شود
        if (link.getAttribute("href") === currentPathDashboard) {
            link.classList.add("active-banafsh");
        }
    });