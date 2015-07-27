// // this is the code to create the runTimer() function
//
//  $(document).ready(function(){
//
//   // function createTimer(){
//   //   var today = new Date()
//   //   var getTodaysDate = str(today.getDate())
//   //   document.getElementById('timer').innerHTML = getTodaysDate
//   // }
//
//   $("#timer").show(function(){
//     var today = new Date();
//     var getTodaysDate = str(today.getDate());
//     document.getElementById('timer').innerHTML = getTodaysDate;
//   })
//
// //  $(.body).append(createTimer());
//
// });


// console.log("beginning")

function startTime() {
    //create new date object
    var today=new Date()
    //get integer values for current time
    var hour=today.getHours()
    var min=today.getMinutes()
    var sec=today.getSeconds()
    // min = checkTime(min)
    // sec = checkTime(sec)
    todayArray = []
    todayArray[0] = hour
    todayArray[1] = min
    todayArray[2] = sec
    //this line posts code to the webpage
  //  document.getElementById('timer').innerHTML = h+":"+m+":"+s;
    //this line updates the code on the webpage
  //  var t = setTimeout(function(){startTime()},500);
    return todayArray
}

// function checkTime(i) {
//     if (i<10) {i = "0" + i}
//     return parseInt(i)
// }

// console.log(startTime())

function endTime(startTime, userDur){
  timeArray = []
  timeArray[0] = startTime
  endTime = startTime
  console.log("Duration: ",userDur)
  showStartTime(timeArray[0])

  if (userDur > 60){
    console.log("over one hour")

    timeArray[1] = endTime
  }
  else if (userDur == 60){
    console.log("one hour")
    endTime[0] = startTime[0]+1
    timeArray[1] = endTime
  }
  else {
    console.log("under one hour")

    timeArray[1] = endTime
  }
  showEndTime(timeArray[1])
}

$("#enterButton").click(function(){
  var userTime = $('#timeInterval').val()
  startingTime = startTime()
  endTime(startingTime, userTime)
})


function showStartTime(currentTimer){
  document.getElementById('startTime').innerHTML = currentTimer[0]+":"+currentTimer[1]+":"+currentTimer[2];
}
function showEndTime(currentTimer){
  document.getElementById('endTime').innerHTML = currentTimer[0]+":"+currentTimer[1]+":"+currentTimer[2];
}
