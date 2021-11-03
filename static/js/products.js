console.log("products")

const add_category_form = document.getElementById('add_category_form');
const edit_category_form = document.getElementById('edit_category_form');
const add_product_form = document.getElementById('add_product_form');
const edit_product_form = document.getElementById('edit_product_form');

add_category_form.addEventListener('submit', (event) => {
    event.preventDefault();
    console.log("add category");
    var name = add_category_form.elements['name'].value;
    var sub_category = add_category_form.elements['sub_category'].value;
    var csrftoken = add_category_form.elements['csrfmiddlewaretoken'].value;
    data = {
        csrfmiddlewaretoken: csrftoken,
        name: name,
        sub_category: sub_category,
        type: 'category',
    }

    $.ajax({
        url:'/products/',
        method: 'POST',
        data: data,
        success: function(result){
            console.log(result);
        },
    })
});

edit_category_form.addEventListener('submit', (event) => {
    event.preventDefault();
    console.log("edit category");
    var name = edit_category_form.elements['name'].value;
    var sub_category = edit_category_form.elements['sub_category'].value;
    var csrftoken = edit_category_form.elements['csrfmiddlewaretoken'].value;
    var cat_id = edit_category_form.elements['cat_id'].value;
    data = {
        category_id: cat_id,
        csrfmiddlewaretoken: csrftoken,
        name: name,
        sub_category: sub_category,
        type: 'category',
    }

    $.ajax({
        url:'/products/',
        method: 'PUT',
        headers:{'X-CSRFToken': csrftoken},
        data: data,
        success: function(result){
            console.log(result);
            location.reload();
        },
        error: function(error){
            alert(error.responseJSON.msg);
        }
    })
})

add_product_form.addEventListener('submit', (event) => {
    event.preventDefault();
    console.log("add product");
    var name = add_product_form.elements['name'].value;
    var product_code = add_product_form.elements['product_code'].value;
    var price = add_product_form.elements['price'].value;
    var category = add_product_form.elements['category'].value;
    var manufacture_date = add_product_form.elements['manufacture_date'].value;
    var expiry_date = add_product_form.elements['expiry_date'].value;
    var status = add_product_form.elements['status'].value;
    var csrftoken = add_product_form.elements['csrfmiddlewaretoken'].value;
    data = {
        csrfmiddlewaretoken: csrftoken,
        name: name,
        product_code: product_code,
        price: price,
        category: category,
        manufacture_date: manufacture_date,
        expiry_date: expiry_date,
        status: status,
        type: 'product',
    }

    $.ajax({
        url:'/products/',
        method: 'POST',
        data: data,
        success: function(result){
            console.log(result);
        },
        error: function(error){
            alert(error.responseJSON.msg);
        }
    })
});

edit_product_form.addEventListener('submit', (event) => {
    event.preventDefault();
    console.log("add product");
    var name = edit_product_form.elements['name'].value;
    var product_code = edit_product_form.elements['product_code'].value;
    var price = edit_product_form.elements['price'].value;
    var category = edit_product_form.elements['category'].value;
    // var manufacture_date = edit_product_form.elements['manufacture_date'].value;
    // var expiry_date = edit_product_form.elements['expiry_date'].value;
    var status = edit_product_form.elements['status'].value;
    var product_id = edit_product_form.elements['pro_id'].value;
    var csrftoken = edit_product_form.elements['csrfmiddlewaretoken'].value;
    data = {
        product_id: product_id,
        csrfmiddlewaretoken: csrftoken,
        name: name,
        product_code: product_code,
        price: price,
        category: category,
        // manufacture_date: manufacture_date,
        // expiry_date: expiry_date,
        status: status,
        type: 'product',
    }

    $.ajax({
        url:'/products/',
        method: 'PUT',
        headers:{'X-CSRFToken': csrftoken},
        data: data,
        success: function(result){
            console.log(result);
            location.reload();
        },
        error: function(error){
            // console.log(error)
            alert(error.responseJSON.msg);
            location.reload();
        }
    })
})


function editCat(cat_id){
    if (document.getElementById(`view_${cat_id}`).style.display == "block"){
        document.getElementById(`view_${cat_id}`).style.display = "none";
        document.getElementById(`edit_${cat_id}`).style.display = "block";
    }else{
        document.getElementById(`view_${cat_id}`).style.display = "block";
        document.getElementById(`edit_${cat_id}`).style.display = "none";
    }
}

function editProduct(pro_id){
    if (document.getElementById(`view_pro_${pro_id}`).style.display == "block"){
        document.getElementById(`view_pro_${pro_id}`).style.display = "none";
        document.getElementById(`edit_pro_${pro_id}`).style.display = "block";
    }else{
        document.getElementById(`view_pro_${pro_id}`).style.display = "block";
        document.getElementById(`edit_pro_${pro_id}`).style.display = "none";
    }

}