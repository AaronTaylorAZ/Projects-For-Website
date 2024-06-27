var productPrices = {};

$(function () {
    //Json data by api call for order table
    $.get(productListApiUrl, function (response) {
        productPrices = {}
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().text('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().text('0.0');
});

$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

$("#saveOrder").on("click", function () {
    var requestPayload = {
        customer_name: $('#customerName').val(),
        grand_total: $('#product_grand_total').val(),
        order_details: []
    };

    $('.product-box-extra .row').each(function () {
        var product_id = $(this).find('.cart-product').val();
        var quantity = $(this).find('.product-qty').val();
        var total_price = $(this).find('.product-total').text();

        requestPayload.order_details.push({
            product_id: product_id,
            quantity: quantity,
            total_price: total_price
        });
    });

    $.ajax({
        url: orderSaveApiUrl,
        type: 'POST',
        contentType: 'application/json', // Ensure content type is JSON
        data: JSON.stringify(requestPayload), // Convert payload to JSON string
        success: function (response) {
            console.log('Order saved successfully. Response:', response);
            alert('Order saved successfully. Order ID: ' + response.order_id);
            // Additional success handling goes here
        },
        error: function (xhr, status, error) {
            console.error('Error saving order:', error);
            alert('Error saving order. Please try again.');
            // Additional error handling goes here
        }
    });
});