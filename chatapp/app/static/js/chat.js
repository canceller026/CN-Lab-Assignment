/*List friend*/
let person = [
    {
        id:01,
        name: "Gojo Satoru",
        avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQNhdbD8W2BUsdE3scIMBRjsbT13R4b86gmX3OEmYu8NsSWTkfPiCBB0vR9VR2j3SC71w&usqp=CAU",
        status: "Active 17 minutes ago"
    },
    {
        id:02,
        name: "Uzumaki Naruto",
        avatar: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9z5hgzxGR_PkmFy6mp9ohpJLdnuknkEEY1A&usqp=CAU",
        status: "Active"
    },
    {
        id:03,
        name: "Monkey .D. Luffy",
        avatar: "https://gamek.mediacdn.vn/133514250583805952/2022/5/18/photo-1-16528608926331302726659.jpg",
        status: "Active 2 hours ago"
    },  
];
/*Display list friend*/
function Chat(){
    for(let i = 0; i<=person.length; i++){
        document.getElementById("demo").innerHTML += `
            <div class="item" id="${person[i].id}">
                <img src=${person[i].avatar} alt="">
                <div class="contacto">
                    <div class="name">${person[i].name}</div>
                    <div class="status">${person[i].status}</div>
                </div>
            </div>
        
        `;
    };
}
Chat();