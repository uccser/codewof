# Installation

## Step 1: Development Stack

Start with the [UCCSER Installation Guide][1].
You will need Docker and Docker Compose, as well as the UCCSER Development Stack before you can install CodeWOF.

Once the Development Stack is installed, and started, we can move onto installing CodeWOF

## Step 2: Get the code

In your terminal, run
```
$ git clone https://github.com/uccser/codewof
```
or
```
$ git clone git@github.com:uccser/codewof
```
if you use SSH to connect to GitHub. This may be necessary if you have two factor authentication.

## Step 3: Start the Docker services

Change directory to the codewof directory that you just
cloned, and run `./dev start` to start the application.
```
$ cd codewof
$ ./dev start
```

At this point you should be able to access the server at
https://codewof.localhost, however you'll you see an error at the
moment.

This is fine, the database hasn't be setup yet.
Run `./dev update` to load content into the database.
This may take a while, so feel free to go make a coffee
while you wait.

Once this is done, you should be able to see the website in all its glory.
But wait... there's more!

## Step 4: Setting up an account.

If you try and navigate to the Questions page, you'll see that you
need to sign in. For development, there is a command to help you do just that!
If you run `./dev sample_data`, it will load the questions into the database,
and add an Admin account with username `admin@codewof.co.nz`, and password `password`.

WARNING: THIS SHOULD ONLY EVER BE USED ON A LOCAL DEVELOPMENT SERVER,
NEVER ON A PRODUCTION SERVER.

## Next steps

- Answer some questions
- Write some questions (There's a full documentation page on this)
- Have a poke around the codebase
- Have fun!!

[1]: https://uccser.github.io/technical-documentation/installation-guide/
