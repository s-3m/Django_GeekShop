function recalculate_total_value () {
    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    let quantities = []
    let prices = []

    for(let i = 0; i < TOTAL_FORMS; i++) {
        let _quantity = parseInt($('input[name="orderitems-' + i +'-quantity"]').val());
        let _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantities[i] = _quantity;
        if (_price) {
            prices[i] = _price
        } else {
            prices[i] = 0
        }


    order_total_quantity = 0;
    order_total_cost = 0;

    for(let i=0; i < TOTAL_FORMS; i++) {
        order_total_quantity += quantities[i]
        order_total_cost += quantities[i] * prices[i]
    }
    }

    $('.order_total_cost').text(order_total_cost.toFixed(2));
    $('.order_total_quantity').text(order_total_quantity)
}

window.onload = function () {
    $('.order_form input[type="number"]').on('click', recalculate_total_value)
    recalculate_total_value()
}