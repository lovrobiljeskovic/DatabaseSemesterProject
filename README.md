# DatabaseSemesterProject

## Links

- [Exam material](https://github.com/datsoftlyngby/soft2019spring-databases/tree/master/Exam)
- [RDF source](https://www.gutenberg.org/wiki/Gutenberg:Feeds)


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