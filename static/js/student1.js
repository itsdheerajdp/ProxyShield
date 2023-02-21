names = document.querySelector("#studentName").innerHTML;
roll_no = document.querySelector("#studentID").innerHTML;
progress1 = document.querySelector("#studentProgress").innerHTML;
var user = {
    name: names,
    image: "data:image/jpeg;base64,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",
    progress: progress1
}

var courseArr = [{
        title: "Memory Management",
        subject: "COA"
    }, {
        title: "SQL",
        subject: "DBMS"
    }, {
        title: "DFA",
        subject: "TOC"
    }];

var activityArr = [{
        title: "Completed COA  Module 1 Quiz1",
        subject: "Submitted for review 11/02/2023 at 10:00PM"
    }, {
        title: "Commented SQL code Tuesday Discussion Group",
        subject: "Who wants to grab coffee to talk."
    }, {
        title: "Enrolled in all CSE courses",
        subject: "Course begins 11/02/2023"
    }];

var accountArr = [{
        title: "Enrolled since: ",
        subject: "09/12/2021"
    }, {
        title: "Enrollment Status: ",
        subject: "Active Student"
    }, {
        title: "Department",
        subject: "Computer Science"
    }];

function userDetails(user, image, name, id){
image.src = user.image;
name.innerText = user.name;
id.innerText = "Roll_No: "+ roll_no;
}

userDetails(user,document.getElementById("studentImage"), document.getElementById("studentName"), document.getElementById("studentID"));

function leadingZero(number) {
if (number < 10) {
return "0" + number;
} else {
return number;
}
}

function displayDate(){
var myDate = new Date();


var currentSs=leadingZero(myDate.getSeconds());
var currentHr=leadingZero(myDate.getHours());
if (currentHr>12){
    currentHr=currentHr-12;
}
if (currentHr<12){
    currentSs=currentSs+" pm";
}else{
    currentSs=currentSs+" am";
}


var currentMin=leadingZero(myDate.getMinutes());
var currentYear=myDate.getFullYear();
var currentMonth=leadingZero(myDate.getMonth()+1);
var currentDay=leadingZero(myDate.getDate());


var displayArea=document.getElementById("displayTime");
    displayArea.innerHTML=currentHr+":"+currentMin+":"+currentSs +" | "+ currentDay+"/"+currentMonth+"/"+currentYear;

setTimeout(function() {
displayDate();
}, 1000)
}
displayDate();

function studentProgress(user, progress){
progress.innerText = user.progress+"%";
progress.style.width = user.progress+"%";
}

studentProgress(user, document.getElementById("studentProgress"),(document.getElementById("studentProgress")));


function currentTab(array, title, list, string){
title.innerText=string;
list.innerHTML="";
for(var i=0; i<array.length; i++){
    list.innerHTML+="<li><h6>"+array[i].title+ "</h6><p>"+ array[i].subject+ "</p></li>"
}
}

function courses(){
currentTab(courseArr, document.getElementById("title"), document.getElementById("list"), "My Courses:")
}

function activity(){
currentTab(activityArr, document.getElementById("title"), document.getElementById("list"), "My Recent Activity:")
}

function account() {
currentTab(accountArr, document.getElementById("title"), document.getElementById("list"), "My Account:")
}

function menu(){
document.getElementById("menu").classList.toggle("menuExpand");
document.getElementById("home").classList.toggle("whiteText");
document.getElementById("logOut").classList.toggle("whiteText");
}

courses();