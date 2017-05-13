var allRadios = document.getElementsByName('choice');

function hi () {
var booRadio;
var st = document.getElementById('status');        	
var x = 0;
for(x = 0; x < allRadios.length; x++){
	allRadios[x].onclick = function(){
	if(booRadio == this){
        this.checked = false;
        booRadio = null;
        //if not y green->red
        tgR();
        }
    else{
        booRadio = this;
        //if not y red->green
        tgG();
        } 
     };
}
}

function tgR()
{
	var side = document.getElementById('side');
	var st = document.getElementById('status');
	var x = document.getElementById('dstat');
	if(st.value != "yellow")
	{
		st.value = "red";
		x.style.backgroundColor = "red";
		// side.style.backgroundColor = "red";
		console.log(st.value + " hidden")
	}
}

function tgG()
{
	 var side = document.getElementById('side');
	var st = document.getElementById('status');
	console.log(st.value);
	var x = document.getElementById('dstat');
	if(st.value != 'yellow')
	{
		st.value = "green";
		x.style.backgroundColor = "#228B22";
		// side.style.backgroundColor = "#228B22";
		console.log(st.value + " hidden")
	}
}


function curStat () {
	var st = document.getElementById('status');
	var x = document.getElementById('dstat');
	var side = document.getElementById('side');
	if(sel() != false)
	{
	//choice exist
	if(st.value == "yellow")
		{//marking on dobut
			st.value = "green";
			x.style.backgroundColor = "#228B22";
			x.innerHTML = "Flag";
			// side.style.backgroundColor = "#228B22";
		}
		else
		{
			st.value ="yellow";
			x.style.backgroundColor = "orange";
			x.innerHTML = "Unflag";
			// side.style.backgroundColor = "orange";
		}
	}
	else
	{
		//no choice exist
		if(st.value == "yellow")
		{
			st.value = "red";
			x.style.backgroundColor = "red";
			x.innerHTML = "Flag";
			// side.style.backgroundColor = "red";	
		}
		else
		{
			st.value = "yellow";
			x.style.backgroundColor = "orange";
			x.innerHTML = "Unflag";
			//side.style.backgroundColor = "orange";
		}

	}
	console.log(st.value + " hidden")
}

function sel()
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
	var st = document.getElementById('status');
	var x = sel();
	var y = document.getElementById('dstat');
	//console.log("init");
	if(x != false)
	{
	dob(x);
	dob(x);
	}
	else
	{
		//no option exsit
		console.log("no option exsit");
		var x = allRadios[0];
		dob(x);
		x.click();
		
	}
	console.log(st.value + "hidden")
}

function dob(x)
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
	console.log(min.value+" " + sec.value);
}