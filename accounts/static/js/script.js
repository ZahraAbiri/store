let card ;

function login_signUp()
{
    document.getElementById("signUp").addEventListener("submit", function(event){
        card.style.transform = 'rotateY(0deg)';
        event.preventDefault();
    });

    card = document.getElementById('card');
}


function flip()
{
    card.style.transform = 'rotateY(180deg)';
}

function openLogin()
{
    window.open('login.html','_self')
}