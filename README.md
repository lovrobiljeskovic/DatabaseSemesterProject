# DatabaseSemesterProject

## Links

- [Exam material](https://github.com/datsoftlyngby/soft2019spring-databases/tree/master/Exam)
- [RDF source](https://www.gutenberg.org/wiki/Gutenberg:Feeds)
- [Cities files and description](http://download.geonames.org/export/dump/)

## Scripts

### parse_rdfs.py

This script extracts information about the books from the offline catalog. Change `bookFolder` variable inside it to point it to the RDF folder. It will produce two files `authors.csv` and `titles.csv`.

# MySQL

# Importing data

Obviusly all the the files mentioned in the SQL queries need to be on your system.

## Titles

```
CREATE TABLE `book_titles` (
  `book_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

```
load data local infile '/work/soft2019spring-databases/exam/titles.csv' into table titles COLUMNS terminated by '"';
```

## Book cities

```
CREATE TABLE `book_cities` (
  `id` int auto_increment not null,
  `book_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
load data local infile '/work/soft2019spring-databases/exam/book_cities.csv' into table book_cities fields terminated by ',' (book_id, city_id);
```

## Authors

```
CREATE TABLE `authors` (
  `book_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
load data local infile '/work/soft2019spring-databases/exam/authors.csv' into table authors fields terminated by ',' enclosed by '"';
```

## Cities
```
CREATE TABLE IF NOT EXISTS `cities` (
    `city_id` int(11) NOT NULL,
    `name` VARCHAR(255) not null,
    `ascii_name` varchar(255) not null,
    `alternate_names` text null,
    latitude_str varchar(255) not null,
    longitude_str varchar(255) not null,
    `feature_class` char(1) null,
    `feature_code` varchar(10) null,
    `country_code` char(2) null,
    `cc2` varchar(200) null,
    `population` bigint null,
    `elevation` int null,
    `timezone` varchar(40) null,
    `modification_date` varchar(255) null,
    primary key(city_id)
);
```

```
load data local infile '/work/soft2019spring-databases/exam/cities5000.txt' into table cities character set utf8mb4 fields terminated by '\t' (
    city_id,
    name,
    ascii_name,
    alternate_names,
    latitude_str,
    longitude_str,
    feature_class,
    feature_code,
    country_code,
    cc2,
    @dummy,
    @dummy,
    @dummy,
    @dummy,
    population,
    elevation,
    @dummy,
    timezone,
    modification_date
);
```

