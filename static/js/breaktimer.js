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
* the endTime() function takes the start time and duration and returns an array
* that includes the startTime array and the endTime array
*
* precondition: the passed startTime array accurately reflects the initail starting time
*               the userDur accurately reflects the intended duration
* postcondition: an array of the two time arrays (start and end arrays) is returned
* postcondition2: an array of only the ending time is returned (CURRENT VERSION)
*/
function endTime(userDur){
  starting = startTime()
  userDur = parseInt(userDur)
  timeArray = []
  timeArray[0] = starting
  endTime = starting
  console.log("Duration: ",userDur)
  showStartTime(timeArray[0])

  //the desired duration is over one hour
  if (userDur > 60){
    hours = (userDur - userDur%60)/60
    endTime[0] += hours
    if((endTime[1] + (userDur%60)) > 60 || (endTime[1] + (userDur%60)) == 60){
      //roll over needed
      endTime[0] += 1
      endTime[1] = (endTime[1]+(userDur%60))-60
    }
    else{
      endTime[1] += (userDur%60)
    }

    timeArray[1] = endTime
  }
  //the desired duration is exactly one hour
  else if (userDur == 60){
    endTime[0] += 1
    timeArray[1] = endTime
  }
  //the desired duration is under one hour
  else {
    if( (endTime[1]+userDur) > 60 || (endTime[1]+userDur) == 60){
      //roll over needed
      endTime[0] += 1
      endTime[1] = (endTime[1]+(userDur%60))-60
    }
    else{
      endTime[1] += userDur
    }
    timeArray[1] = endTime
  }
  showEndTime(timeArray[1])
  // return timeArray[1]



  runTimer(timeArray[1])
  updateEndTime(timeArray[1])



}

/*
* the updateEndTime() function uses ajax to submit the current endTime
* to the python handler that will update the datastore information
*
* precondition: the passed endTime array is accurate
* postcondition: the data of the endtime array is passed to the handler
*/
function updateEndTime(endTime){
  $.ajax({
    type: "POST",
    url: "/logEndTime",
    dataType: 'json',
    data: JSON.stringify({
      "hours": endTime[0],
      "minutes": endTime[1],
      "seconds": endTime[2],
      "status": 'breaking'
    })
  })
}



/* OBSOLETE
* this JQuery function is now obsolete
*
* this JQuery function responds to a button click and calls the startTime() function
* and the endTime() function
*
* precondition: the button is clicked
* postcondition: the different time functions are called in order to initiate the timer
*/
$("#enterButton").click(function(){
  var userTime = $('#timeInterval').val()
  startingTime = startTime()
  endArray = endTime(startingTime, userTime)
  runTimer(endArray)
})

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
          clearInterval(clockVar)
          console.log(" enter clear")
        }

      }
    },1000)
}





function showStartTime(currentTimer){
  document.getElementById('startTime').innerHTML = currentTimer[0]+":"+currentTimer[1]+":"+currentTimer[2];
}
function showEndTime(currentTimer){
  document.getElementById('endTime').innerHTML = currentTimer[0]+":"+currentTimer[1]+":"+currentTimer[2];
}
