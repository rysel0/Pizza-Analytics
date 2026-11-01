{{ config(materialized='table') }}
 
with order_items as (
    select * from {{ ref('stg_order_items') }}
),
 
menu as (
    select * from {{ ref('stg_menu') }}
),
 
dish_stats as (
    select
        oi.dish_id,
        count(distinct oi.order_id) as orders_count,
        sum(oi.quantity) as total_quantity,
        sum(oi.line_revenue) as total_revenue
    from order_items oi
    group by oi.dish_id
)
 
select
    m.dish_id,
    m.dish_name,
    m.category,
    m.price,
    m.cost_price,
    m.margin_pct,
    coalesce(ds.orders_count, 0) as orders_count,
    coalesce(ds.total_quantity, 0) as total_quantity,
    coalesce(ds.total_revenue, 0) as total_revenue,
    coalesce(ds.total_quantity, 0) * m.margin_abs as total_profit
from menu m
left join dish_stats ds on m.dish_id = ds.dish_id
order by total_revenue desc