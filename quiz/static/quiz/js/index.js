var allRadios = document.getElementsByName('choice');
var hiddenStatus = document.getElementById('hiddenstatus');
var statusBtn = document.getElementById('statusbtn');

function radioClick() {
var booRadio;
var x = 0;
for(x = 0; x < allRadios.length; x++){
	allRadios[x].onclick = function(){
	if(booRadio == this){
        
        this.checked = false;
         booRadio = null;
        //if not y green->red
        	toogleGreenToRed();
        }
    else{
    	//new option selcted
        booRadio = this;
        //if not y red->green
        toogleRedToGreen();
        } 
     };
}
}

function toogleGreenToRed()
{
	
	var hiddenStatus = document.getElementById('hiddenstatus');
	var statusBtn = document.getElementById('statusbtn');
	if(hiddenStatus.value != "yellow")
	{
		hiddenStatus.value = "red";
		statusBtn.style.backgroundColor = "red";
		console.log(hiddenStatus.value + " hidden")
	}
}

function toogleRedToGreen()
{

	var hiddenStatus = document.getElementById('hiddenstatus');
	var statusBtn = document.getElementById('statusbtn');

	
	if(hiddenStatus.value != 'yellow')
	{
		hiddenStatus.value = "green";
		statusBtn.style.backgroundColor = "#228B22";
		console.log(hiddenStatus.value + " hidden")
	}
}

//click on  stat btn
function changeStatus() {
	
	var hiddenStatus = document.getElementById('hiddenstatus');
	var statusBtn = document.getElementById('statusbtn');
	if(selectedRadio() != false)
	{
	//choice exist
	if(hiddenStatus.value == "yellow")
		{
			//marking on dobut
			hiddenStatus.value = "green";
			statusBtn.style.backgroundColor = "#228B22";
			statusBtn.innerHTML = "Flag";
		}
		else
		{
			hiddenStatus.value ="yellow";
			statusBtn.style.backgroundColor = "orange";
			statusBtn.innerHTML = "Unflag";
		}
	}
	else
	{
		//no choice exist
		if(hiddenStatus.value == "yellow")
		{
			hiddenStatus.value = "red";
			statusBtn.style.backgroundColor = "red";
			statusBtn.innerHTML = "Flag";
		}
		else
		{
			hiddenStatus.value = "yellow";
			statusBtn.style.backgroundColor = "orange";
			statusBtn.innerHTML = "Unflag";
		}

	}
	console.log(hiddenStatus.value + " hidden")
}

function selectedRadio()
{
	var allRadios = document.getElementsByName('choice');

	for (var i = 0; i < allRadios.length; i++)
	{
		if(allRadios[i].checked == true)
			return allRadios[i];
	}
	return false;

}

//to avoid triple click to deselect
function init() {
var hiddenStatus = document.getElementById('hiddenstatus');

	var selectedRadioBtn = selectedRadio();

	if(selectedRadioBtn != false)
	{
	doubleClick(selectedRadioBtn);
	doubleClick(selectedRadioBtn);
	}
	else
	{
		//no option exsit
		console.log("no option exist");
		var selectedRadioBtn = allRadios[0];
		//click 3 times
		doubleClick(selectedRadioBtn);
		selectedRadioBtn.click(selectedRadio);
		
	}
	console.log(hiddenStatus.value + " hidden in init ")
}

//helper funtion
function doubleClick(x)
{
	x.click();
	x.click();
}

function timer () {
	
	var x = document.getElementById('ms_timer');
	var min = document.getElementById('minrem');
	var sec = document.getElementById('secrem');
	min.value = x.textContent[0]+x.textContent[1];
	sec.value = x.textContent[3]+x.textContent[4];
	// console.log(min.value+" " + sec.value);
}

function checkInputStatus()
{
	inputBox = $('#inputbox')[0]
	if(inputBox.value == '')
	{
		toogleGreenToRed();
	}
	else
	{
		toogleRedToGreen();
	}
}