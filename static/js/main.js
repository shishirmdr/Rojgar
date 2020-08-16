function show() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

let validate_for_available=()=>{
	let x = document.forms["workprofile"];
	let y = x["available_for_hire"].checked;
	let error = document.getElementById("e_message");

	let z = x["username"].value;
	if (z==""){
		return false;
	}

	if (y==true){
		let z = x["first_name"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter Your First Name.");
			return false;
		}

		z = x["last_name"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter Your Last Name.");
			return false;
		}

		z = x["occupation"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter Your Occupation.");
			return false;
		}


		z = x["education"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter Your Education Level or any Extra class.");
			return false;
		}

		z = x["skills"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter list of your skills.");
			return false;
		}

		z = x["description"].value;
		if (z==""){
			error.innerHTML = errormessage("Enter a small description about yourself.");
			return false;
		}
	}
}

let errormessage = (a) =>{
	return `
		<div class="alert alert-danger" role="alert">
			${a}
		</div>`;
}