-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Checking crimes reported on the date of the theft, and the transcripst of said crime:
SELECT description
  FROM crime_scene_reports
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street = "Humphrey Street";
-- Theft of THE DUCK took place at the bakery of that street at 10:15 A.M.

-- Checking the interviews:
SELECT transcript, name
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day > 27;
-- Thief left within 10 minutes of theft, must check security footage.
-- Before 10:15 A.M. thief was seen by Eugene withdrawing money at the ATM on Legget Street.
-- Thief was on the phone for less than a minute, asked for accomplice to purchase ticket for the first flight to out of town the next day.

-- Checking security logs of the bakery between 10:15 and 10:25 A.M.:
 SELECT name
   FROM people
  WHERE license_plate IN
(SELECT license_plate
   FROM bakery_security_logs
  WHERE year = 2021
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity = "exit");
-- SUSPECTS LIST: Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce

-- Checking ATM Transactions to see who withdrew money before 10 A.M on the 28th that day, narrowing down further the list of suspects:
  SELECT name
    FROM people
   WHERE id IN
 (SELECT person_id
   FROM bank_accounts
   WHERE account_number IN
 (SELECT account_number
    FROM atm_transactions
   WHERE atm_location = "Leggett Street"
     AND transaction_type = "withdraw"
     AND year = 2021
     AND month = 7
     AND day = 28));
-- UPDATED SUSPECTS LIST: Iman, Luca, Diana, Bruce

-- Checking the phone calls that lasted less than a minute fro that day:
 SELECT name
   FROM people
  WHERE phone_number IN
(SELECT caller
   FROM phone_calls
  WHERE duration <= 60
    AND year = 2021
    AND month = 7
    AND day = 28);
-- UPDATED SUSPECTS LIST: Diana, Bruce

-- Checking first flight of the next day:
 SELECT name
   FROM people
  WHERE passport_number IN
(SELECT passport_number
   FROM passengers
  WHERE flight_id IN
(SELECT id
   FROM flights
  WHERE year = 2021
    AND month = 7
    AND day = 29
    ORDER BY hour, minute ASC
    LIMIT 1));
-- Thief is Bruce!

-- To check where Bruce escaped to, we check the destination of the flight that originates in fiftyville that bruce took:
 SELECT city
   FROM airports
  WHERE id =
(SELECT destination_airport_id
   FROM flights
  WHERE id =
(SELECT flight_id
   FROM passengers
  WHERE passport_number =
(SELECT passport_number
   FROM people
   WHERE name = "Bruce")));
-- He escaped to New York City!

-- To discover the accomplice we go through the phone logs:
 SELECT name
   FROM people
  WHERE phone_number =
(SELECT receiver
   FROM phone_calls
  WHERE duration < 60
    AND year = 2021
    AND month = 7
    AND day = 28
    AND caller =
(SELECT phone_number
   FROM people
  WHERE name = "Bruce"));
-- Accomplice is Robin!