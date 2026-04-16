# Steps to insert the csv data into the databse using DBeaver
1. download the files from the *data-for-db-import* folder
2. create the tables in the databse without primary or foreign keys using *create-tables.sql* script
3. manually insert the csv data, path: *schemas*/*your_db_username*/*tables*

## right click on the name of the table and select *import data*
![right click on the name of the table and select *import data*](img/insert-1.png)

## select csv import and choose the right file
![select csv import](img/insert-2.png)

## click next until the final window
![click next until the final window](img/insert-3.png)

## finally click *Proceed*
![finally click *Proceed*](img/insert-4.png)

4. Repeat this for every table
5. Chech if the tables are filled with data
6. Run *add-primary-keys.sql* script
7. Run *add-foreign-key.sql* script
8. Run *test.sql* to check if the relations work