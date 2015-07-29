/*
* the startTime() function returns the time associated with the
* start of the function (when the user hits the enter button)
*
* precondition: the function is called once the button is clicked
* postcondition: the starting time is returned in array format
*/
function startTime() {
    //create new date object
    var today=new Date()
    //get integer values for current time
    var hour=today.getHours()
    var min=today.getMinutes()
    var sec=today.getSeconds()
    todayArray = []
    todayArray[0] = parseInt(hour)
    todayArray[1] = parseInt(min)
    todayArray[2] = parseInt(sec)
    //this line posts code to the webpage
  //  document.getElementById('timer').innerHTML = h+":"+m+":"+s;
    //this line updates the code on the webpage
  //  var t = setTimeout(function(){startTime()},500);
    return todayArray
}


/*
* the runTimer() function uses array representation of the ending time to create a
* countdown clock
*
* precondition: the correct end time is passed
* postcondition: a countdown clock is displayed
*/
function runTimer(endTime){
    timeLeft = []
    currentTime = startTime()
    clockVar = setInterval(function(){
      currentTime = startTime()
      document.getElementById('clock').innerHTML = currentTime[0]+":"+currentTime[1]+":"+currentTime[2]

      //find time remaining
      for (i=2; i > -1; i--){
        if (endTime[i] < currentTime[i]){
          timeLeft[i] = (60 + endTime[i]) - currentTime[i]
          currentTime[i-1] += 1
        }
        else {
          timeLeft[i] = endTime[i] - currentTime[i]
        }
      }
      document.getElementById('timer').innerHTML = timeLeft[0]+":"+timeLeft[1]+":"+timeLeft[2]


      //stopping function: if current time matches ending time
      if (currentTime[1] == endTime[1]){
        if (currentTime[0]==endTime[0] && currentTime[2]==endTime[2]){
          //userAlert
          alert("Time's Up!! \n\n You should move on now")
          clearInterval(clockVar)
          console.log(" enter clear")
        }

      }
    },1000)
}
