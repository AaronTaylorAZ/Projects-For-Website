SELECT products.product_id, products.name, products.price_per_unit, uom.uom_name
FROM products inner join uom on products.uom_id=uom.uom_id;