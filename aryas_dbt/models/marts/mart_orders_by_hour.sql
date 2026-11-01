{{ config(materialized='table') }}
 
select
    day_of_week,
    order_hour,
    count(*) as orders_count,
    sum(total_amount) as revenue,
    round(avg(total_amount), 2) as avg_check
from {{ ref('stg_orders') }}
group by day_of_week, order_hour
order by day_of_week, order_hour