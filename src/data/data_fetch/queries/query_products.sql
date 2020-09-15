SELECT product_id,
       product_name,
       gross_price,
       color,
       supplier

FROM products {% if products %}
WHERE {{product_name}} in {{products}}{% endif %}