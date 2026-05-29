function confirmDelete() {
    return confirm("Are you sure?");
}

function validateForm() {

    let product =
    document.getElementById("product_name").value;

    let quantity =
    document.getElementById("quantity").value;

    let price =
    document.getElementById("price").value;

    if(product == "" || quantity == "" || price == "") {

        alert("Please fill all fields");

        return false;
    }

    return true;
}

function togglePassword(id, icon) {

    let input = document.getElementById(id);

    if(input.type === "password") {

        input.type = "text";

        icon.classList.remove("fa-eye");

        icon.classList.add("fa-eye-slash");

    } else {

        input.type = "password";

        icon.classList.remove("fa-eye-slash");

        icon.classList.add("fa-eye");
    }
}

document.addEventListener("DOMContentLoaded", function(){

    let searchInput =
    document.getElementById("searchInput");

    if(searchInput){

        searchInput.addEventListener("keyup", function(){

            let filter =
            searchInput.value.toLowerCase();

            let rows =
            document.querySelectorAll("#productTable tbody tr");

            rows.forEach(function(row){

                let text =
                row.textContent.toLowerCase();

                if(text.includes(filter)){

                    row.style.display = "";

                } else {

                    row.style.display = "none";
                }

            });

        });

    }

});