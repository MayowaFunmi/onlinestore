if (user == 'AnonymousUser') {
    $('#btn_1').hide();
    $('#btn_2').data('action', 'add');
    //console.log($("#btn_2").data('action'))

    var product_id = '{{ product.id }}';
    var action = $("#btn_2").data('action')
    //console.log('product_id:', product_id, 'Action:', action)

    $(".update-cart").click(function() {
        addCookieItem(product_id, action);
    });

} else {
    $('#btn_2').hide();
}

function addCookieItem(product_id, action) {
    //var cart = JSON.parse(getCookie("cart"));
    var selectedOption = $('#id_quantity option:selected').attr('value');
    console.log(parseInt(selectedOption))
    if (cart == undefined) {
        cart = {}
        console.log('Cart was created')
    }

    if (action == 'add') {
        if (cart[product_id] == null) {
            cart[product_id] = {"quantity":parseInt(selectedOption)}
        } else {
            cart[product_id]["quantity"] += parseInt(selectedOption)
        }
    }

    if (action == 'remove') {
        cart[productId]["quantity"] -= 1
        if(cart[productId]["quantity"] <= 0) {
            console.log('item should be deleted')
            delete cart[productId];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    console.log('Cart: ', cart)
    $('.cart_details').append(document.cookie)
}