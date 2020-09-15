SELECT product_id,
       store_id,
       date,
       nb_sold_pieces

FROM transactions

WHERE date BETWEEN CAST('{{start_date}}' as date) AND CAST('{{end_date}}' as date) {% if products %} AND {{products_name}} in {{products}}{% endif %}
    {% if location %} AND {{location_name}} in {{location}}{% endif %}