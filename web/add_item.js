
async function addItem() {
    body = document.body
    form = document.createElement("form");
    //form.onsubmit = "sender()";
    form.method = "post"
    form.id = "forma"
    form.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("button").click();
        }
    });
    
    //Name input
    name_label = document.createElement("label");
    name_label.htmlFor = "name"
    name_label.innerHTML = "Item name<br/>";
    item_name = document.createElement("input");
    item_name.type = "text"
    item_name.name = "name"
    item_name.id = "name"
    form.appendChild(name_label);
    form.appendChild(item_name);
    form.appendChild(document.createElement("BR"));

    //Category input
    category_label = document.createElement("label");
    category_label.htmlFor = "category"
    category_label.innerHTML = "Category<br/>";

    const category_response = await fetch("http://localhost:8000/category/", {
        method: "GET",
        }
    );
    const categories = await category_response.json();
    category = document.createElement("select");
    category.name = "category"
    category.id = "category"
    for (let x in categories){
        one_category = document.createElement("option");
        one_category.value = categories[x]["name"]
        one_category.innerHTML = categories[x]["name"]
        category.appendChild(one_category);
    }
    form.appendChild(category_label);
    form.appendChild(category);
    form.appendChild(document.createElement("BR"));

    //Price input
    price_label = document.createElement("label");
    price_label.htmlFor = "price"
    price_label.innerHTML = "Base price<br/>";
    price = document.createElement("input");
    price.type = "text"
    price.name = "price"
    price.id = "price"
    form.appendChild(price_label);
    form.appendChild(price);
    form.appendChild(document.createElement("BR"));

    //Effect input
    effect_label = document.createElement("label");
    effect_label.htmlFor = "effect"
    effect_label.innerHTML = "Effect description<br/>";
    effect = document.createElement("input");
    effect.type = "text"
    effect.name = "effect"
    effect.id = "effect"
    form.appendChild(effect_label);
    form.appendChild(effect);
    form.appendChild(document.createElement("BR"));

    //Location input
    location_label = document.createElement("label");
    location_label.htmlFor = "location"
    location_label.innerHTML = "Where to find<br/>";

    const location_response = await fetch("http://localhost:8000/location/", {
        method: "GET",
        }
    );
    const locations = await location_response.json();
    item_location = document.createElement("select");
    item_location.name = "location"
    item_location.id = "location"
    for (let x in locations){
        one_location = document.createElement("option");
        one_location.value = locations[x]["name"]
        one_location.innerHTML = locations[x]["name"]
        item_location.appendChild(one_location);
    }
    form.appendChild(location_label);
    form.appendChild(item_location);
    form.appendChild(document.createElement("BR"));

    //Submit button    
    button = document.createElement("input");
    button.type = "button";
    button.name = "button";
    button.id = "button";
    button.value = "Send";
    button.onclick = function() {sender()};
    form.appendChild(button);
    
    body.append(form);
}

async function sender() {
    base_url = "http://localhost:8000/items"
    alert_message = "Missing data:\n"
    must_alert = false

    add1 = document.getElementById("name").value;
    if (add1 === ""){
        alert_message += "-Name\n"
        must_alert = true
    }
    u1 = "?name="+add1;

    add2 = document.getElementById("category").value;
    if (add2 === ""){
        alert_message += "-Category\n"
        must_alert = true
    }
    u2 = "&category="+add2;

    add3 = document.getElementById("price").value;
    if (add3 === ""){
        alert_message += "-Base price\n"
        must_alert = true
    }
    u3 = "&price="+add3;

    add4 = document.getElementById("effect").value;
    if (add4 === ""){
        alert_message += "-Effect\n"
        must_alert = true
    }
    u4 = "&effect="+add4;

    add5 = document.getElementById("location").value;
    if (add5 === ""){
        alert_message += "-Location\n"
        must_alert = true
    }
    u5 = "&location="+add5;

    if(must_alert){
        alert(alert_message)
        return
    }

    full_url = base_url+u1+u2+u3+u4+u5;
    const estado_response = await fetch(full_url, {
        method: "POST",
        }
    );
    const aceptacion = await estado_response.json();
    if(aceptacion != "Aceptado"){
        alert("Error: Invalid data.")
        return
    }
    if (estado_response.status === 200){
        alert("Successfully uploaded.")
        location.reload()
    }
    else {
        alert("Unknown error.")
    }
}

addItem()

