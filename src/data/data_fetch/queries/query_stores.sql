SELECT store_id,
       city,
       surface_area

FROM stores {% if location %}
WHERE {{loaction_name}} in {{location}}{% endif %}