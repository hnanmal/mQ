

function hideAllPages() {
        document.querySelector("#home").style.fontWeight = "normal";
        document.querySelector("#homePage").style.display = "None";
        document.querySelector("#info").style.fontWeight = "normal";
        document.querySelector("#infoPage").style.display = "None";
        document.querySelector("#famType").style.fontWeight = "normal";
        document.querySelector("#famTypePage").style.display = "None";
        document.querySelector("#roomInfo").style.fontWeight = "normal";
        document.querySelector("#roomInfoPage").style.display = "None";
        document.querySelector("#roomInfoPage_chk").style.display = "None";
}

document.querySelector("#cute").onclick = function() {
	    let img = document.createElement("img");
	    
	    img.setAttribute("src", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8DcTzTMtsaI7YOpQt52y8gLsDqWFKdfH46_TI2v5Z2A&s");
	    document.querySelector("#cute").style.display = "None";
	    img.setAttribute("style", "width:500px;margin-top:20px;");
	    
	    //document.body.append(img);
	    const place = document.querySelector("#mainImg");
	    place.append(img);
	    
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
document.querySelector("#roomInfo_chk").onclick = function() {
        hideAllPages();
        document.querySelector("#roomInfo_chk").style.fontWeight = "bolder";
        document.querySelector("#roomInfoPage_chk").style.display = "inline";
	};
	
