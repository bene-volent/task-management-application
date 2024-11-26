@echo off

:: Remove the db.sqlite3 file
if exist db.sqlite3 (
    del db.sqlite3
    echo Removed db.sqlite3
) else (
    echo db.sqlite3 does not exist
)

:: Get the current folder name
for %%i in (.) do set CURRENT_FOLDER=%%~nxi

echo Current folder: %CURRENT_FOLDER%
:: Make migrations for each app but not the folder with the same name as the current one and not hidden folders
for /d %%d in (*) do (
    if not "%%d"=="%CURRENT_FOLDER%" (
        if not "%%d"=="." (
            python manage.py makemigrations %%d
            echo Made migrations for %%d
        )
    )
)

:: Apply migrations
python manage.py migrate
echo Applied migrations

:: Create admin
python create_admin.py