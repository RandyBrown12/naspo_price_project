function updateURLByPageSearch() {

    const url = new URL(window.location.href).origin;

    const vendor_name = document.getElementById("vendor_name").value;
    const description = document.getElementById("description").value;
    const manufacturer_part_number = document.getElementById("manufacturer_part_number").value;
    const list_price = document.getElementById("list_price").value;
    const naspo_price = document.getElementById("naspo_price").value;
    const page = document.getElementById("page_input").value;

    const searchMap = {
        "vendor_name": vendor_name,
        "description": description,
        "manufacturer_part_number": manufacturer_part_number,
        "list_price": list_price,
        "naspo_price": naspo_price,
        "page": page
    }

    const params = new URLSearchParams();
    
    for(let [element_name, element_value] of Object.entries(searchMap)) {
        if(element_name) {
            params.append(element_name, element_value);
        }
    }

    const fullUrl = `${url}?${params.toString()}`;

    window.location.href = fullUrl;
}

function updateURLByPageButton(page_number) {

    const url = new URL(window.location.href).origin;

    const vendor_name = document.getElementById("vendor_name").value;
    const description = document.getElementById("description").value;
    const manufacturer_part_number = document.getElementById("manufacturer_part_number").value;
    const list_price = document.getElementById("list_price").value;
    const naspo_price = document.getElementById("naspo_price").value;

    const searchMap = {
        "vendor_name": vendor_name,
        "description": description,
        "manufacturer_part_number": manufacturer_part_number,
        "list_price": list_price,
        "naspo_price": naspo_price,
        "page": page_number
    }

    if(isNaN(Number(page_number))) {
        throw new TypeError("Page Number is not a number")
    }

    const params = new URLSearchParams();
    
    for(let [element_name, element_value] of Object.entries(searchMap)) {
        if(element_name) {
            params.append(element_name, element_value);
        }
    }

    const fullUrl = `${url}?${params.toString()}`;

    window.location.href = fullUrl;
}