function updateURLByPageSearch() {

    const url_params = new URLSearchParams(window.location.search);

    const vendor_name = document.getElementById("vendor_name").value;
    const description = document.getElementById("description").value;
    const manufacturer_part_number = document.getElementById("manufacturer_part_number").value;
    const list_price = document.getElementById("list_price").value;
    const naspo_price = document.getElementById("naspo_price").value;
    const page = document.getElementById("page_input").value;
    const sort_direction = url_params.get("sort_direction");
    const sort_value = url_params.get("sort_value");

    const searchMap = {
        "vendor_name": vendor_name,
        "description": description,
        "manufacturer_part_number": manufacturer_part_number,
        "list_price": list_price,
        "naspo_price": naspo_price,
        "page": page,
        "sort_value": sort_value,
        "sort_direction": sort_direction
    }

    window.location.href = buildFullURL(searchMap);
}

function updateURLByPageButton(page_number) {

    const url_params = new URLSearchParams(window.location.search);

    const vendor_name = document.getElementById("vendor_name").value;
    const description = document.getElementById("description").value;
    const manufacturer_part_number = document.getElementById("manufacturer_part_number").value;
    const list_price = document.getElementById("list_price").value;
    const naspo_price = document.getElementById("naspo_price").value;
    const sort_direction = url_params.get("sort_direction");
    const sort_value = url_params.get("sort_value");

    const searchMap = {
        "vendor_name": vendor_name,
        "description": description,
        "manufacturer_part_number": manufacturer_part_number,
        "list_price": list_price,
        "naspo_price": naspo_price,
        "page": page_number,
        "sort_value": sort_value,
        "sort_direction": sort_direction
    }

    if(isNaN(Number(page_number))) {
        throw new TypeError("Page Number is not a number")
    }

    window.location.href = buildFullURL(searchMap);
}

function sortURLByName(column_name) {

    const url_params = new URLSearchParams(window.location.search);

    const vendor_name = document.getElementById("vendor_name").value;
    const description = document.getElementById("description").value;
    const manufacturer_part_number = document.getElementById("manufacturer_part_number").value;
    const list_price = document.getElementById("list_price").value;
    const naspo_price = document.getElementById("naspo_price").value;
    let sort_direction = url_params.get("sort_direction");
    const url_sort_value = url_params.get("sort_value");
    const page = document.getElementById("page_input").value;

    if(sort_direction === null || sort_direction === "desc") {
        sort_direction = "asc"
    } else if(column_name != url_sort_value) {
        sort_direction = "asc"
    } else {
        sort_direction = "desc"
    }

    const searchMap = {
        "vendor_name": vendor_name,
        "description": description,
        "manufacturer_part_number": manufacturer_part_number,
        "list_price": list_price,
        "naspo_price": naspo_price,
        "page": page,
        "sort_value": column_name,
        "sort_direction": sort_direction
    }

    window.location.href = buildFullURL(searchMap);
}

function buildFullURL(searchMap) {
    const url = new URL(window.location.href).origin;
    const params = new URLSearchParams();
    
    for(let [element_name, element_value] of Object.entries(searchMap)) {
        if(element_name && element_value) {
            params.append(element_name, element_value);
        }
    }

    const fullUrl = `${url}?${params.toString()}`;
    return fullUrl;
}