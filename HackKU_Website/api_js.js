//document.addEventListener('load', makeObjs, false);
document.getElementById("getdata").addEventListener('click', getData, false);

var myTeam = [];

function assembleTeam() {

    document.getElementById("teamTXT").innerHTML = "Your team:";
    document.getElementById("getdata").value = "Re-roll your team!";

    for (var i = 0; i < 6; i++) {

        var poke = document.createElement("Object");

        poke.name = myTeam[i].name;
        poke.src = myTeam[i].sprites.front_default;

        document.getElementById("teamn" + i).innerHTML = poke.name;
        document.getElementById("teami" + i).src = poke.src;
    }

    //poke1.style.boarder = "5px solid red";
    //poke1.style.width = "900px";

}


//Application Programming Interface
function getData() {
    myTeam = [];
    var randomNum;

    var requestObj = new XMLHttpRequest();
    randomNum = Math.round(Math.floor(Math.random() * 891 + 1));
    requestObj.addEventListener('load', stickInArray, false);
    requestObj.open("GET", "https://localhost:5000/api/");
    console.log(requestObj);
    requestObj.send();


    function stickInArray(e) {
        console.log(myTeam);
        myTeam.push(JSON.parse(e.currentTarget.response));
        if (myTeam.length == 6) { assembleTeam(); }
    }
}


// curl http://localhost:5000/api