# Booking Report

This repo is created to automatically send notifications on telegram to inform the changes of a googlesheet.

## What we need?
Change the .env.example file to .env
On your google drive account, create a new google sheet. Then, we will press on the top right button "Share" and will select share with link.
Copy the url to your clipboard. It will be something like "https://docs.google.com/spreadsheets/d/**18qtpMICtaPBnu85H6mat3NSFkPh5PV4f7sjkl3890S**/edit?usp=sharing". Copy the bold text and set it to the variable "SHEET_ID" on your .env file
Create a telegram api token and set it to "TELEGRAM_API_TOKEN" var on .env file
Copy your telegram chat id and paste it to "TELEGRAM_CHAT_ID" var on .env file. you can write more than one separated by "," like in the example
Finally set the "REFRESH" value. This is the minutes that will wait to refresh your sheet.

## Execute
Once the vars are setted, run main.py file
