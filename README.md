# DatabaseSemesterProject

## Links

- [Exam material](https://github.com/datsoftlyngby/soft2019spring-databases/tree/master/Exam)
- [RDF source](https://www.gutenberg.org/wiki/Gutenberg:Feeds)
- [Cities files and description](http://download.geonames.org/export/dump/)
- [FTP containing most data files](https://bit.ly/2EyCDsk)

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
load data local infile '/work/soft2019spring-databases/exam/titles.csv' into table book_titles COLUMNS terminated by '"';
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

Given that this is the largest file, it also takes forever to import:
```
Query OK, 1662465 rows affected, 706 warnings (34 min 56.14 sec)
Records: 1662466  Deleted: 0  Skipped: 1  Warnings: 706
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
CREATE TABLE `cities` (
  `geonameid` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `asciiname` varchar(255) DEFAULT NULL,
  `alternatenames` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `feature class` varchar(255) DEFAULT NULL,
  `feature code` varchar(255) DEFAULT NULL,
  `country code` varchar(255) DEFAULT NULL,
  `cc2` varchar(255) DEFAULT NULL,
  `admin1 code` varchar(255) DEFAULT NULL,
  `admin2 code` varchar(255) DEFAULT NULL,
  `admin3 code` varchar(255) DEFAULT NULL,
  `admin4 code` varchar(255) DEFAULT NULL,
  `population` varchar(255) DEFAULT NULL,
  `elevation` varchar(255) DEFAULT NULL,
  `dem` varchar(255) DEFAULT NULL,
  `timezone` varchar(255) DEFAULT NULL,
  `modification date` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`geonameid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
load data local infile '/work/soft2019spring-databases/exam/cities5000.txt' into table cities character set utf8mb4 fields terminated by '\t';
```

## Foreign keys, indexes & fixes

```sql 
update authors set last_name = null where last_name = '';
update authors set first_name = null where first_name = '';

create unique index book_titles_book_id_index on book_titles(book_id);
-- TODO give authors a primary key?
create index authors_book_id_index on authors(book_id);

alter table book_cities add foreign key (book_id) references book_titles(book_id) on delete cascade;
alter table book_cities add foreign key (city_id) references cities(geonameid) on delete cascade;

alter table cities add column `location` POINT;
update cities set `location` = ST_GeomFromText(CONCAT('POINT(', latitude, ' ', longitude, ')'), 4326);
alter table cities change location location point not null, add spatial index(location);
```

## Exporting as JSON(input for mongo)

```sql
select 
    json_object(
        'book_id', book_titles_with_authors.book_id, 
        'title', book_titles_with_authors.book_title,
        'cities', json_arrayagg(json_object(
            'name',  cities.asciiname,
            'location', json_object(
                'type', 'Point',
                'coordinates', json_array(st_y(cities.location), st_x(cities.location))
            )
        )),
        'authors', book_titles_with_authors.authors,
        'authors_org', book_titles_with_authors.authors_org
    ) as book_data 
from 
    (
        select 
            book_titles.book_id as book_id,
            book_titles.title as book_title,
            json_arrayagg(authors.name) as authors_org, 
            if(group_concat(first_name) is not null and group_concat(last_name) is not null, json_arrayagg(concat(authors.first_name,' ', authors.last_name)), 
            json_arrayagg(authors.name)) as authors 
        from 
            book_titles 
        left join authors on authors.book_id = book_titles.book_id 
        group by book_titles.book_id
    ) as book_titles_with_authors 
left join 
    book_cities on book_cities.book_id = book_titles_with_authors.book_id 
left join 
    cities on cities.geonameid = book_cities.city_id 
group by 
    book_titles_with_authors.book_id 
into outfile '/var/lib/mysql-files/book_data5';
```

#SQL

## Queries

1. ```sql
    SELECT * FROM book_titles INNER JOIN authors ON book_titles.book_id = authors.book_id
    INNER JOIN book_cities ON book_cities.book_id = book_titles.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id 
    WHERE cities.asciiname = ?;
    ```
2. ```sql
    SELECT * FROM book_titles INNER JOIN book_cities ON book_titles.book_id = book_cities.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id WHERE book_titles.title = ?;
    ```
3. ```sql
    SELECT * FROM authors INNER JOIN book_titles ON authors.book_id = book_titles.book_id INNER JOIN book_cities ON book_cities.book_id = authors.book_id
    INNER JOIN cities ON cities.geonameid = book_cities.city_id WHERE authors.name = ? OR authors.first_name = ?;

4. ```sql
    SELECT distinct(cities.asciiname), title, ST_Distance(cities.location, ST_GeomFromText(?, 4326)) as distance FROM cities INNER JOIN book_cities ON cities.geonameid = book_cities.city_id INNER JOIN book_titles ON book_titles.book_id = book_cities.book_id having distance <= ?;
    ```


# MongoDB

## Importing data

To import data use the query from MySQL section to generate a mysql dump. Then use some text editor to replace `\\"` characters to `\"` and finally run command below, changing database, collection and file names as necessary. 
```bash
mongoimport --db db_exam --collection books --file soft2019spring-databases/exam/book_data5
```


## Indexes, cleanup etc

```
db.books.updateMany( { "cities.0.name": { $type: 10 }, cities: { $size: 1 } },  { $set: { cities: [] } })

db.books.createIndex({"cities.location": '2dsphere'})
```

## Queries

1.


4. ```
db.books.find({"cities.*.location": { '$near': { $geometry: { type: 'Point', coordinates: [55.67594, 12.56553]}, '$maxDistance': 5000 } }  })
```