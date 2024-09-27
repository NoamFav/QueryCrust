USE querycrust;
CREATE TABLE `customer_personal_information` (
  `id` integer PRIMARY KEY,
  `address` integer,
  `birthday` timestamp,
  `phone_number` integer,
  `gender` varchar(18),
  `previous_orders` integer,
  `age` integer
);

CREATE TABLE `customer_orders` (
  `id` integer PRIMARY KEY,
  `customer_id` integer,
  `total_cost` float,
  `delivery_eta` timestamp,
  `ordered_at` timestamp,
  `status` varchar(10),
  `password` varchar(30)
);

CREATE TABLE `discounts` (
  `id` integer PRIMARY KEY,
  `used` boolean
);

CREATE TABLE `menu` (
  `id` integer PRIMARY KEY COMMENT 'id is preceded by 1/2/3 depending on the food type (pizza, drink, or dessert)',
  `name` varchar(25),
  `price` float
);

CREATE TABLE `ingredients` (
  `id` integer PRIMARY KEY,
  `name` varchar(20),
  `price` float
);

CREATE TABLE `ingredients_per_pizza` (
  `pizza_id` integer,
  `ingredient_id` integer
);

CREATE TABLE `sub_order` (
  `id` integer,
  `item_id` integer
);

CREATE TABLE `ordered_pizza_ingredient` (
  `id` integer,
  `ingredient_id` integer
);

CREATE TABLE `delivery_driver` (
  `id` integer PRIMARY KEY,
  `delivery_area` varchar(8),
  `last_delivery` timestamp
);

CREATE TABLE `delivery` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each delivery record
  `delivered_by` INTEGER,                 -- The ID of the delivery driver
  `order_id` INTEGER,                     -- The ID of the associated order
  `assigned_at` DATETIME,                 -- Timestamp of when the delivery was created/assigned
  `pizza_count` INTEGER DEFAULT 1,   
);

ALTER TABLE `customer_orders` ADD FOREIGN KEY (`customer_id`) REFERENCES `customer_personal_information` (`id`);

ALTER TABLE `ingredients_per_pizza` ADD FOREIGN KEY (`pizza_id`) REFERENCES `menu` (`id`);

ALTER TABLE `ingredients_per_pizza` ADD FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`);

ALTER TABLE `sub_order` ADD FOREIGN KEY (`id`) REFERENCES `customer_orders` (`id`);

ALTER TABLE `sub_order` ADD FOREIGN KEY (`item_id`) REFERENCES `menu` (`id`);

ALTER TABLE `ordered_pizza_ingredient` ADD FOREIGN KEY (`id`) REFERENCES `customer_orders` (`id`);

ALTER TABLE `ordered_pizza_ingredient` ADD FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`);

ALTER TABLE `delivery` ADD FOREIGN KEY (`delviered_by`) REFERENCES `delivery_driver` (`id`);

ALTER TABLE `delivery` ADD FOREIGN KEY (`order`) REFERENCES `customer_orders` (`id`);
