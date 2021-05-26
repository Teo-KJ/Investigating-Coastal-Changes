
CREATE TABLE shorelineData (
	location VARCHAR NOT NULL,
	date VARCHAR NOT NULL,
	shorelines VARCHAR,
	filename VARCHAR NOT NULL,
	cloud_cover FLOAT NOT NULL,
	geoaccuracy FLOAT NOT NULL,
	idx SMALLINT NOT NULL,
	satname VARCHAR NOT NULL
);


CREATE TABLE polygonData (
	location VARCHAR NOT NULL,
	polygon VARCHAR NOT NULL
);


ALTER TABLE shorelineData RENAME COLUMN date TO dates;


DROP TABLE polygonData;


DELETE FROM shorelineData
WHERE location = 'Cuddalore, India';


DELETE FROM shorelineData
WHERE date > '2020-01-01'
SET date = date || '+00:00';


UPDATE shorelineData
SET date = LEFT(date, LENGTH(date)-6)
WHERE LENGTH(date)>19;


INSERT INTO polygonData
VALUES ('TLW and TTW, Hong Kong', '%s', 'Hong Kong');


ALTER TABLE polygonData 
ADD COLUMN folder_name VARCHAR;


UPDATE polygonData SET folder_name = 'San Jose'
WHERE location = 'San Jose, Philippines';


UPDATE shorelineData
SET location = 'TLW and TTW, Hong Kong'
WHERE location = 'HK TLW and TTW';