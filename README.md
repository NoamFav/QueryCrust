# SQL Project - QueryCrust


## Setup Instructions

1. **Manually create the database**  
   Before proceeding with the project, manually create a database named `QueryCrust` in your SQL environment.

2. **Environment Variables**  
   Create a `.env` file in the root directory of the project and add the following environment variables:

   ```bash
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/QueryCrust
   ```

   Replace `your_secret_key` with a secret key of your choice.
   Replace `username`, `password` with your MySQL username and password respectively.

3. **Initialize Flask-Migrate**  
   In the command line, run the following command to initialize Flask-Migrate:

   ```bash
   flask db init
   ```

4. **Generate migration scripts**  
   Once the migration system is initialized, generate the migration scripts by running:

   ```bash
   flask db migrate
   ```

5. **Apply the migration**  
   Finally, apply the migration to the database:

   ```bash
   flask db upgrade
   ```

6. **Install the Required Packages**

   be sure to install the required python packages

## Install Node.js

You'll also need to install Node.js for this project. Follow this [link to download Node.js](https://nodejs.org/en/download/) and install it on your machine.

You may also need to install the packages in the `package.json` file. To do this, navigate to the `frontend` directory and run the following command:

```bash
npm install
```

This will install all the required packages for the frontend.

## Launching the Project

### Unix-based Systems

- **If you have `tmux` installed**  
  Run the following script to launch the project in a `tmux` session:

  ```bash
  ./tmux_launch.sh
  ```

- **If you don't have `tmux` installed**  
  You can run the project with the following script:

  ```bash
  ./launch.sh
  ```

### Windows Systems

- **Run the Launch Script**  
  On Windows, run the following command to launch the project:

  ```bash
  Launch.cmd
  ```

## Accessing the Website

If the website doesn't open automatically in your browser, navigate to:

```
http://localhost:9000
```

This will allow you to access the application.
