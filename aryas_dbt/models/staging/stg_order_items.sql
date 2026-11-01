with source as (
    select * from {{ source('raw', 'order_items') }}
),
 
renamed as (
    select
        order_id,
        dish_id,
        quantity,
        item_price,
        quantity * item_price as line_revenue
    from source
)
 
select * from renamed