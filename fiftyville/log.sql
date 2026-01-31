
-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Step 1: Initial Setup, Crime Scene, and The First Suspect List
-- Checking the crime report and gathering the first set of suspects based on car logs.
SELECT description
FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND street = 'Humphrey Street';

-- Result: Theft was at 10:15am at the Humphrey Street bakery.

-- Finding all cars that exited the bakery between 10:15 and 10:25 (Ruth's testimony)
SELECT license_plate
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';

-- Cross-referencing plates with names to get the first suspects list
SELECT name
FROM people
WHERE license_plate IN (
    '5P2BI95', '94KL13X', '6P58WS2', '4328GD8',
    'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55'
);
-- Result: Initial suspects included Bruce, Luca, Iman, Diana, and others.

-- Step 2: Reducing Suspects (Eugene's Testimony & ATM)
-- Filtering suspects by who withdrew money at the Leggett Street ATM that morning.
SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Joining the account numbers to find the names of the remaining suspects
SELECT p.name
FROM people p
JOIN bank_accounts ba ON ba.person_id = p.id
WHERE account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)
AND p.name IN (
    SELECT name FROM people WHERE license_plate IN (
        '5P2BI95', '94KL13X', '6P58WS2', '4328GD8',
        'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55'
    )
);
-- Result: Suspects reduced to: Bruce, Diana, Iman, and Luca.

-- Step 3: The Escape Flight (Destination)
-- Finding the earliest flight out of Fiftyville on July 29, as per Raymond's testimony.
SELECT id, destination_airport_id, hour, minute
FROM flights
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND day = 29
AND month = 7
ORDER BY hour, minute
LIMIT 1;
-- Result: Flight ID 36, at 8:20 AM, heading to airport ID 4.

-- Finding the city of the destination airport ID 4
SELECT city
FROM airports
WHERE id = 4;
-- Destination: New York City.

-- Step 4: Confirming the Thief (The Flight Manifest Breakthrough)
-- Checking which of the four remaining suspects was on the confirmed escape flight (ID 36).
SELECT p.name
FROM people p
JOIN passengers ps ON p.passport_number = ps.passport_number
WHERE ps.flight_id = 36
AND p.passport_number IN (
    SELECT passport_number FROM people WHERE name IN ('Bruce', 'Diana', 'Iman', 'Luca')
);
-- Conclusion: The only suspect on Flight 36 was Bruce.
-- THIEF: Bruce.

-- Step 5: Identifying the Accomplice (Bruce's Phone Call)
-- Finding the accomplice: the receiver of Bruce's short call (less than 60 seconds).
SELECT name FROM people
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce')
    AND duration < 60
    AND day = 28
);
-- Conclusion: The accomplice is Robin.
-- ACCOMPLICE: Robin.

-- Final Solution
The THIEF is: Bruce
The city the thief ESCAPED TO: New York City
The ACCOMPLICE is: Robin
```
