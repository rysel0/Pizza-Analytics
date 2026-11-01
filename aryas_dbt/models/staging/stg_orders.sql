with source as (
    select * from {{ source('raw', 'orders') }}
),
 
renamed as (
    select
        order_id,
        order_datetime,
        toDate(order_datetime) as order_date,
        toHour(order_datetime) as order_hour,
        toDayOfWeek(order_datetime) as day_of_week,
        table_number,
        waiter_id,
        total_amount
    from source
)
 
select * from renamed