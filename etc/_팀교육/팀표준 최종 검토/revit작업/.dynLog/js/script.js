
function hideAllPages() {
        document.querySelector("#home").style.fontWeight = "normal";
        document.querySelector("#homePage").style.display = "None";
        document.querySelector("#info").style.fontWeight = "normal";
        document.querySelector("#infoPage").style.display = "None";
        document.querySelector("#famType").style.fontWeight = "normal";
        document.querySelector("#famTypePage").style.display = "None";
        document.querySelector("#roomInfo").style.fontWeight = "normal";
        document.querySelector("#roomInfoPage").style.display = "None";
}

document.querySelector("#cat").onclick = function() {
	    let img = document.createElement("img");
	    img.setAttribute("src", "https://t4.ftcdn.net/jpg/05/62/99/31/360_F_562993122_e7pGkeY8yMfXJcRmclsoIjtOoVDDgIlh.jpg");
	    document.querySelector("#cat").style.display = "None";
	    img.setAttribute("style", "width:300px;margin-top:20px;")
	    document.body.append(img);
	};
document.querySelector("#home").onclick = function() {
        hideAllPages();
        document.querySelector("#home").style.fontWeight = "bolder";
        document.querySelector("#homePage").style.display = "inline";
	};
document.querySelector("#info").onclick = function() {
        hideAllPages();
        document.querySelector("#info").style.fontWeight = "bolder";
        document.querySelector("#infoPage").style.display = "inline";
	};
document.querySelector("#famType").onclick = function() {
        hideAllPages();
        document.querySelector("#famType").style.fontWeight = "bolder";
        document.querySelector("#famTypePage").style.display = "inline";
	};
document.querySelector("#roomInfo").onclick = function() {
        hideAllPages();
        document.querySelector("#roomInfo").style.fontWeight = "bolder";
        document.querySelector("#roomInfoPage").style.display = "inline";
	};
	
