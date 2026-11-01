with source as (
    select * from {{ source('raw', 'menu') }}
),
 
renamed as (
    select
        dish_id,
        dish_name,
        category,
        price,
        cost_price,
        price - cost_price as margin_abs,
        round((price - cost_price) / price * 100, 2) as margin_pct
    from source
)
 
select * from renamed