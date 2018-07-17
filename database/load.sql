LOAD DATA LOCAL INFILE "/home/izzy/data_science/csv/hsdata3.csv"
INTO TABLE hs_courses_and_grades
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
